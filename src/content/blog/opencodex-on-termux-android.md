---
title: "Cài OpenCodex trên Termux Android"
description: "Biến điện thoại của bạn thành 1 api server local, phục vụ cho những tham vọng lớn lao."
pubDate: 2026-08-02
tags: ["termux", "Termux installation", "codex"]
---
Ý tưởng: tôi

Hành văn: GPT-5.6-Terra và GPT-5.6-Sol (mức high và xhigh, chạy qua Codex, mở rộng qua Brave Leo AI byom qua Opencodex trên máy tính)

## Lời mở đầu

Chạy OpenCodex trên Android bằng Termux làm được, nhưng nó không phải kiểu “cài một lệnh rồi quên luôn” như trên máy Linux đầy đủ. Android có sandbox riêng, dùng libc Bionic thay vì glibc, quản lý tiến trình nền khá gắt, và có thể giết app bất cứ lúc nào để tiết kiệm pin. Vì vậy, nếu chỉ bê nguyên hướng dẫn Linux sang rồi cầu nguyện, rất dễ gặp một mớ lỗi mơ hồ kiểu `EACCES`, `Exec format error`, hoặc service vừa chạy đã chết.

Bài này đi theo hướng thực dụng: cài từng lớp một, kiểm tra từng lớp hoạt động rồi mới ghép chúng lại. Thứ tự là:

1.  Chuẩn bị môi trường Termux đúng cách.
    
2.  Cài Node, Codex CLI và các công cụ cần thiết.
    
3.  Cài OpenCodex (`ocx`) và chạy foreground trước.
    
4.  Kiểm tra endpoint, token, port và runtime.
    
5.  Chỉ khi foreground chạy ổn mới đưa nó vào `termux-services`.
    
6.  Nếu thực sự cần, cấu hình tự chạy qua Termux:Boot.
    

Đừng nhảy thẳng tới phần service khi chưa chạy được `ocx start` trong terminal. Service không sửa được lỗi nền; nó chỉ làm lỗi khó nhìn hơn. Một thiết kế hơi ngáo nhưng rất phổ biến: biến một chương trình chưa chạy nổi thành daemon rồi mất cả log lẫn kiên nhẫn.

Hướng dẫn này giữ toàn bộ project, config và executable trong `$HOME` của Termux. Đây là filesystem Linux riêng của app, có quyền Unix, symlink và khả năng thực thi bình thường hơn. Không dùng shared storage Android làm thư mục làm việc chính.

* * *

## Phạm vi và lưu ý hỗ trợ

