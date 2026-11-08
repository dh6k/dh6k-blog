# Hành trình biến Android thành AI Server: Tự chế Installer Odysseus, Debian Slim và ChromaDB không dùng Docker

## TL;DR

Ban đầu, ý định chỉ là tìm một giải pháp chạy Web UI AI gọn nhẹ trên thiết bị Android. Nhưng sau một chuỗi các thử nghiệm, sửa lỗi mất tương thích và tối ưu hóa hệ thống, kết quả thu được là một AI Control Plane hoàn chỉnh chạy ngay trong môi trường user-space Linux của Termux.

Stack kỹ thuật cuối cùng bao gồm: **Termux -> PRoot-Distro (Debian Bookworm Slim) -> Odysseus (main branch) -> ChromaDB v1.5.9 (venv riêng) -> FastEmbed -> MCP (Email, RAG, Memory, Image Gen) -> BYOK APIs**.

Setup này hoàn toàn **không sử dụng Docker**, không cài Node.js/Chromium (Browser MCP chủ động tắt để tiết kiệm tài nguyên), mặc định chỉ bind vào `127.0.0.1` để bảo mật. Toàn bộ quy trình từ kiểm tra tương thích kernel (`ptrace`/`seccomp`), khởi tạo môi trường, patch bug upstream, cho đến tự động khởi chạy dịch vụ qua **Termux:Boot** đã được đóng gói gọn gàng trong một kịch bản cài đặt tự động (`install-odysseus-android-debian-v2.sh`).

* * *

## Mục lục

