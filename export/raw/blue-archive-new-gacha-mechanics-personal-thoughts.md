# Cơ chế gacha mới của Blue Archive: thêm pity 100, nhưng đánh đổi quyền kiểm soát ở mốc 200

Ý tưởng: tôi

Hành văn: gpt-5.6-sol (mức high, qua chat app, không phải work/codex). Đã có một chút chỉnh lí, bổ sung cho phù hợp.

Khi một hệ thống gacha tặng thêm 40 lượt quay nhưng đồng thời lấy đi quyền tự chọn ở mốc 200, câu hỏi không còn đơn giản là “được thêm bao nhiêu”. Câu hỏi đúng hơn là: sau khi đã tiêu 24.000 Pyroxene, người chơi còn kiểm soát được kết quả đến mức nào?

## Thông tin về cơ chế mới 
Từ ngày 29/07/2026, hệ thống tuyển dụng của *Blue Archive* được thay đổi theo ba điểm lớn:

*   **Recruitment Point** và cơ chế dùng 200 điểm để đổi trực tiếp một pickup bị loại bỏ.
    
*   **Recruitment Charge** được bổ sung: 100 Charge cho một học sinh 3★ với 50% khả năng là pickup; 200 Charge bảo đảm pickup của banner đang quay.
    
*   **Recruitment Count Rewards** được thêm vào, trao vé 10 lượt có thời hạn và nguyên liệu theo tổng số lần tuyển dụng trong kỳ banner.
    

Nhìn riêng từng phần, cơ chế mới có vẻ hào phóng hơn. Người chơi có một mốc 50/50 ở lượt 100, được thêm vé quay, và Charge có thể được giữ lại theo điều kiện của từng nhóm banner.

Nhưng thay đổi quan trọng nhất lại nằm ở một dòng khác:

> Khi nhận được pickup, Charge đã tích đến đúng vị trí nhân vật xuất hiện sẽ reset về 0.

Đây là điểm khiến cơ chế mới trở nên dễ chịu hơn khi săn **một mục tiêu**, nhưng kém ổn định hơn rõ rệt khi săn **hai hoặc ba nhân vật trong cùng một đợt**.

* * *

## Hai bộ đếm hoàn toàn khác nhau

Cơ chế mới sử dụng song song hai bộ đếm, và việc nhầm chúng với nhau sẽ khiến toàn bộ phép tính lệch khỏi đường ray.

### Recruitment Charge

Recruitment Charge quyết định mốc pity:

*   100 Charge: chắc chắn có một học sinh 3★, với 50% khả năng là pickup.
    
*   200 Charge: chắc chắn nhận pickup của banner đang quay.
    
*   Khi nhận pickup, Charge reset về 0 tại đúng vị trí nhân vật xuất hiện.
    
*   Các lượt còn lại phía sau pickup trong cùng một lần quay 10 tiếp tục cộng Charge mới.
    
*   Charge có thể được mang sang đợt pickup tiếp theo theo các nhóm banner tương ứng.
    

### Recruitment Count Rewards

Recruitment Count Rewards chỉ đếm tổng số lần quay trong **kỳ pickup hiện tại**:

*   Được chia sẻ giữa các pickup chạy cùng kỳ.
    
*   Không được mang sang kỳ pickup tiếp theo.
    
*   Khi kỳ hiện tại kết thúc, cả số lượt lẫn trạng thái nhận thưởng đều reset.
    
*   Sang kỳ mới, phần thưởng “lần đầu” từ mốc 10 lại có thể nhận lại.
    
*   Archive Recruitment và một số hình thức tuyển dụng bằng sản phẩm trả phí không được tính.
    

Nói cách khác, Charge là pity dài hạn; Count Rewards là một đường thưởng theo mùa. Hai thứ đứng cạnh nhau trên giao diện nhưng sống hai cuộc đời riêng, rất đúng tinh thần những hệ thống do con người thiết kế.

* * *

## Phần thưởng lượt quay thực sự bù được bao nhiêu?

Trong dãy phần thưởng lần đầu, vé 10 lượt có thời hạn xuất hiện tại các mốc:

*   70
    
*   130
    
*   150
    
*   170
    
*   270
    
*   330
    
*   350
    
*   370
    

Như vậy:

*   Trước mốc 200, người chơi nhận **4 vé 10 lượt**, tương đương 40 lượt quay.
    
*   Trước mốc 390, người chơi nhận tổng cộng **8 vé 10 lượt**, tương đương 80 lượt quay.
    

Sau mốc 390, hệ thống chuyển sang phần thưởng lặp từ 410 đến 590. Vòng lặp này có nguyên liệu, quà tặng, Keystone Fragment, Eligma và Secret Tech Note, nhưng **không có thêm vé 10 lượt**.

Vì thế, đây không phải máy in vé vô hạn. Tám vé đầu là khoản hoàn trả một lần trong mỗi kỳ pickup; sang kỳ mới, dãy phần thưởng đầu lại reset và bắt đầu từ mốc 10.

Với một người bỏ đúng 24.000 Pyroxene:

```text
24.000 Pyroxene = 200 lượt trả bằng đá
4 vé 10 lượt trước mốc 200 = 40 lượt bổ sung
Tổng lượt có thể thực hiện trong kỳ = 240
```

Phần phân tích dưới đây giả định các vé có thể được sử dụng ngay trên banner hợp lệ trong cùng kỳ và các lượt bằng vé tiếp tục được tính vào hệ thống tuyển dụng. Đây cũng là cách các bài công bố về phần thưởng mô tả tác động của bốn vé trước mốc 200.

* * *

## Bài toán Magical Girl Heavy Caliber

