# Đưa google về lại 2009

Phiên bản này tốn ít bộ nhớ, ngon hơn hẳn so với google hiện nay (tin t đi, t dùng qua rồi).

# Chuẩn bị

* Stylus: [Firefox](https://addons.mozilla.org/en-US/firefox/addon/styl-us/) | [Chrome](https://chromewebstore.google.com/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne)
    
* Tampermonkey (để dùng Gbar, violent hay scriptcat nó ko chạy): [Firefox](https://addons.mozilla.org/vi/firefox/addon/tampermonkey/) | [Chrome](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
    
* Ublock origin (bản mv2) (để xoá vài yếu tố): [Firefox](https://addons.mozilla.org/vi/firefox/addon/ublock-origin/) | [Chrome](https://chromewebstore.google.com/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm)
    
* Header Editor (để chuyển user-agent, cái này tính năng nhiều lắm): [Firefox](https://addons.mozilla.org/en-US/firefox/addon/header-editor/) | [Chrome](https://chromewebstore.google.com/detail/header-editor/)
    
* Don’t track me Google (để cho Google đỡ theo dõi, khuyến khích cài đặt): [Firefox](https://addons.mozilla.org/en-US/firefox/addon/dont-track-me-google/) | [Chrome](https://chromewebstore.google.com/detail/dont-track-me-google/gdbofhhdmcladcmmfjolgndfkpobecpg)
    

# Phần chính

Phần này là hướng dẫn cho từng ứng dụng, làm theo tuần tự nếu ko muốn những lỗi không mong muốn có thể xảy ra:

## Header editor

Thêm cái này trong header editor

* Name: `OldGoogle`
    

* Modify request header
    
* Regular expression
    
* Match rules: `^https://www.google.com/(.*?$)`
    
* Header name: `user-agent`
    
* Header value: `Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)`
    

Add xong nhớ bấm save, có thế thêm vào group nếu muốn.

## Stylus

Lấy [file css](https://github.com/comdlg32/google2009/blob/main/google2009.css) từ [repo này](https://github.com/comdlg32/google2009), sau đó nhập thủ công trong stylus

bấm icon stylus, rồi chọn manage:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750619899213/789e1c8b-fc6c-45f0-b45a-267ddf6e8dc9.png#_uDarkisuploading=false&align=left&logo_match=true align="left")

sau đấy chọn dấu +:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750619961954/ead12dbf-7394-43b9-aeb9-27c8012fe950.png#_uDarkisuploading=false&align=middle&logo_match=true align="center")

Xoá hết cái đống này đi:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750621094273/7b27b436-3f90-4570-99aa-82b162901b61.png#_uDarkisuploading=false&align=middle&logo_match=true align="center")

Rồi kéo thả cái file “google2009.css” vừa tải về vào xong bấm save.

## Tampermonkey

Tải và cài đặt userscript [ở đây](https://github.com/dh6k/Google-Gbar/raw/main/google-gbar.user.js) ([fork của t](https://github.com/dh6k/Google-Gbar)) ([nguồn repo gốc](https://github.com/CallyHam/Google-Gbar))

fork của t để đảm bảo rằng trang web khác của google không bị cái thanh trên che mất, gây mất thẩm mỹ.

## Ublock Origin

Thêm trang web này làm custom filter:  
[ogg.33166099.xyz](http://ogg.33166099.xyz)

## Don’t track me google

Chỉ cần cài và sử dụng thôi.

### Và thế là hoàn tất. Mặc dù có lỗi hình ảnh ở chỗ toolbar, nhưng nhìn chung là giống tới 90% rồi.

Nhược điểm là maps sẽ có ít tính năng hơn, cũng như light mode hơi chói tí.  
còn lại vẫn có gemini, ggone, play,… đủ nhu cầu luôn.