1.  [Một chiếc Android có thể thành AI server nhỏ đến mức nào?](#1-m%E1%BB%99t-chi%E1%BA%BFc-android-c%C3%B3-th%E1%BB%83-th%C3%A0nh-ai-server-nh%E1%BB%8F-%C4%91%E1%BA%BFn-m%E1%BB%A9c-n%C3%A0o)
    
2.  [Mục tiêu của dự án](#2-m%E1%BB%A5c-ti%C3%AAu-c%E1%BB%A7a-d%E1%BB%B1-%C3%A1n)
    
3.  [Kiến trúc tổng thể](#3-ki%E1%BA%BFn-tr%C3%BAc-t%E1%BB%95ng-th%E1%BB%83)
    
4.  [Lựa chọn nền tảng: Vì sao PRoot-Distro + Debian Slim?](#4-l%E1%BB%B1a-ch%E1%BB%8Dn-n%E1%BB%81n-t%E1%BA%A3ng-v%C3%AC-sao-proot-distro--debian-slim)
    
5.  [So sánh kiến trúc Desktop vs Android Installer](#5-so-s%C3%A1nh-ki%E1%BA%BFn-tr%C3%BAc-desktop-vs-android-installer)
    
6.  [Nhật ký khắc phục sự cố (What Went Wrong)](#6-nh%E1%BA%ADt-k%C3%BD-kh%E1%BA%AFc-ph%E1%BB%A5c-s%E1%BB%B1-c%E1%BB%91-what-went-wrong)
    
7.  [Fix #1: Patch lỗi thiếu `Any` import ở Upstream](#7-fix-1-patch-l%E1%BB%97i-thi%E1%BA%BFu-any-import-%E1%BB%9F-upstream)
    
8.  [Fix #2: Quản lý MCP Dependency Drift](#8-fix-2-qu%E1%BA%A3n-l%C3%BD-mcp-dependency-drift)
    
9.  [Fix #3: Biến ChromaDB thành một Standalone Service](#9-fix-3-bi%E1%BA%BFn-chromadb-th%C3%A0nh-m%E1%BB%99t-standalone-service)
    
10.  [Fix #4: Xử lý FastEmbed / ONNX CPU Affinity trong PRoot](#10-fix-4-x%E1%BB%AD-l%C3%BD-fastembed--onnx-cpu-affinity-trong-proot)
     
11.  [Xử lý MIME Type Upload với `python-magic`](#11-x%E1%BB%AD-l%C3%BD-mime-type-upload-v%E1%BB%9Bi-python-magic)
     
12.  [Cắt giảm Browser MCP: Trade-off hợp lý cho Android](#12-c%E1%BA%AFt-gi%E1%BA%A3m-browser-mcp-trade-off-h%E1%BB%A3p-l%C3%BD-cho-android)
     
13.  [Launcher hai tầng: Phối hợp ChromaDB & Odysseus](#13-launcher-hai-t%E1%BA%A7ng-ph%E1%BB%91i-h%E1%BB%A3p-chromadb--odysseus)
     
14.  [Service Supervisor & Autostart không dùng Systemd](#14-service-supervisor--autostart-kh%C3%B4ng-d%C3%B9ng-systemd)
     
15.  [Tích hợp OpenCodex chạy song song](#15-t%C3%ADch-h%E1%BB%A3p-opencodex-ch%E1%BA%A1y-song-song)
     
16.  [Thử nghiệm trên Emulator: Sự cố `ptrace(TRACEME)` Permission Denied](#16-th%E1%BB%AD-nghi%E1%BB%87m-tr%C3%AAn-emulator-s%E1%BB%B1-c%E1%BB%91-ptracetraceme-permission-denied)
     
17.  [Cơ chế Fail Fast: PRoot Preflight trong Installer v2](#17-c%C6%A1-ch%E1%BA%BF-fail-fast-proot-preflight-trong-installer-v2)
     
18.  [Mặc định an toàn: Localhost Binding & Bảo mật API Keys](#18-m%E1%BA%B7c-%C4%91%E1%BB%8Bnh-an-to%C3%A0n-localhost-binding--b%E1%BA%A3o-m%E1%BA%ADt-api-keys)
     
19.  [BYOK: Vì sao mô hình này khả thi trên di động?](#19-byok-v%C3%AC-sao-m%C3%B4-h%C3%ACnh-n%C3%A0y-kh%E1%BA%A3-thi-tr%C3%AAn-di-%C4%91%E1%BB%99ng)
     
20.  [Tối ưu hóa dung lượng lưu trữ (Disk Cleanup)](#20-t%E1%BB%91i-%C6%B0u-h%C3%B3a-dung-l%C6%B0%E1%BB%A3ng-l%C6%B0u-tr%E1%BB%AF-disk-cleanup)
     
21.  [Những giới hạn kỹ thuật cần lưu ý](#21-nh%E1%BB%AFng-gi%E1%BB%9Bi-h%E1%BA%A1n-k%E1%BB%B9-thu%E1%BA%ADt-c%E1%BA%A7n-l%C6%B0u-%C3%BD)
     
22.  [Hướng dẫn sử dụng Installer](#22-h%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-s%E1%BB%AD-d%E1%BB%A5ng-installer)
     
23.  [Kết luận](#23-k%E1%BA%BFt-lu%E1%BA%ADn)
     
24.  [Maintenance Checklist: Những điểm cần theo dõi khi Upstream thay đổi](#24-maintenance-checklist-nh%E1%BB%AFng-%C4%91i%E1%BB%83m-c%E1%BA%A7n-theo-d%C3%B5i-khi-upstream-thay-%C4%91%E1%BB%95i)
     

* * *

## 1\. Một chiếc Android có thể thành AI server nhỏ đến mức nào?

Ban đầu, ý định chỉ là tìm một giải pháp chạy Web UI AI đơn giản để chạy trên chiếc điện thoại Android không còn dùng đến. Nhưng càng đi sâu vào chi tiết triển khai, yêu cầu bài toán lại càng mở rộng: làm sao để có lưu trữ Vector RAG, có bộ nhớ semantic memory, hỗ trợ các Python MCP server (Model Context Protocol), và tự động khởi động cùng hệ điều hành mà không làm cạn kiệt tài nguyên thiết bị?

Cuối cùng, thay vì một ứng dụng đơn lẻ, tôi thu được một mini Linux environment hoàn chỉnh sống ngay trong Termux, với Debian Bookworm Slim, ChromaDB, FastEmbed, MCP và một mini init system tự viết.

Bài viết này ghi lại toàn bộ quá trình: từ lý do lựa chọn kiến trúc, các lỗi bất ngờ phát sinh khi đem ứng dụng Python từ x86\_64 xuống môi trường PRoot Android, đến cách đóng gói toàn bộ các workaround đó thành một script installer có thể tái sử dụng và đáng tin cậy.

* * *

## 2\. Mục tiêu của dự án

*   **Self-host Odysseus**: Triển khai ứng dụng Web UI / Agent Orchestrator Odysseus trên thiết bị Android.
    
*   **BYOK (Bring Your Own Key)**: Sử dụng API key cá nhân kết nối tới các nhà cung cấp LLM bên ngoài để xử lý tính toán nặng.
    
*   **Không sử dụng Docker**: Loại bỏ hoàn toàn sự phụ thuộc vào Docker daemon nhằm giữ hệ thống nhẹ nhàng và portable.
    
*   **Nhẹ, gọn & Đủ tính năng**: Giữ lại các MCP server thiết yếu (Email, RAG, Memory, Image Generation) nhưng cắt giảm các thành phần quá tải cho di động.
    
*   **Mặc định an toàn**: Tất cả dịch vụ chỉ bind vào IP loopback nội bộ (`127.0.0.1`).
    

* * *

## 3\. Kiến trúc tổng thể

Sơ đồ bên dưới thể hiện cấu trúc phân tầng của toàn bộ hệ thống sau khi cài đặt:

Android Device (Host Kernel)

└── Termux App (User-Space Environment)

```plaintext
├── \~/start-services.sh (Shell Service Supervisor)

│   ├── \~/.termux/boot/10-services (Termux:Boot Autostart Hook)

│   └── \~/.bashrc / \~/.zshrc (Interactive Shell Autostart Hook)

├── \~/run-odysseus.sh (Termux Host Entrypoint / PROOT\_NO\_SECCOMP export)

└── PRoot-Distro (Syscall Translation via ptrace)

    └── Debian Bookworm Slim (Guest Rootfs)

        ├── ChromaDB Server (:8100) \[/root/chroma-venv, Data: /root/chroma-data\]

        └── Odysseus App (:7000) \[/root/odysseus/venv\]

            ├── FastEmbed / ONNX Runtime (Explicit threads \= 2\)

            ├── Python MCP Servers (Email, RAG, Memory, Image Gen)

            └── BYOK Remote LLM Providers (OpenAI, Anthropic, Gemini, v.v.)
```

*Ghi chú kiến trúc:*

*   **Browser MCP**: Chủ động tắt (`ODYSSEUS_DISABLE_BROWSER_MCP=1`). Không cài Node.js, Chromium hay Playwright.
    
*   **OpenCodex**: Thành phần tùy chọn. Script cài đặt KHÔNG tự cài OpenCodex, nhưng nếu phát hiện binary `ocx` hoặc `opencodex` đã tồn tại trên Termux host, supervisor sẽ tự động thực hiện health-check và duy trì service này chạy song song.
    

* * *

## 4\. Lựa chọn nền tảng: Vì sao PRoot-Distro + Debian Slim?

### Vì sao không dùng Docker?

Cần làm rõ rằng Docker không phải là điều tuyệt đối không thể chạy trên Android. Tuy nhiên, Docker daemon đòi hỏi kernel support rất sâu (cgroups, namespaces, overlayfs) vốn thường bị cắt giảm trên các bản ROM Android thương mại. Việc cấu hình Docker trên Android đòi hỏi thiết bị phải root và tùy chỉnh kernel – điều này làm mất đi tính đơn giản và khả năng di chuyển (portability).

Do đó, setup này chọn **PRoot-Distro** làm nền tảng vì nó hoạt động hoàn toàn ở không gian người dùng (user-space) mà không cần quyền root.

### Bản chất của PRoot

PRoot không phải là một máy ảo (VM) và cũng không phải là container cấp kernel như Docker. Khi chạy trong PRoot, hệ điều hành Linux khách (guest) vẫn dùng chung kernel của thiết bị Android host. PRoot sử dụng cơ chế `ptrace` để chặn (intercept) và dịch các lời gọi hệ thống (system calls) về đường dẫn rootfs ảo. Đây chính là yếu tố then chốt dẫn tới các hiện tượng tương thích về sau.

### Lựa chọn Debian Bookworm Slim

Installer sử dụng image `debian:bookworm-slim` thông qua hỗ trợ OCI của `proot-distro`. Những lý do thiết kế bao gồm:

1.  **Sử dụng glibc**: Khác với các distro sử dụng `musl` như Alpine, Debian dùng `glibc` giúp khả năng tương thích với các bản pre-compiled Python binary wheels (như ONNX Runtime, ChromaDB, Pydantic) mượt mà hơn rất nhiều.
    
2.  **Ecosystem phong phú**: Hệ thống quản lý gói `apt` của Debian đầy đủ và ổn định.
    
3.  **Kích thước tối ưu**: Image slim nhỏ gọn hơn đáng kể so với Ubuntu đầy đủ, loại bỏ các dịch vụ ngầm không cần thiết.
    

* * *

## 5\. So sánh kiến trúc Desktop vs Android Installer

| Thành phần | Upstream / Desktop Style | Android Installer (`install-odysseus-android-debian-v2.sh`) |
| --- | --- | --- |
| **Môi trường Linux** | Native Linux / Docker Container | Debian Bookworm Slim trong PRoot-Distro |
| **ChromaDB** | Service riêng trong Docker Compose | Standalone Python venv (`/root/chroma-venv`) bind `127.0.0.1:8100` |
| **Embedding Engine** | FastEmbed (Auto CPU Affinity) | FastEmbed với số thread cố định (`FASTEMBED_THREADS=2`) |
| **MCP Python SDK** | Unpinned Dependency | Ghim phiên bản tương thích v1 (`mcp==1.28.1`) |
| **Browser MCP** | Playwright / Node.js Process | Tắt hoàn toàn (`ODYSSEUS_DISABLE_BROWSER_MCP=1`) |
| **Quản lý Process** | Docker Compose / Systemd | Shell Supervisor (`start-services.sh`) |
| **Tự động khởi động** | OS System Service | Termux:Boot + Shell Startup Hook |
| **Địa chỉ Network Bind** | Configurable / Public IP | Mặc định chỉ Bind Loopback (`127.0.0.1`) |

* * *

## 6\. Nhật ký khắc phục sự cố (What Went Wrong)

| Hiện tượng / Triệu chứng | Nguyên nhân gốc rễ | Giải pháp trong Installer |
| --- | --- | --- |
| `NameError: name 'Any' is not defined` khi import agent loop | Bug upstream trong `src/agent_loop.py` sử dụng type hint `dict[str, Any]` nhưng quên import `Any` từ `typing` | Kiểm tra file source và bổ sung `Any` vào câu lệnh import một cách có điều kiện |
| `AttributeError: 'Server' object has no attribute 'list_tools'` | Code Odysseus main sử dụng Low-level API v1 của MCP SDK, nhưng dependency `mcp` không pin version bị nâng lên v2 | Ghim phiên bản `mcp==1.28.1` trong `requirements.txt` trước khi `pip install` |
| Log báo `ChromaDB not reachable` / `VectorRAG degraded` | Tách khỏi Docker Compose khiến Odysseus không tìm thấy ChromaDB server ở port 8100 | Dựng một venv riêng cho ChromaDB v1.5.9, quản lý lifecycle khởi động trước Odysseus |
| Log cảnh báo `pthread_setaffinity_np failed error code: 22` | ONNX Runtime trong PRoot cố tự đặt CPU affinity nhưng Android kernel/topology trả về `EINVAL` | Gán biến `FASTEMBED_THREADS=2` và patch `src/embeddings.py` truyền `threads` vào FastEmbed |
| Xử lý upload file fallback về kiểm tra đuôi mở rộng cơ bản | Môi trường Debian tối giản thiếu C-library `libmagic` để phát hiện MIME type chính xác | Cài đặt package `libmagic1` (apt) và package `python-magic` (pip) |
| Lỗi thiếu `npx` / Node.js khi kích hoạt Browser MCP | Môi trường không có Node.js; Browser MCP cố gọi `@playwright/mcp` | Patch `src/builtin_mcp.py` để loại bỏ `builtin_browser` khi phát hiện env flag tắt browser |
| `proot error: ptrace(TRACEME): Permission denied` trên emulator | Security policy hoặc kernel của Android emulator cấm hoàn toàn syscall `ptrace(TRACEME)` | Tạo bước Preflight test capability: Thử no-seccomp fallback, nếu cả hai đều thất bại thì fail fast và báo lỗi rõ ràng |

* * *

## 7\. Fix #1: Patch lỗi thiếu `Any` import ở Upstream

### Triệu chứng & Nguyên nhân

Khi chạy Odysseus lần đầu, ứng dụng tung ra lỗi:

NameError: name 'Any' is not defined

Kiểm tra tệp `src/agent_loop.py` cho thấy tệp có sử dụng type annotation `dict[str, Any]`, nhưng dòng lệnh import phía trên chỉ bao gồm:

from typing import Dict, List, Optional # Thiếu Any!

Đây là một bug thuần túy từ phía source code upstream.

### Cơ chế Patch của Installer

Installer giải quyết vấn đề này bằng một script Python ngắn chạy ngay trong môi trường Debian. Đoạn code kiểm tra chính xác sự hiện diện của `dict[str, Any]` và bổ sung `Any` vào danh sách import nếu chưa có:

\# Đoạn snippet trích từ installer

p = root / "src/agent\_loop.py"

s = p.read\_text(encoding="utf-8")

if "dict\[str, Any\]" in s:

```plaintext
m \= re.search(r"^from typing import (\[^
```

\]+)$", s, flags=re.MULTILINE)

```plaintext
if m:

    names \= \[x.strip() for x in m.group(1).split(",")\]

    if "Any" not in names:

        names.insert(0, "Any")

        s \= s\[:m.start()\] \+ "from typing import " \+ ", ".join(names) \+ s\[m.end():\]

        p.write\_text(s, encoding="utf-8")
```

### Bài học về Installer Idempotency

Script installer không sử dụng các lệnh patch mù (blind patch) hay đè file toàn bộ. Việc kiểm tra điều kiện trước khi patch giúp script đạt tính **idempotent** – có thể chạy đi chạy lại nhiều lần mà không làm hỏng nguồn code, đồng thời tự động bỏ qua nếu bản nâng cấp upstream sau này đã tự sửa lỗi này.

* * *

## 8\. Fix #2: Quản lý MCP Dependency Drift

### Sự cố API Mismatch

Trong quá trình thử nghiệm với nhánh `main` của Odysseus, việc cài đặt gói `mcp` không ghim phiên bản đã dẫn đến lỗi runtime:

AttributeError: 'Server' object has no attribute 'list\_tools'

Lý do là thư viện `mcp` upstream đã phát hành phiên bản major mới (v2.x) với các thay đổi cấu trúc API, trong khi code của Odysseus `main` vẫn đang viết theo chuẩn Low-level Server API v1 (như trang trí hàm với `@server.list_tools()`).

### Giải pháp

Để đảm bảo tính tái lập (reproducibility), installer tạo một tệp tạm để thay thế dòng `mcp` trong `requirements.txt` thành phiên bản cụ thể đã qua kiểm chứng:

mcp==1.28.1

chromadb-client==1.5.9

fastembed==0.8.0

Điều này đảm bảo rằng dù upstream dependency có thay đổi API trong tương lai, quy trình cài đặt installer vẫn cho ra một môi trường hoạt động ổn định.

* * *

## 9\. Fix #3: Biến ChromaDB thành một Standalone Service

Ứng dụng Odysseus sử dụng thư viện `chromadb-client` để tương tác với ChromaDB server qua HTTP REST API. Trong các hướng dẫn chuẩn cho Desktop, ChromaDB thường được chạy dưới dạng một container trong Docker Compose.

Vì không sử dụng Docker, installer đã chuyển đổi ChromaDB thành một dịch vụ độc lập:

1.  Tạo một Python virtualenv riêng biệt tại `/root/chroma-venv`.
    
2.  Cài đặt `chromadb==1.5.9`.
    
3.  Chỉ định thư mục lưu trữ dữ liệu tại `/root/chroma-data`.
    
4.  Lắng nghe tại `127.0.0.1:8100`.
    

### Phân biệt Core App Boot & Full Feature Stack Healthy

Trong quá trình kiểm thử, nếu ChromaDB chưa khởi động, Web UI chính của Odysseus vẫn có thể boot ở trạng thái suy giảm (degraded state) và ghi log:

\[WARN\] ChromaDB not reachable at 127.0.0.1:8100

\[WARN\] VectorRAG unavailable

\[WARN\] MemoryVectorStore degraded

Sau khi dịch vụ ChromaDB được khởi động và cổng 8100 sẵn sàng, các log sẽ chuyển sang:

\[INFO\] VectorRAG ready

\[INFO\] MemoryVectorStore ready

Đây là ví dụ rõ ràng minh họa sự khác biệt giữa việc "ứng dụng chính chạy được" và việc "toàn bộ hệ thống tính năng đạt trạng thái healthy".

* * *

## 10\. Fix #4: Xử lý FastEmbed / ONNX CPU Affinity trong PRoot

Khi FastEmbed khởi tạo các mô hình nhúng (embeddings) trong môi trường PRoot, hệ thống thường ghi nhận cảnh báo:

pthread\_setaffinity\_np failed error code: 22 Invalid argument

Mặc dù sau cảnh báo này FastEmbed vẫn tiếp tục load model và hoạt động, nhưng lỗi xuất hiện liên tục trong log.

### Giải thích nguyên nhân \[Inference\]

*\[Inference\]* ONNX Runtime mặc định cố gắng tự động phân bổ worker threads và gắn CPU affinity dựa trên cấu trúc nhân CPU của thiết bị. Tuy nhiên, kiến trúc virtual rootfs của PRoot kết hợp với chính sách phân quyền kernel Android khiến syscall `pthread_setaffinity_np` nhận được tham số không hợp lệ (`EINVAL` / 22).

### Tối ưu hóa trong Installer

Installer khắc phục vấn đề này bằng cách thiết lập biến môi trường `FASTEMBED_THREADS=2` và patch constructor của FastEmbed trong `src/embeddings.py` để truyền tham số `threads` một cách tường minh:

\# Patch trong src/embeddings.py

threads = max(1, int(os.getenv("FASTEMBED\_THREADS", "2")))

kwargs = {"model\_name": self.model, "cache\_dir": cache\_dir, "threads": threads}

Mức **2 threads** được chọn làm giá trị mặc định bảo thủ (conservative default) giúp giảm thiểu xung đột cấu hình CPU trên di động mà vẫn đảm bảo hiệu năng xử lý.

* * *

## 11\. Xử lý MIME Type Upload với `python-magic`

Để việc xử lý tệp tin tải lên (file upload) trong Odysseus hoạt động chính xác thay vì fallback về nhận diện đuôi mở rộng đơn thuần, installer bổ sung:

*   C-library hệ thống: `libmagic1` (cài qua `apt-get`).
    
*   Python binding: `python-magic` (cài qua `pip`).
    

Bổ sung nhỏ này giúp ứng dụng phân loại MIME type của tài liệu chính xác hơn ở cấp độ binary.

* * *

## 12\. Cắt giảm Browser MCP: Trade-off hợp lý cho Android

Thành phần Browser MCP mặc định trong Odysseus cố gắng khởi chạy dịch vụ qua lệnh:

npx @playwright/mcp

Trong môi trường Debian tối giản ban đầu, lệnh này lập tức thất bại do thiếu Node.js và `npx`.

### Quyết định Thiết kế

Việc cài đặt Node.js, Chromium và các dependency của Playwright vào PRoot trên Android sẽ ngốn hàng gigabyte bộ nhớ và tạo ra các tiến trình chạy ngầm cực kỳ nặng nề.

Do đó, installer quyết định:

1.  **Loại bỏ**: Không cài Node.js, không cài Chromium, không cài Playwright.
    
2.  **Patch mã nguồn**: Thêm cờ tắt riêng `ODYSSEUS_DISABLE_BROWSER_MCP` vào `src/builtin_mcp.py` để loại bỏ duy nhất `builtin_browser` ra khỏi danh sách MCP server.
    
3.  **Giữ lại**: Toàn bộ các MCP server bằng Python (Email MCP, RAG MCP, Memory MCP, Image Generation MCP) vẫn hoạt động bình thường.
    

\# Injected patch in src/builtin\_mcp.py

if os.environ.get("ODYSSEUS\_DISABLE\_BROWSER\_MCP", "").lower() in ("1", "true", "yes"):

```plaintext
\_BUILTIN\_NPX\_SERVERS.pop("builtin\_browser", None)
```

Đây là một trade-off hoàn toàn hợp lý: đánh đổi tính năng tự động duyệt web bằng trình duyệt headless để lấy một hệ thống gọn nhẹ, tiết kiệm pin và RAM.

* * *

## 13\. Launcher hai tầng: Phối hợp ChromaDB & Odysseus

Để tránh tình trạng race condition khi Odysseus khởi động trước khi ChromaDB sẵn sàng, installer xây dựng cấu trúc launcher hai tầng:

### Tầng Termux Host (`~/run-odysseus.sh`)

Đóng vai trò điểm truy cập từ Termux, thiết lập các biến môi trường tương thích PRoot (như `PROOT_NO_SECCOMP=1` nếu cần) và đăng nhập vào Debian:

#!/data/data/com.termux/files/usr/bin/bash

exec proot-distro login odysseus-debian -- bash -lc '/root/start-odysseus.sh'

### Tầng Debian Guest (`/root/start-odysseus.sh`)

Hoạt động như một kịch bản điều phối chi tiết bên trong Debian:

1.  **Check Port 8100**: Lắng nghe xem ChromaDB đã mở cổng chưa.
    
2.  **Khởi động ChromaDB**: Nếu chưa, gọi `chroma run --host 127.0.0.1 --port 8100 --path /root/chroma-data` dưới dạng background process.
    
3.  **Chờ Sẵn sàng**: Vòng lặp kiểm tra tối đa 60 giây cho tới khi port 8100 phản hồi.
    
4.  **Khởi động Odysseus**: Kích hoạt venv Odysseus và chạy Uvicorn server tại `127.0.0.1:7000`.
    
5.  **Cleanup Trap**: Đăng ký `trap cleanup EXIT INT TERM` để tự động ngắt ChromaDB process nếu launcher này bị dừng.
    

* * *

## 14\. Service Supervisor & Autostart không dùng Systemd

Môi trường PRoot không chạy daemon `systemd` (PID 1). Do đó, việc quản lý các tiến trình khởi động được giao cho một kịch bản supervisor nhẹ tại `~/start-services.sh`.

```plaintext
           Android Boot / Termux Open

                       │

                       ▼

             \~/start-services.sh

                       │

        ┌──────────────┴──────────────┐

        │                             │

\[termux-wake-lock\]           \[Check Odysseus\]

                                      │

                             ┌────────┴────────┐

                             │                 │

                        Healthy/Running     Not Running

                             │                 │

                           Skip         Start \~/run-odysseus.sh

                                               │

                                      \[Check OpenCodex\]

                                               │

                                        (If installed \-\>

                                         Health & Start)
```

### Nguyên lý hoạt động của `start-services.sh`

*   **Giữ thiết bị Wake**: Bật `termux-wake-lock` để ngăn Android chuyển CPU sang trạng thái ngủ sâu (deep sleep).
    
*   **Health-check Odysseus**: Sử dụng `curl -fsS http://127.0.0.1:7000/`.
    
*   **Chống Stale PID**: Kiểm tra PID file `~/.odysseus.pid` kết hợp đọc `/proc/$pid/cmdline` để đảm bảo không nhầm lẫn nếu hệ thống Android tái sử dụng PID cũ cho một tiến trình khác.
    

### Tái sử dụng tại 2 điểm Autostart

1.  **Termux:Boot Hook** (`~/.termux/boot/10-services`): Tự động thực thi sau khi điện thoại khởi động xong 10 giây.
    
2.  **Shell Startup Hook** (`~/.bashrc` hoặc `~/.zshrc`): Tự động chạy mỗi khi người dùng mở ứng dụng Termux, giúp khôi phục dịch vụ nếu Android vô tình kill tiến trình chạy ngầm trước đó.
    

* * *

## 15\. Tích hợp OpenCodex chạy song song

Mặc dù installer **KHÔNG** cài đặt OpenCodex, nhưng kịch bản `start-services.sh` được thiết kế sẵn khả năng tương thích:

*   Kiểm tra sự tồn tại của lệnh `ocx` hoặc `opencodex` trong `$PATH`.
    
*   Nếu phát hiện binary đã được người dùng cài đặt trước đó, supervisor sẽ gọi `ocx health`.
    
*   Nếu OpenCodex chưa chạy, nó sẽ được tự động khởi động song song với Odysseus và ghi log riêng tại `~/opencodex.log`.
    

* * *

## 16\. Thử nghiệm trên Emulator: Sự cố `ptrace(TRACEME)` Permission Denied

Khi đem installer v2 sang thử nghiệm trên một môi trường Android Emulator (kiến trúc x86\_64), một sự cố nghiêm trọng đã xảy ra:

`proot-distro` thực hiện việc authenticate OCI registry, tải image `debian:bookworm-slim` (manifest x86\_64 hoàn toàn đúng kiến trúc) và giải nén rootfs thành công. Nhưng ngay khi gọi `proot-distro login odysseus-debian`, màn hình xuất hiện lỗi:

proot error: ptrace(TRACEME): Permission denied

Ngay cả khi thử đặt biến môi trường `PROOT_NO_SECCOMP=1`, lỗi trên vẫn tiếp tục xuất hiện.

### Phân tích Bản chất Lỗi

1.  **Cơ chế ptrace**: PRoot bắt buộc phải dùng lệnh hệ thống `ptrace(TRACEME)` để theo dõi và can thiệp vào các syscall của tiến trình con.
    
2.  **Nguyên nhân chính**: Kernel hoặc chính sách bảo mật (SELinux/seccomp policy) của bản build Android Emulator đó đã cấm hoàn toàn khả năng gọi `ptrace(TRACEME)`.
    
3.  **Các điểm khẳng định quan trọng**:
    
    *   Đây **KHÔNG** phải là lỗi của Debian hay `bookworm-slim`.
        
    *   Đây **KHÔNG** phải lỗi do máy khách dùng kiến trúc x86\_64 (việc lấy manifest x86\_64 trên emulator x86\_64 là hoàn toàn chính xác).
        
    *   Đây **KHÔNG** phải do thiếu `/usr/bin/bash` hay do bug của Python.
        
    *   Các lỗi liên quan đến `execve` hay loader xuất hiện phía sau chỉ là hệ quả kéo theo khi PRoot đã thất bại ngay từ bước khởi tạo đầu tiên.
        

*Lưu ý*: Không phải mọi Android Emulator đều bị lỗi này, đây chỉ là hành vi của kernel/security build cụ thể trên môi trường đã kiểm thử.

* * *

## 17\. Cơ chế Fail Fast: PRoot Preflight trong Installer v2

Từ bài học trên emulator, bản installer v2 đã bổ sung bước kiểm tra **PRoot Compatibility Preflight** ngay từ đầu script, trước khi thực hiện tải xuống hàng trăm megabyte dữ liệu của Debian.

```plaintext
                PRoot Compatibility Check

                            │

                  ┌─────────┴─────────┐

                  │                   │

           Direct PRoot OK     Direct PRoot Failed

                  │                   │

               Continue     Test PROOT\_NO\_SECCOMP=1

                                      │

                              ┌───────┴───────┐

                              │               │

                         Seccomp OK      Both Failed

                              │               │

                      Export SECCOMP=1   Abort Install

                       & Save Flag     (Fail Fast Message)

                              │

                           Continue
```

### Logic chi tiết của Preflight

info "Checking PRoot compatibility..."

PROOT\_NO\_SECCOMP\_REQUIRED=0

PROOT\_TEST\_SHELL="$PREFIX/bin/sh"

if env -u PROOT\_NO\_SECCOMP proot "$PROOT\_TEST\_SHELL" -c 'exit 0' >/dev/null 2>&1; then

```plaintext
ok "PRoot compatibility check passed."
```

elif PROOT\_NO\_SECCOMP=1 proot "$PROOT\_TEST\_SHELL" -c 'exit 0' >/dev/null 2>&1; then

```plaintext
export PROOT\_NO\_SECCOMP=1

PROOT\_NO\_SECCOMP\_REQUIRED=1

warn "PRoot works only with PROOT\_NO\_SECCOMP=1 on this device."
```

else

```plaintext
die "PRoot cannot run on this Android kernel/security policy..."
```

fi

Cách thiết kế này giúp installer phản hồi ngay lập tức (fail fast) nếu môi trường host không đủ điều kiện chạy PRoot, thay vì bắt người dùng chờ đợi tải dữ liệu rồi mới phát hiện lỗi.

* * *

## 18\. Mặc định an toàn: Localhost Binding & Bảo mật API Keys

Cả hai dịch vụ trong hệ thống đều được cấu hình chỉ lắng nghe trên giao diện loopback nội bộ:

*   **Odysseus Web UI**: `127.0.0.1:7000`
    
*   **ChromaDB Server**: `127.0.0.1:8100`
    

### Ý nghĩa Bảo mật

Việc chỉ bind vào `127.0.0.1` ngăn chặn tình trạng dịch vụ vô tình bị lộ ra ngoài mạng Wi-Fi công cộng. Điều này cực kỳ quan trọng vì Odysseus chứa các thông tin nhạy cảm như API Keys cá nhân, tài khoản email và dữ liệu bộ nhớ riêng tư.

Nếu có nhu cầu truy cập giao diện Web từ thiết bị khác, giải pháp an toàn được khuyến nghị là sử dụng mạng riêng ảo (như Tailscale/WireGuard), một Reverse Proxy có xác thực, hoặc SSH Tunneling.

* * *

## 19\. BYOK: Vì sao mô hình này khả thi trên di động?

Sở dĩ setup này hoạt động mượt mà trên một chiếc điện thoại Android cấu hình trung bình là nhờ sự phân chia trách nhiệm hợp lý trong mô hình **BYOK (Bring Your Own Key)**:

*   **Thiết bị Android đảm nhận (Local Orchestration)**:
    
    *   Giao diện Web UI và quản lý luồng hội thoại.
        
    *   Lưu trữ cơ sở dữ liệu local (`SQLite`).
        
    *   Tìm kiếm Vector Search & Memory (`ChromaDB`).
        
    *   Tạo Vector Embedding cho văn bản ngắn (`FastEmbed` / ONNX).
        
    *   Thực thi các tác vụ MCP Python nhẹ (Email, Image Gen, RAG).
        
*   **Remote Cloud Providers đảm nhận (LLM Inference)**:
    
    *   Việc tính toán xử lý mô hình ngôn ngữ lớn (LLM) hàng chục tỷ tham số được đẩy hoàn toàn sang các API provider bên ngoài (OpenAI, Anthropic, Gemini, v.v.) qua API Key của người dùng.
        

Nhờ vậy, điện thoại Android đóng vai trò như một **Control Plane / Orchestrator** thông minh chứ không cần gánh phần cứng cho tác vụ inference nặng.

* * *

## 20\. Tối ưu hóa dung lượng lưu trữ (Disk Cleanup)

Để đảm bảo hệ thống chiếm ít không gian bộ nhớ nhất trên di động, installer tự động thực hiện các bước dọn dẹp sau khi cài đặt:

*   Dùng cờ `--no-install-recommends` khi cài gói Debian `apt`.
    
*   Chạy `apt-get clean` và xóa danh sách gói `/var/lib/apt/lists/*`.
    
*   Xóa bộ nhớ tạm của pip (`rm -rf /root/.cache/pip`).
    
*   Tắt Browser MCP và dọn dẹp thư mục cache cũ `playwright-mcp-cache` nếu có.
    

* * *

## 21\. Những giới hạn kỹ thuật cần lưu ý

1.  **Phụ thuộc Kernel Android**: PRoot không phải là máy ảo độc lập, mọi hoạt động đều dựa trên kernel host của Android.
    
2.  **Cơ chế Kill Background của Android**: Một số ROM Android tùy biến có thể tắt Termux nếu không được cấu hình loại trừ tối ưu hóa pin (Battery Optimization) và bật `termux-wake-lock`.
    
3.  **Tính tương thích Emulator**: Không đảm bảo hoạt động trên mọi Android Emulator do chính sách cấm `ptrace` ở cấp độ kernel của từng nhà phát triển emulator.
    
4.  **Không dành cho Local LLM lớn**: Hệ thống thiết kế cho tác vụ Orchestration, không phù hợp để tự chạy các model LLM dung lượng lớn trực tiếp trên phần cứng điện thoại.
    
5.  **Cấu trúc Upstream thay đổi**: Nếu dự án Odysseus upstream thay đổi cấu trúc thư mục hoặc thay đổi API chính trong tương lai, các đoạn code patch trong installer có thể cần được cập nhật tương ứng.
    

* * *

## 22\. Hướng dẫn sử dụng Installer

Để cài đặt hệ thống, người dùng chỉ cần thực hiện các lệnh sau trong ứng dụng Termux:

\# Phân quyền thực thi và chạy installer

chmod +x install-odysseus-android-debian-v2.sh

./install-odysseus-android-debian-v2.sh

Sau khi quá trình cài đặt hoàn tất, truy cập ứng dụng tại địa chỉ: `http://127.0.0.1:7000`

### Các lệnh quản lý hữu ích

\# Theo dõi log hoạt động của Odysseus

tail -f ~/odysseus.log

\# Theo dõi log hoạt động của OpenCodex (nếu có)

tail -f ~/opencodex.log

\# Chạy trực tiếp launcher vào Debian

./run-odysseus.sh

\# Kiểm tra mật khẩu admin ban đầu tạo bởi setup.py

proot-distro login odysseus-debian -- cat /root/odysseus-setup.log

* * *

## 23\. Kết luận

Mục tiêu của dự án không phải là cố gắng biến một chiếc điện thoại Android thành một "AI Workstation" cồng kềnh. Thay vào đó, bằng cách kết hợp Termux, PRoot-Distro Debian Slim, ChromaDB và các bản patch tương thích nhỏ gọn, chúng ta đã tạo ra một **AI Control Plane** vô cùng hiệu quả, hoạt động ổn định và tự chủ ngay trên thiết bị di động cá nhân.

* * *

## 24\. Maintenance Checklist: Những điểm cần theo dõi khi Upstream thay đổi

Do installer có thực hiện một số bước patch mã nguồn và ghim phiên bản dependency, dưới đây là danh sách các điểm kỹ thuật cần theo dõi khi Odysseus upstream cập nhật:

*   \[ \] Upstream `src/agent_loop.py` đã bổ sung `from typing import Any` chưa?
    
*   \[ \] File `requirements.txt` upstream đã thực hiện pin phiên bản cho MCP SDK chưa?
    
*   \[ \] Odysseus đã chuyển đổi mã nguồn sang hỗ trợ MCP SDK v2.x chưa?
    
*   \[ \] Odysseus có bổ sung cờ chính thức (official environment flag) để tắt Browser MCP chưa?
    
*   \[ \] Tính tương thích API giữa `chromadb-client` và `chromadb` server khi nâng cấp phiên bản.
    
*   \[ \] Constructor của FastEmbed có thay đổi cách nhận tham số cấu hình `threads` không?
    
*   \[ \] Cập nhật của `proot-distro` liên quan đến cơ chế xử lý `seccomp` hoặc `ptrace`.
    
*   \[ \] Khả năng tương thích của base image `debian:bookworm-slim` theo thời gian.