[OpenCodex](https://github.com/lidge-jun/opencodex) là proxy/dashboard cho Codex. README hiện liệt kê service manager cho macOS (`launchd`), Linux (`systemd` user unit) và Windows (Task Scheduler), nhưng **không liệt kê Termux/Android**.

Điều đó không có nghĩa là không thể chạy trên Android. Nó chỉ có nghĩa là đây không phải môi trường được upstream cam kết hỗ trợ. Khi có lỗi liên quan Android, Bionic, process nền hoặc lifecycle của app, không nên mặc định rằng `ocx service install` sẽ giải quyết được.

Bài này dùng `termux-services` làm lớp quản lý service native cho Termux, và tùy chọn dùng Termux:Boot để bật service sau khi Android khởi động.

[Codex CLI trên Android/Termux](https://timharbakon.com/openai-codex-cli-android-termux/) cần môi trường Termux, Node và công cụ build phù hợp. [Bun Termux](https://github.com/Happ1ness-dev/bun-termux) cung cấp Bun đã biên dịch cho Android/Bionic.

OpenCodex có thể đã kèm runtime Bun trong bản phát hành. Vì vậy, **không mặc định rằng máy nào cũng phải cài Bun riêng**. Chỉ cài `bun-termux` khi log thực tế cho thấy Bun đi kèm không chạy được hoặc vướng khác biệt Bionic/glibc.

* * *

## Chuẩn bị

Cài Termux từ [F-Droid](https://f-droid.org/packages/com.termux/) hoặc nguồn chính thức mà bạn tin cậy. Không trộn APK Termux, plugin và add-on từ các nguồn ký khác nhau. Ví dụ, cài Termux từ một nơi rồi lấy Termux:Boot từ nơi khác là cách khá hiệu quả để tạo lỗi quyền mà nhìn vào không hiểu nó đến từ đâu.

Nếu muốn tự chạy service sau khi khởi động điện thoại, cài thêm **Termux:Boot** từ cùng nguồn ký với Termux.

Trước khi làm tiếp, nên:

*   cấp quyền thông báo/chạy nền cho Termux nếu Android yêu cầu;
    
*   tắt tối ưu pin cho Termux nếu ROM thường xuyên giết tiến trình nền;
    
*   dùng mạng ổn định vì npm, GitHub và mirror package đôi lúc không thân thiện lắm;
    
*   không để lộ token admin trong ảnh chụp màn hình, log, issue hoặc repository Git.
    

Mở Termux, cập nhật package và tạo thư mục project riêng:

```bash
pkg update && pkg upgrade
mkdir -p "$HOME/projects"
cd "$HOME/projects"
```

Không đặt project trong `/sdcard`, `~/storage/shared` hoặc bất kỳ thư mục shared storage nào của Android.

Lý do không chỉ là quyền ghi. Shared storage thường không có semantics Unix đầy đủ: symlink có thể hỏng, permission bị giả lập, executable có thể bị chặn bởi `noexec`, và các tool như npm/Bun đôi khi cần những thứ đó để chạy script hoặc tạo file tạm. Đây là chỗ Android khiến Linux giả vờ biến thành ổ USB, rất duyên dáng.

* * *

## Cài công cụ nền

Cài Node LTS, Git, curl, ripgrep và OpenSSL:

```bash
pkg install nodejs-lts git curl ripgrep openssl
node --version
npm --version
git --version
curl --version
rg --version
openssl version
```

Các lệnh kiểm tra version không phải nghi thức cho vui. Chúng xác nhận rằng:

*   Node và npm đã nằm trong `PATH`;
    
*   Git có thể dùng để lấy source khi cần;
    
*   curl hoạt động để tải installer hoặc script;
    
*   ripgrep (`rg`) có sẵn để tìm log/config nhanh;
    
*   OpenSSL có thể sinh token ngẫu nhiên.
    

Node LTS là lựa chọn an toàn hơn cho Codex CLI. Những bản Node quá mới đôi khi làm native dependency hoặc script hậu cài đặt vỡ kiểu rất mất thời gian.

Nếu `nodejs-lts` không có trong mirror hiện tại hoặc `pkg install` báo package not found, đổi mirror:

```bash
termux-change-repo
pkg update
```

Sau đó thử cài lại. Đừng đi tải file `.deb` bừa trên web rồi dùng `dpkg` ép cài. Dependency mismatch trên Termux có thể biến thành mớ package nửa sống nửa chết.

* * *

## Cài Codex CLI

Dùng gói cộng đồng dành cho Termux:

```bash
npm install -g @mmmbuto/codex-cli-termux
codex --version
```

Gói này là **bên thứ ba**, không phải package OpenAI chính thức. Vì nó có quyền chạy trong shell của bạn và có thể xử lý credential, nên đọc repository, kiểm tra package/version và chỉ đăng nhập trong môi trường bạn tin cậy.

Không dán API key, session token hay token admin vào:

*   issue GitHub;
    
*   pastebin công khai;
    
*   ảnh chụp terminal;
    
*   file `.md` được commit;
    
*   log service.
    

Nếu `codex --version` báo không tìm thấy lệnh, xem phần xử lý PATH bên dưới. npm global trên Termux đôi lúc cài đúng nhưng shell hiện tại chưa trỏ tới thư mục bin đúng.

* * *

## Cài Bun Termux khi cần

Trước hết, thử OpenCodex với runtime đi kèm package. Nếu nó chạy thì không cần cài Bun riêng. Cài thêm một runtime chỉ để “chắc ăn” thường tạo ra hai binary cùng tên, hai đường PATH khác nhau, rồi sau đó không biết process đang dùng cái nào. Tự bắn vào chân nhưng có dependency manager hỗ trợ.

Khi log cho thấy Bun đi kèm không tương thích Android/Bionic, ưu tiên dùng manager theo hướng dẫn của [bun-termux](https://github.com/Happ1ness-dev/bun-termux):

```bash
curl -fsSL "https://raw.githubusercontent.com/Happ1ness-dev/bun-termux/main/helper_scripts/bun-termux-manager" | bash -s install
```

Mở shell Termux mới rồi kiểm tra:

```bash
command -v bun
bun --version
```

`command -v bun` giúp biết chính xác shell đang dùng binary nào. Nếu nó trỏ tới một đường dẫn lạ hoặc một bản cài cũ, cần dọn PATH trước khi debug sâu hơn.

Fallback thủ công được tài liệu hóa trong repository `bun-termux`:

```bash
pkg install git curl clang make glibc-repo python
pkg install glibc-runner
touch ~/.bashrc
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc
git clone https://github.com/Happ1ness-dev/bun-termux "$HOME/projects/bun-termux"
cd "$HOME/projects/bun-termux"
make && make install
bun --version
bun --bun x cowsay
```

Đoạn này có nhiều lớp vì Bun upstream vốn nhắm chủ yếu vào môi trường glibc, trong khi Android dùng Bionic. `bun-termux` tồn tại để lấp khoảng cách đó.

Nếu build lỗi, đừng vội chạy lại tất cả bằng `sudo`; Termux bình thường không dùng `sudo`, và quyền root không phải thuốc chữa runtime incompatibility.

* * *

## Cài và khởi chạy OpenCodex

Cài package OpenCodex global:

```bash
npm install -g @bitkyc08/opencodex
command -v ocx
ocx --version
ocx init
```

Ba lệnh đầu kiểm tra ba chuyện khác nhau:

*   `npm install -g`: package có được cài không;
    
*   `command -v ocx`: shell có nhìn thấy executable không;
    
*   `ocx --version`: executable có thực sự chạy không;
    
*   `ocx init`: OpenCodex có tạo/khởi tạo state theo đúng cách không.
    

Sau đó tạo token admin ngẫu nhiên. Token này không phải mật khẩu trang trí; ai có nó có thể có quyền quản trị tùy cách OpenCodex triển khai. Đừng dùng chuỗi dễ đoán kiểu `123456`, `admin`, hay tên con mèo nhà bạn.

```bash
export OPENCODEX_ADMIN_AUTH_TOKEN="$(openssl rand -hex 32)"
ocx start --port 10100
```

Lệnh `openssl rand -hex 32` tạo 32 byte ngẫu nhiên, biểu diễn thành 64 ký tự hex.

Trong lần chạy đầu, dùng foreground thay vì service. Khi đó log hiện trực tiếp trên terminal, rất tiện để thấy runtime lỗi ở đâu.

Nếu start thành công, mở trình duyệt trên chính điện thoại tại:

```text
http://127.0.0.1:10100/#/dashboard
```

`127.0.0.1` nghĩa là chỉ máy Android đó truy cập được. Đây là lựa chọn an toàn mặc định. Không đổi sang `0.0.0.0` chỉ vì muốn truy cập từ máy khác trong LAN, trừ khi bạn hiểu rõ OpenCodex đang expose những endpoint gì và đã có lớp bảo vệ phù hợp.

* * *

## Kiểm tra sau cài

Giữ shell đang chạy OpenCodex, mở một tab Termux khác rồi chạy:

```bash
ocx status
ocx doctor
ocx health
curl -i http://127.0.0.1:10100/healthz
curl -i http://127.0.0.1:10100/api/health
```

Mục tiêu ở đây là tách lỗi theo tầng:

*   `ocx status`, `doctor`, `health`: kiểm tra từ góc nhìn CLI;
    
*   `curl /healthz`: kiểm tra process có đang lắng nghe HTTP không;
    
*   `curl /api/health`: kiểm tra endpoint API cụ thể nếu bản đó hỗ trợ.
    

`/healthz` thường là endpoint nhẹ để xác nhận proxy còn sống.

`/api/health` chỉ nên xem là phép thử troubleshooting. Tùy bản phát hành, endpoint này có thể yêu cầu auth hoặc không tồn tại. Không tự động nhét admin token vào header nếu chưa đọc tài liệu của phiên bản đang dùng.

Một số bản CLI có thể dùng cú pháp start khác. Nếu `--port` không được nhận diện, kiểm tra trực tiếp:

```bash
ocx start --help
```

Đừng đoán cờ CLI. CLI đổi option nhanh hơn người ta sửa blog hướng dẫn.

* * *

## Debug và xử lý lỗi

### Mirror, package và PATH

Nếu `pkg` tải lỗi, timeout hoặc không tìm thấy package, đổi mirror:

```bash
termux-change-repo
pkg update
```

Sau khi cài npm global, nếu gặp:

```text
ocx: command not found
```

kiểm tra npm global prefix:

```bash
npm prefix -g
export PATH="$(npm prefix -g)/bin:$PATH"
command -v ocx
```

Nếu cách này chạy được, ghi dòng `export PATH=...` vào `~/.profile` hoặc file shell startup bạn thực sự dùng.

Đừng thêm bừa vào cả `.bashrc`, `.zshrc`, `.profile`, `.bash_profile` rồi hy vọng một cái có tác dụng. Trước hết xác định shell hiện tại:

```bash
echo "$SHELL"
ps -p $$ -o comm=
```

* * *

### Shared storage, symlink và `EACCES`

Lỗi kiểu:

*   `EACCES`
    
*   `permission denied`
    
*   `operation not permitted`
    

thường do một trong các nguyên nhân sau:

1.  project/config nằm trong shared storage;
    
2.  file token có quyền quá rộng hoặc quá hẹp;
    
3.  executable/script mất bit thực thi;
    
4.  app Android hoặc filesystem chặn thao tác kiểu Unix.
    

Kiểm tra thư mục chính:

```bash
echo "$HOME"
ls -ld "$HOME" "$HOME/.opencodex"
```

Nếu path trỏ vào `/data/data/com.termux/files/home/...` thì đó là home Termux bình thường. Nếu bạn thấy `/sdcard`, `/storage/emulated/0` hoặc `~/storage/shared`, chuyển project và config về `$HOME`.

Nếu `/api/health` lỗi `EACCES` nhưng `/healthz` vẫn sống, có khả năng endpoint admin đang cố đọc token/config không đúng quyền. Thử đặt token qua biến môi trường rồi khởi động lại:

```bash
export OPENCODEX_ADMIN_AUTH_TOKEN="$(openssl rand -hex 32)"
ocx start --port 10100
```

Chỉ xóa token cũ khi hiểu rõ state hiện tại. Nếu cần xóa token file theo phạm vi hẹp:

```bash
rm -f "$HOME"/.opencodex/*.admin-token*
```

Lệnh này không thể hoàn tác. Nếu token cũ đang được dùng ở nơi khác, mọi client sử dụng token đó sẽ mất quyền truy cập.

* * *

### Bionic, glibc, Bun và npm script

Android dùng **Bionic libc**, không phải glibc. Vì vậy binary được build cho Linux desktop có thể không chạy được trên Android dù kiến trúc CPU đều là ARM64.

Các dấu hiệu phổ biến:

*   `No such file or directory` dù file có tồn tại;
    
*   `Exec format error`;
    
*   lỗi dynamic linker;
    
*   Bun crash ngay khi chạy;
    
*   native addon Node không load được.
    

Nếu gặp các lỗi đó:

1.  kiểm tra binary đang chạy là gì bằng `command -v`;
    
2.  đọc log OpenCodex;
    
3.  thử `bun --version`;
    
4.  chỉ cài `bun-termux` nếu log cho thấy runtime Bun là điểm vỡ.
    

Không chạy `npm run` trong thư mục package global chỉ để thử vận may. Script npm có thể giả định môi trường build, source tree hoặc dependency development mà bản global không có. Dùng các interface công khai trước:

```bash
ocx --help
ocx doctor
ocx start --help
```

* * *

### Port đã bị chiếm

Nếu OpenCodex báo không bind được port hoặc browser không vào được dashboard, kiểm tra port `10100`:

```bash
curl -i http://127.0.0.1:10100/healthz
ss -ltnp | rg ':10100'
ocx start --port 10101
```

Nếu port `10101` chạy được, nghĩa là port `10100` đang bị process khác chiếm hoặc có instance OpenCodex cũ còn sống.

Khi đổi port, cần cập nhật đồng bộ:

*   URL dashboard;
    
*   script `termux-services`;
    
*   bookmark browser;
    
*   reverse proxy hoặc tunnel, nếu bạn có dùng.
    

Đừng giết process bừa chỉ vì nó đang dùng port. Đầu tiên nhìn PID và command trong output `ss`; có thể đó chính là instance OpenCodex đang chạy từ tab Termux khác.

* * *

### Token và bảo mật

Thay vì export token mỗi lần trong shell, có thể lưu token vào file riêng với permission chặt:

```bash
mkdir -p "$HOME/.config/opencodex"
openssl rand -hex 32 > "$HOME/.config/opencodex/admin-token"
chmod 600 "$HOME/.config/opencodex/admin-token"
```

`chmod 600` nghĩa là chỉ user Termux hiện tại được đọc và ghi file đó.

Không hard-code token trong script được commit Git. Nếu script boot hoặc service bị lộ, token sẽ đi theo luôn. Đây là lỗi bảo mật rất cơ bản nhưng vẫn xuất hiện khắp nơi vì người ta thích “cho tiện”, rồi tiện luôn cho người khác đăng nhập.

Mặc định chỉ bind vào `127.0.0.1`. Nếu cần truy cập từ máy khác:

*   ưu tiên VPN riêng như Tailscale/WireGuard;
    
*   hoặc SSH tunnel;
    
*   hoặc reverse proxy có TLS và auth;
    
*   không expose cổng admin trực tiếp ra Internet nếu chưa hiểu rõ bề mặt tấn công.
    

* * *

### Log và Android giết tiến trình nền

Chạy foreground là cách tốt nhất để debug ban đầu vì log ở ngay trước mặt.

Sau khi chạy dưới `termux-services`, xem trạng thái bằng:

```bash
sv status opencodex
```

Log được lưu theo cấu hình service ở:

```text
$HOME/.local/state/opencodex/log
```

Android vẫn có thể giết process nền, đặc biệt trên ROM có battery manager hung hãn. Battery optimization trên nhiều máy thực chất là “đóng app bất kể nó đang làm gì rồi gọi đó là tối ưu”.

Các biện pháp giảm nguy cơ:

*   tắt battery optimization cho Termux;
    
*   mở Termux ít nhất một lần sau reboot;
    
*   dùng Termux:Boot nếu cần;
    
*   dùng `termux-wake-lock` khi thật sự cần chạy lâu.
    

Wake lock làm tăng tiêu thụ pin. Nó không phải phép miễn tử cho process; Android vẫn có thể kill app trong các tình huống tài nguyên căng hoặc chính sách ROM đặc biệt.

* * *

## Service native Termux

Chỉ cấu hình service sau khi `ocx start --port 10100` chạy ổn ở foreground.

Cài `termux-services`:

```bash
pkg install termux-services
```

Sau khi cài, mở shell Termux mới để profile service được nạp đúng cách.

Tạo service dưới `$HOME/.config/sv/opencodex`, sau đó symlink nó vào thư mục service của Termux. Token không nằm trực tiếp trong script mà được đọc từ file riêng:

```bash
mkdir -p "$HOME/.config/sv/opencodex/log"

cat > "$HOME/.config/sv/opencodex/run" <<'SH'
#!/data/data/com.termux/files/usr/bin/sh
set -eu

export PATH="$PREFIX/bin:$PATH"

TOKEN_FILE="$HOME/.config/opencodex/admin-token"
test -r "$TOKEN_FILE"

export OPENCODEX_ADMIN_AUTH_TOKEN="$(cat "$TOKEN_FILE")"

OCX="$PREFIX/bin/ocx"
test -x "$OCX" || {
  echo "Không tìm thấy ocx tại $OCX" >&2
  exit 127
}

exec "$OCX" start --port 10100
SH

cat > "$HOME/.config/sv/opencodex/log/run" <<'SH'
#!/data/data/com.termux/files/usr/bin/sh
mkdir -p "$HOME/.local/state/opencodex/log"
exec svlogd "$HOME/.local/state/opencodex/log"
SH

chmod 700 "$HOME/.config/sv/opencodex/run" \
          "$HOME/.config/sv/opencodex/log/run"

chmod 600 "$HOME/.config/opencodex/admin-token"

ln -sfn "$HOME/.config/sv/opencodex" \
        "$PREFIX/var/service/opencodex"

source "$PREFIX/etc/profile.d/start-services.sh"

sv up opencodex
sv status opencodex
```

Cấu trúc này có vài điểm quan trọng:

*   `run` là process chính của service;
    
*   `exec` thay shell bằng process `ocx`, giúp supervisor theo dõi đúng PID;
    
*   `set -eu` khiến script fail sớm nếu biến lỗi hoặc command thất bại;
    
*   `test -r "$TOKEN_FILE"` ngăn service chạy trong trạng thái thiếu token;
    
*   `svlogd` ghi log thành file;
    
*   symlink vào `$PREFIX/var/service` là thứ để `runsv` nhìn thấy service.
    

Điều khiển lifecycle service:

```bash
source "$PREFIX/etc/profile.d/start-services.sh"

sv down opencodex
sv up opencodex
sv restart opencodex
sv status opencodex
```

Đây là tích hợp theo cơ chế native của Termux. Nó **không phải** bằng chứng rằng `ocx service install` được upstream OpenCodex hỗ trợ chính thức trên Android.

Nếu service liên tục restart, đừng chỉ nhìn `sv status`. Đọc log:

```bash
tail -n 100 "$HOME/.local/state/opencodex/log/current"
```

Các nguyên nhân thường là:

*   `ocx` không nằm ở `$PREFIX/bin/ocx`;
    
*   token file không tồn tại hoặc không đọc được;
    
*   port 10100 đã bị chiếm;
    
*   Bun/runtime lỗi;
    
*   config OpenCodex lỗi sau cập nhật.
    

* * *

## Tự chạy bằng Termux:Boot

Sau khi service chạy ổn khi bạn tự mở Termux, mới thêm boot script. Termux:Boot không thay thế service manager; nó chỉ là cơ chế gọi service khi Android khởi động.

Cài Termux:Boot từ cùng nguồn ký với Termux, mở app Termux:Boot một lần, rồi tạo script:

```bash
mkdir -p "$HOME/.termux/boot"

cat > "$HOME/.termux/boot/10-opencodex.sh" <<'SH'
#!/data/data/com.termux/files/usr/bin/sh
source "$PREFIX/etc/profile.d/start-services.sh"
termux-wake-lock
sv up opencodex
SH

chmod 700 "$HOME/.termux/boot/10-opencodex.sh"
```

Script này không tự chạy `ocx` trực tiếp. Nó chỉ bật service đã được định nghĩa sẵn. Cách đó tốt hơn vì toàn bộ config, log và restart behavior vẫn tập trung ở một nơi.

Sau reboot, kiểm tra:

```bash
source "$PREFIX/etc/profile.d/start-services.sh"
sv status opencodex
curl -i http://127.0.0.1:10100/healthz
```

Nếu không tự chạy sau reboot, kiểm tra theo thứ tự:

1.  Termux:Boot đã được mở ít nhất một lần chưa;
    
2.  Termux và Termux:Boot có cùng chữ ký/nguồn cài không;
    
3.  Android có chặn background activity không;
    
4.  script có executable không;
    
5.  service có chạy thủ công được không;
    
6.  log service nói gì.
    

* * *

## Cập nhật, gỡ và rollback

Trước khi cập nhật package global, xem package nào đang cũ:

```bash
npm outdated -g
```

Cập nhật OpenCodex và Codex CLI:

```bash
npm update -g @bitkyc08/opencodex @mmmbuto/codex-cli-termux
ocx --version
```

Sau cập nhật, kiểm tra lại ít nhất:

```bash
ocx doctor
ocx health
curl -i http://127.0.0.1:10100/healthz
```

Cập nhật có thể đổi behavior CLI, runtime, cấu trúc config hoặc endpoint. Vì vậy, trước khi update, sao lưu config và token vào nơi riêng tư.

Nếu bản mới lỗi, rollback về một version đã biết:

```bash
npm install -g @bitkyc08/opencodex@<known-version>
```

Thay `<known-version>` bằng version cụ thể bạn đã từng xác nhận hoạt động, ví dụ dạng `1.2.3`. Đừng rollback kiểu đoán mò; xem npm history hoặc log cài đặt cũ để biết bản ổn định trước đó.

Để gỡ OpenCodex và service do bài này tạo:

```bash
source "$PREFIX/etc/profile.d/start-services.sh"

sv down opencodex

rm -f "$PREFIX/var/service/opencodex"

rm -f "$HOME/.config/sv/opencodex/run" \
      "$HOME/.config/sv/opencodex/log/run"

rmdir "$HOME/.config/sv/opencodex/log" \
      "$HOME/.config/sv/opencodex" 2>/dev/null || true

rm -f "$HOME/.termux/boot/10-opencodex.sh"

rm -rf "$HOME/.local/state/opencodex/log"

npm uninstall -g @bitkyc08/opencodex
```

Lệnh trên không chủ động xóa:

*   token tại `$HOME/.config/opencodex/admin-token`;
    
*   state tại `~/.opencodex`;
    
*   Codex CLI;
    
*   Bun Termux;
    
*   `termux-services`.
    

Đó là chủ ý. Gỡ application không đồng nghĩa với xóa mọi credential và config mà không hỏi. Nếu muốn xóa toàn bộ state OpenCodex, kiểm tra backup trước rồi mới xóa thủ công.

Nếu CLI có `ocx uninstall`, đọc help trước:

```bash
ocx uninstall --help
```

Lệnh upstream có thể xóa state theo cách khác với phần service tự tạo trong bài này.

* * *

## Khi nào không nên chạy trên Android

Chạy OpenCodex trên Termux phù hợp nếu bạn muốn:

*   thử nghiệm cá nhân;
    
*   dùng dashboard cục bộ;
    
*   chạy tool nhẹ trên điện thoại/tablet;
    
*   học cách Termux, service và Android background hoạt động.
    

Nó kém phù hợp nếu bạn cần:

*   uptime ổn định;
    
*   chạy liên tục nhiều ngày;
    
*   expose service ra Internet;
    
*   xử lý code hoặc token nhạy cảm;
    
*   log, backup và giám sát nghiêm túc;
    
*   môi trường production.
    

Với nhu cầu nhạy cảm hoặc cần độ ổn định, chạy OpenCodex trên Linux/macOS được hỗ trợ tốt hơn, rồi truy cập qua SSH tunnel hoặc VPN thường là kiến trúc ít đau đầu hơn. Android không phải server mini miễn phí; nó là điện thoại có một đống chính sách power management đang chờ phá kế hoạch của bạn.

* * *

## Nguồn tham khảo

*   [OpenCodex repository](https://github.com/lidge-jun/opencodex)
    
*   [Codex CLI trên Termux Android](https://timharbakon.com/openai-codex-cli-android-termux/)
    
*   [bun-termux](https://github.com/Happ1ness-dev/bun-termux)
    
*   [termux-services](https://github.com/termux/termux-services)
    
*   [Termux:Boot](https://wiki.termux.dev/wiki/Termux%3ABoot)
    
*   [Termux](https://termux.dev/)