![](https://cdn.hashnode.com/uploads/covers/61ed6307e247b2151e61a1b1/efa59b6a-55ed-4935-944a-9f0f329634d8.png align="center")

Giả sử một đợt rerun có ba mục tiêu:

*   **Magical Suzumi**, giới hạn.
    
*   **Magical Reisa**, giới hạn.
    
*   **Magical Shimiko**, nhân vật thường và có thể lệch ra sau.
    

Người chơi có:

```text
24.000 Pyroxene
= 200 lượt bằng đá
= tối đa 240 lượt thực tế sau bốn vé thưởng
```

Hai mức mục tiêu:

*   **Kỳ vọng 1:** lấy Suzumi, Reisa và Shimiko.
    
*   **Kỳ vọng 2:** lấy Suzumi và Reisa; Shimiko có thể để lệch ra sau.
    

Ở đây, “kỳ vọng” chỉ có nghĩa là mục tiêu mong muốn, không phải giá trị kỳ vọng theo thống kê.

* * *

## Cơ chế cũ: 200 điểm là tài sản của cả đợt banner

Trong cơ chế cũ, mỗi lượt quay tạo ra 1 Recruitment Point. Đạt 200 điểm, người chơi có thể đổi trực tiếp một pickup đang diễn ra.

Điểm mạnh nhất là:

> Trúng pickup không làm mất số điểm đã tích.

May mắn không chỉ đem đến một nhân vật. Nó còn làm mốc spark 200 trở nên mạnh hơn.

### Suzumi xuất hiện sớm

Nếu Suzumi xuất hiện trong 100 lượt đầu, người chơi tiếp tục quay đến 200:

*   Nếu Reisa tự xuất hiện trước mốc 200, dùng spark đổi Shimiko.
    
    *   Kết quả: đạt kỳ vọng 1.
        
*   Nếu Reisa không xuất hiện, dùng spark đổi Reisa.
    
    *   Kết quả: đạt kỳ vọng 2.
        

Chỉ cần một trong hai nhân vật giới hạn xuất hiện tự nhiên, nhân vật còn lại đã có thể được khóa bằng spark.

### Suzumi xuất hiện ở lượt 190

Đây là tình huống cho thấy sức mạnh của hệ thống cũ rõ nhất:

```text
Lượt 190: Suzumi xuất hiện
Recruitment Point vẫn là 190
Quay thêm 10 lượt
Đủ 200 điểm và đổi Reisa
```

Kết quả:

```text
200 lượt = Suzumi + Reisa
```

Pickup đến muộn vẫn là một kết quả rất tốt. Nó không phá hủy tiến độ đã tích.

### Hai nhân vật xuất hiện tự nhiên

Nếu hai trong ba nhân vật đã xuất hiện trong 200 lượt, spark được dùng để lấy người còn thiếu:

*   Suzumi + Reisa → đổi Shimiko.
    
*   Suzumi + Shimiko → đổi Reisa.
    
*   Reisa + Shimiko → đổi Suzumi.
    

Kỳ vọng 1 vì thế không chỉ tồn tại trên lý thuyết. Nó là một kết quả mà người chơi có thể chủ động hoàn thiện bằng quyền lựa chọn ở mốc 200.

### Không ai xuất hiện

Nếu toàn bộ 200 lượt đều không có mục tiêu mong muốn, người chơi vẫn được chọn một pickup.

Đây không phải kết quả đẹp, nhưng ít nhất hệ thống không quyết định hộ người chơi rằng họ phải mang ai về.

* * *

## Cơ chế mới: 40 lượt thêm không đồng nghĩa với một spark mới

Với cơ chế mới, 24.000 Pyroxene có thể tạo ra tối đa 240 lượt thực tế nhờ bốn vé 10 lượt.

Nghe rất hấp dẫn. Nhưng 240 lượt quay và một quyền chọn ở mốc 200 là hai loại giá trị hoàn toàn khác nhau.

Gọi `x` là vị trí Suzumi xuất hiện.

Ngay tại lượt `x`:

```text
Charge → 0
```

Nếu pickup xuất hiện trong một lượt quay 10, các ô phía sau tiếp tục cộng Charge. Lượng Charge còn lại sau khi kết thúc lượt quay 10 đó là:

```text
Charge thừa = (10 - (x mod 10)) mod 10
```

Ví dụ:

*   Suzumi ở lượt 93 → sau khi hoàn tất lượt 91–100 còn 7 Charge.
    
*   Suzumi ở lượt 99 → còn 1 Charge.
    
*   Suzumi ở lượt 100 → còn 0 Charge.
    

Dù còn vài Charge lẻ, mốc pity tiếp theo vẫn được tính từ đúng vị trí pickup:

```text
Mốc 50/50 tiếp theo = x + 100
Mốc bảo đảm tiếp theo = x + 200
```

Với tổng ngân sách mới là 240 lượt:

```text
Có thể chạm 50/50 cho nhân vật thứ hai nếu x ≤ 140
Có thể bảo đảm nhân vật thứ hai nếu x ≤ 40
```

Đây là hai ngưỡng quan trọng nhất của toàn bộ bài toán.

* * *

## Trường hợp 1: Suzumi xuất hiện trong 40 lượt đầu

Nếu Suzumi xuất hiện tại `x ≤ 40`, người chơi còn ít nhất 200 lượt trong tổng ngân sách 240.

Khi đó:

```text
x + 200 ≤ 240
```

Người chơi có thể bảo đảm Reisa sau khi Charge reset.

Đây là vùng mà cơ chế mới thực sự hoạt động rất tốt: pickup đầu đến cực sớm, bốn vé thưởng đủ kéo tổng ngân sách lên 240, và hard pity thứ hai vẫn nằm trong tầm với.

Tuy nhiên, vùng này chỉ kéo dài 40 lượt đầu. Sau đó, quyền bảo đảm bắt đầu biến mất.

* * *

## Trường hợp 2: Suzumi xuất hiện từ lượt 41 đến 140

Nếu:

```text
41 ≤ x ≤ 140
```

người chơi không còn đủ 200 lượt để bảo đảm Reisa, nhưng vẫn đủ 100 lượt để chạm một mốc 50/50:

```text
x + 100 ≤ 240
```

Kết quả:

*   Thắng 50/50 → đạt kỳ vọng 2.
    
*   Thua 50/50 → Reisa chỉ còn có thể tự xuất hiện trong số lượt còn lại.
    
*   Shimiko hầu như không có một con đường chủ động nào ngoài việc tự lệch ra.
    

So với cơ chế cũ:

*   Cũ: Suzumi xuất hiện ở bất kỳ vị trí nào trước 200 → Reisa được khóa bằng spark.
    
*   Mới: Suzumi xuất hiện từ 41 đến 140 → Reisa chỉ được một mốc 50/50, không được bảo đảm.
    

Bốn vé thưởng đã nới rộng cánh cửa, nhưng không dựng lại chiếc cầu từng tồn tại ở mốc 200.

* * *

## Trường hợp 3: Suzumi đến từ 50/50 ở lượt 100

Nếu Suzumi chính là kết quả thắng 50/50 tại lượt 100:

*   Charge reset về 0.
    
*   Mốc 50/50 tiếp theo cho Reisa nằm ở lượt 200.
    
*   Sau đó người chơi còn tối đa 40 lượt bổ sung từ vé.
    

Nếu Reisa không xuất hiện tự nhiên trước lượt 200:

*   Thắng 50/50 thứ hai → đạt kỳ vọng 2.
    
*   Thua → còn 40 lượt tự nhiên để tìm Reisa.
    
*   Không có bảo đảm cho Reisa trong ngân sách 240.
    

Nếu cả Suzumi và Reisa chỉ đến từ hai mốc 50/50, xác suất minh họa là:

```text
50% × 50% = 25%
```

Đây không phải xác suất tổng thể của toàn banner, vì nhân vật vẫn có thể xuất hiện tự nhiên ở các lượt khác. Nó chỉ cho thấy rằng hai mốc 100 liên tiếp không tạo ra một bảo đảm tương đương spark cũ.

* * *

## Trường hợp 4: Suzumi xuất hiện từ lượt 141 trở đi

Nếu:

```text
x > 140
```

người chơi còn ít hơn 100 lượt trong tổng ngân sách 240.

Điều đó có nghĩa:

*   Không thể chạm thêm mốc 50/50 cho Reisa.
    
*   Reisa chỉ có thể xuất hiện tự nhiên.
    
*   Kỳ vọng 2 không còn một con đường bảo hiểm.
    
*   Kỳ vọng 1 gần như hoàn toàn phụ thuộc vào chuỗi may mắn.
    

### Ví dụ: Suzumi xuất hiện ở lượt 190

Trong cơ chế cũ:

```text
190: ra Suzumi
200: dùng spark đổi Reisa
```

Trong cơ chế mới:

```text
190: ra Suzumi, Charge reset
Tổng ngân sách tối đa: 240
Còn 50 lượt
```

Năm mươi lượt thêm tốt hơn mười lượt, nhưng vẫn không tạo ra mốc 100 Charge tiếp theo.

Kết quả từng là “may mắn muộn nhưng vẫn đổi được người thứ hai” nay trở thành “có thêm 50 cơ hội và không có bảo hiểm”. Một bên là quyền quyết định; bên kia là thêm số lần tung xúc xắc.

* * *

## Nếu Reisa xuất hiện sau Suzumi thì sao?

Gọi `y` là số lượt từ khi nhận Suzumi đến khi Reisa xuất hiện.

Reisa xuất hiện ở lượt tổng:

```text
x + y
```

Charge lại reset về 0.

Muốn chạm mốc 100 cho Shimiko trước khi hết 240 lượt:

```text
x + y + 100 ≤ 240
```

Tương đương:

```text
x + y ≤ 140
```

Muốn bảo đảm Shimiko:

```text
x + y + 200 ≤ 240
```

Tương đương:

```text
x + y ≤ 40
```

Nghĩa là để bảo đảm cả ba nhân vật bằng 24.000 Pyroxene và bốn vé thưởng, Suzumi và Reisa phải cùng xuất hiện cực sớm, với tổng vị trí của lần reset thứ hai không vượt quá lượt 40.

Về mặt toán học, điều đó có thể xảy ra.

Về mặt lập kế hoạch, nó gần như không phải một chiến lược.

Kỳ vọng 1 vì thế không bị “xóa khỏi vũ trụ”, nhưng không còn là kết quả người chơi có thể chủ động hoàn thiện bằng một spark. Nó chủ yếu dựa vào việc hai hoặc ba mục tiêu tự xuất hiện đúng lúc.

* * *

## Bốn vé 10 lượt đã thay đổi điều gì?

Phần thưởng mới không phải vô nghĩa. Nó cải thiện hệ thống theo ba cách thực tế:

1.  **Tăng số lượt quay thực tế**  
    24.000 Pyroxene có thể tạo ra tối đa 240 lượt thay vì chỉ 200.
    
2.  **Tăng cơ hội kết thúc sớm**  
    Người chỉ săn một pickup có thêm mốc 50/50 ở 100 và nhiều lượt quay hơn.
    
3.  **Hoàn lại tài nguyên theo từng kỳ**  
    Các mốc 10–390 reset sang kỳ pickup mới, nên người chơi có thể nhận lại phần thưởng lần đầu ở mỗi kỳ.
    

Nhưng bốn vé không khôi phục được ba thứ mà spark cũ từng bảo đảm:

*   Quyền chọn nhân vật ở mốc 200.
    
*   Khả năng biến một pickup đến muộn thành pickup thứ hai.
    
*   Khả năng dùng hai lần trúng tự nhiên để hoàn thiện nhân vật thứ ba.
    

Nói cách khác:

> Phần thưởng lượt quay bù vào **số lượng**, nhưng không bù lại **quyền kiểm soát**.

* * *

## So sánh trực tiếp hai cơ chế

| Tiêu chí | Cơ chế cũ | Cơ chế mới |
| --- | --- | --- |
| Ngân sách 24.000 Pyroxene | 200 lượt | Tối đa 240 lượt nhờ bốn vé thưởng |
| Mốc giữa đường | Không có | 100 Charge: 3★, 50% pickup |
| Mốc bảo đảm một pickup | 200 lượt, được chọn | 200 Charge, pickup của banner đang quay |
| Khi trúng pickup | Điểm vẫn giữ nguyên | Charge reset tại đúng vị trí pickup |
| Pickup ở lượt 190 | Thêm 10 lượt để đổi người thứ hai | Còn tối đa 50 lượt, không có pity tiếp theo |
| Bảo đảm hai pickup | Có, nếu một người tự xuất hiện trong 200 lượt | Chỉ có nếu pickup đầu xuất hiện không muộn hơn lượt 40 |
| Lấy ba nhân vật cùng đợt | Hai người tự rơi, spark người còn lại | Phụ thuộc phần lớn vào nhiều lần tự rơi |
| Quyền lựa chọn | Cao | Thấp hơn |
| Số lượt quay | Ít hơn | Nhiều hơn |
| Khả năng lập kế hoạch | Tốt hơn | Biến động hơn |
| Săn một mục tiêu | Ổn định nhưng không có pity 100 | Tốt hơn |
| Săn nhiều mục tiêu | Tốt hơn rõ rệt | Bất lợi do reset Charge |

* * *

## Khi endgame đòi hỏi roster rộng hơn

Cơ chế gacha không tồn tại trong chân không. Giá trị của nó phụ thuộc vào loại nội dung mà game yêu cầu người chơi xây dựng.

Một đội hình tiêu chuẩn của *Blue Archive* gồm bốn STRIKER và hai SPECIAL. Các nội dung endgame như Total Assault, Grand Assault và Final Restriction Release đã khuyến khích hoặc trực tiếp yêu cầu người chơi duy trì nhiều đội hình, nhiều vai trò và nhiều lớp nâng cấp khác nhau.

Chế độ **Virtual Aptitude Test** mới được công bố cho phép triển khai tối đa năm đội và trao nguyên liệu cho hệ thống nâng cấp **Deep Thought Blossom**. Hiện chưa đủ thông tin để khẳng định người chơi bắt buộc phải dùng đủ năm đội ở mọi mức thưởng, hoặc toàn bộ 30 vị trí phải là 30 học sinh không trùng nhau.

![Nội dung endgame mới. Nguồn: X (@Blue_ArchiveJP)](https://cdn.hashnode.com/uploads/covers/61ed6307e247b2151e61a1b1/ad8d5bae-8773-4016-9e38-981085bd0a9b.png align="center")

![Chế độ nâng cấp mới. Nguồn: X (@Blue_ArchiveJP)](https://cdn.hashnode.com/uploads/covers/61ed6307e247b2151e61a1b1/e29d2ea6-a8b1-40ca-8000-886dd38c25fb.png align="center")

![Hệ thống nâng cấp Deep Thought Blossom. Nguồn: X (@Blue_ArchiveJP)](https://cdn.hashnode.com/uploads/covers/61ed6307e247b2151e61a1b1/5d9104b9-a255-4b47-a9e6-df9785c17ad6.png align="center")

Tuy vậy, hướng thiết kế đã khá rõ:

> Game đang tăng giá trị của một roster rộng, đúng lúc cơ chế gacha mới làm việc chủ động lấy nhiều pickup trong cùng kỳ kém ổn định hơn.

Phần thưởng xếp hạng Total Assault hiện vẫn ở mức 1.200 Pyroxene cho Platinum và 1.000 cho Gold. Trong khi đó, số lượng nhân vật, banner và lớp nâng cấp tiếp tục mở rộng.

![Phần thưởng Total Assault. Nguồn: in-game, global server.](https://cdn.hashnode.com/uploads/covers/61ed6307e247b2151e61a1b1/8a3142bb-6b5f-4d43-bf25-77807b70d18a.png align="center")

### \[Suy luận\] Vòng lặp đối với người chơi mới

Nếu các mốc thưởng cao của nội dung mới thực sự yêu cầu nhiều đội độc lập, người chơi mới có thể rơi vào vòng lặp sau:

```text
Roster hẹp
→ khó tiến sâu trong endgame
→ nhận ít tài nguyên nâng cấp hơn
→ khó xây roster rộng hơn
→ khoảng cách với tài khoản cũ tiếp tục tăng
```

Cơ chế gacha mới không tự tạo ra vòng lặp này, nhưng nó có thể làm việc thu hẹp khoảng cách khó hơn vì người chơi mất công cụ chuyển một pickup tự nhiên thành một pickup khác bằng spark.

### \[Suy luận\] Áp lực đối với người chơi lâu năm

Người chơi lâu năm có roster rộng hơn, nhưng cũng phải:

*   duy trì nhiều đội hình hơn;
    
*   đầu tư vào nhiều lớp nâng cấp hơn;
    
*   tiếp tục theo dõi các pickup tối ưu cho từng nội dung;
    
*   chấp nhận việc một pickup đến muộn có thể reset gần toàn bộ tiến độ Charge.
    

Với họ, vấn đề không phải thiếu nhân vật tuyệt đối, mà là chi phí duy trì một roster cạnh tranh ngày càng lớn.

* * *

## Những điểm trong giả thuyết ban đầu vẫn đúng

Sau khi tính thêm bốn vé 10 lượt trước mốc 200, các kết luận sau vẫn giữ nguyên:

1.  **Cơ chế mới làm việc bảo đảm nhiều pickup trong cùng một đợt khó hơn.**
    
2.  **Pickup xuất hiện càng muộn, lượng Charge bị mất càng lớn.**
    
3.  **Một pickup ở lượt 190 vẫn tốt hơn không có gì, nhưng không còn mở khóa nhân vật thứ hai như spark cũ.**
    
4.  **Kỳ vọng lấy Suzumi, Reisa và Shimiko không còn là kết quả có thể chủ động hoàn thiện bằng 24.000 Pyroxene.**
    
5.  **Trong cấu trúc banner đôi hoặc banner ba, cơ chế cũ tận dụng may mắn tốt hơn.**
    
6.  **Phần thưởng lượt quay cải thiện số lượng cơ hội, nhưng không trả lại quyền lựa chọn.**
    

Những chỗ cần sửa là các khẳng định tuyệt đối:

*   “Không đạt được kỳ vọng nào” nên đổi thành “không còn con đường bảo hiểm để đạt kỳ vọng”.
    
*   “Kỳ vọng 1 bị loại bỏ” nên đổi thành “kỳ vọng 1 không còn khả năng được chủ động bảo đảm”.
    
*   “24.000 Pyroxene chỉ có 200 lượt” phải đổi thành “200 lượt bằng đá, tối đa 240 lượt thực tế sau bốn vé thưởng”.
    
*   Ngưỡng mới cần dùng là:
    
    *   pickup đầu ở lượt 40 trở xuống → còn khả năng bảo đảm pickup thứ hai;
        
    *   pickup đầu ở lượt 140 trở xuống → còn khả năng chạm một mốc 50/50;
        
    *   pickup đầu sau lượt 140 → không còn pity tiếp theo trong ngân sách 240.
        

* * *

## Kết luận: cơ chế nào tốt hơn?

Câu trả lời chính xác nhất không phải “cũ tốt hơn tuyệt đối” hay “mới hào phóng hơn tuyệt đối”.

Hai cơ chế tối ưu cho hai kiểu hành vi khác nhau.

### Nếu chỉ săn đúng một pickup

**Cơ chế mới tốt hơn.**

Người chơi nhận được:

*   một mốc 50/50 ở lượt 100;
    
*   hard pity ở 200 Charge;
    
*   Charge có khả năng được giữ lại theo nhóm banner;
    
*   bốn vé 10 lượt trước mốc 200;
    
*   thêm nguyên liệu và phần thưởng theo số lần quay.
    

Với một mục tiêu duy nhất, hệ thống mới giảm khả năng phải đi toàn bộ 200 lượt mà không có điểm dừng đáng kể.

### Nếu muốn lấy hai hoặc ba pickup trong cùng một đợt

**Cơ chế cũ tốt hơn rõ rệt về khả năng bảo đảm và lập kế hoạch.**

Trong hệ thống cũ:

*   một pickup tự xuất hiện → spark lấy pickup thứ hai;
    
*   hai nhân vật tự xuất hiện → spark lấy nhân vật thứ ba;
    
*   pickup xuất hiện ở lượt 190 vẫn giữ nguyên toàn bộ giá trị;
    
*   người chơi quyết định ai được nhận ở mốc 200.
    

Trong hệ thống mới:

*   người chơi có nhiều lượt quay hơn;
    
*   nhưng mỗi pickup reset Charge;
    
*   nhân vật đầu phải xuất hiện trong 40 lượt đầu mới còn đủ ngân sách bảo đảm nhân vật thứ hai;
    
*   từ lượt 41 đến 140, nhân vật thứ hai chỉ còn một mốc 50/50;
    
*   sau lượt 140, nhân vật thứ hai không còn pity trong tổng 240 lượt;
    
*   nhân vật thứ ba gần như hoàn toàn phụ thuộc vào nhiều lần tự xuất hiện.
    

Vì vậy, kết luận chính xác nhất là:

> **Cơ chế mới là một hệ thống pity tốt hơn, nhưng là một công cụ lập kế hoạch tệ hơn.**

Nó tốt hơn cho người chỉ nhắm một cánh cửa.

Nó tệ hơn cho người muốn bước qua cả hành lang.

* * *

## Kết luận cuối cùng

![](https://cdn.hashnode.com/uploads/covers/61ed6307e247b2151e61a1b1/7916f3d6-ef91-45cf-8814-587d81b77c9b.png align="center")

Với trường hợp Magical Suzumi, Magical Reisa và giả định có thêm Magical Shimiko:

*   Bốn vé 10 lượt làm cơ chế mới bớt khắc nghiệt hơn phép tính 200 lượt ban đầu.
    
*   Chúng nâng tổng số lượt tiềm năng từ 200 lên 240.
    
*   Chúng giúp người chơi có thêm cơ hội tự nhiên và mở rộng vùng có thể chạm pity thứ hai.
    
*   Nhưng chúng không khôi phục quyền chọn ở mốc 200.
    
*   Chúng không biến pickup ở lượt 190 thành nhân vật thứ hai.
    
*   Chúng không bảo đảm kỳ vọng 2 trừ khi pickup đầu xuất hiện trong 40 lượt đầu.
    
*   Chúng càng không biến kỳ vọng 1 thành một kế hoạch ổn định.
    

Đối với người chơi chỉ săn một nhân vật, cơ chế mới là một cải tiến.

Đối với người chơi tích 24.000 Pyroxene để tận dụng một đợt banner đôi hoặc banner ba, cơ chế cũ vẫn có giá trị chiến lược cao hơn.

Và còn một điều.

Hệ thống cũ thưởng cho may mắn bằng cách mở thêm lựa chọn.

Hệ thống mới thưởng cho may mắn bằng cách cho thêm lượt quay, rồi đặt đồng hồ về 0.

Con số 200 vẫn ở đó, sáng bóng như trước. Chỉ là chiếc chìa khóa từng mở được cả hành lang giờ đã được đổi thành một túi vé để thử thêm vài cánh cửa.

* * *

## Nguồn tham khảo

*   [Thông báo chính thức về việc làm mới hệ thống tuyển dụng](https://bluearchive.jp/news/newsJump/679)
    
*   [Dengeki Online: nội dung Recruitment Count Rewards và tám vé 10 lượt](https://dengekionline.com/article/202607/82720)
    
*   [AUTOMATON: 40 lượt thưởng trước mốc 200 và phản ứng về cơ chế mới](https://automaton-media.com/articles/newsjp/20260728-457011/)
    
*   [AppMedia: thông tin ban đầu về Virtual Aptitude Test và tối đa năm đội](https://appmedia.jp/blue_archive/80252752)
