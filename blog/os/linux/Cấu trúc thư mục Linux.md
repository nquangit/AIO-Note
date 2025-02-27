# **Khám Phá Cấu Trúc Thư Mục Gốc ("/") Trong Linux**

Linux là một hệ điều hành dựa trên nhân Unix, và giống như Unix, nó sử dụng một cấu trúc thư mục phân cấp để tổ chức các tập tin và thư mục. Tất cả mọi thứ trong Linux bắt đầu từ thư mục gốc, được ký hiệu là "/", và từ đó phát triển thành một cây thư mục phức tạp. Hãy cùng khám phá những thư mục quan trọng trong "/" và chức năng của chúng.

#### 1. **/** - Thư Mục Gốc
Thư mục gốc là nơi bắt đầu của tất cả các thư mục khác trong hệ thống. Đây là đỉnh của cây thư mục, và mọi thư mục khác đều là con của nó. Mọi thứ trên hệ thống tệp của Linux nằm dưới thư mục gốc này.

#### 2. **/bin** - Binaries
Thư mục `/bin` chứa các chương trình nhị phân thiết yếu cho người dùng, như các lệnh cơ bản (`ls`, `cp`, `mv`, `rm`, `cat`, v.v.). Đây là nơi lưu trữ những công cụ mà người dùng cần thiết để quản lý hệ thống, ngay cả khi hệ thống đang trong chế độ đơn người dùng (single-user mode).

#### 3. **/sbin** - System Binaries
Thư mục `/sbin` chứa các chương trình nhị phân cho quản trị hệ thống, chẳng hạn như các lệnh để khởi động, sửa chữa, và khôi phục hệ thống (`reboot`, `shutdown`, `fsck`, `mkfs`, v.v.). Các lệnh trong `/sbin` thường chỉ được sử dụng bởi người dùng root.

#### 4. **/etc** - Configuration Files
Thư mục `/etc` chứa các tập tin cấu hình của hệ thống. Đây là nơi lưu trữ các tệp cấu hình toàn hệ thống, các tập tin khởi động, và các script khởi động. Một số tệp quan trọng bao gồm `/etc/passwd` (quản lý người dùng), `/etc/fstab` (thông tin phân vùng), và `/etc/network/interfaces` (cấu hình mạng).

#### 5. **/dev** - Device Files
Thư mục `/dev` chứa các tệp thiết bị đại diện cho các thiết bị phần cứng của hệ thống, chẳng hạn như ổ cứng, bàn phím, chuột, v.v. Các tệp này không phải là tệp thông thường, mà là các tệp đặc biệt cung cấp một giao diện với các thiết bị phần cứng.

#### 6. **/proc** - Process Information
Thư mục `/proc` là một hệ thống tệp giả (pseudo-filesystem) cung cấp một giao diện với thông tin về các tiến trình đang chạy. Nó chứa các thư mục con đại diện cho mỗi tiến trình, chứa các tập tin cung cấp thông tin như trạng thái của tiến trình, tài nguyên sử dụng, và các thông tin liên quan khác.

#### 7. **/var** - Variable Files
Thư mục `/var` chứa các tệp thay đổi thường xuyên trong quá trình hoạt động của hệ thống. Điều này bao gồm các file log, file spool, và các tệp tạm thời như cache. Một số thư mục quan trọng trong `/var` bao gồm `/var/log` (lưu trữ các file log), `/var/spool` (dành cho các công việc hàng đợi như in ấn), và `/var/tmp` (dành cho các tệp tạm thời tồn tại qua các phiên khởi động).

#### 8. **/tmp** - Temporary Files
Thư mục `/tmp` được sử dụng để lưu trữ các tập tin tạm thời mà các chương trình tạo ra trong khi hoạt động. Các tệp trong `/tmp` thường được hệ thống tự động xóa khi khởi động lại để giải phóng dung lượng.

#### 9. **/usr** - User Binaries and Applications
Thư mục `/usr` chứa các chương trình và thư viện cho người dùng, cũng như các tài liệu và dữ liệu liên quan. Đây là nơi chứa các ứng dụng và tiện ích cài đặt trên hệ thống. Các thư mục con quan trọng bao gồm:
- `/usr/bin`: Chứa các chương trình nhị phân của người dùng (như `/bin`, nhưng không phải thiết yếu).
- `/usr/sbin`: Chứa các chương trình nhị phân quản trị hệ thống (giống `/sbin`, nhưng không phải thiết yếu).
- `/usr/lib`: Chứa các thư viện dùng chung cho các chương trình trong `/usr/bin` và `/usr/sbin`.

#### 10. **/lib** - Shared Libraries
Thư mục `/lib` chứa các thư viện chia sẻ cần thiết cho các tệp nhị phân trong `/bin` và `/sbin`. Thư viện này bao gồm các tệp `.so` (shared objects), là các thư viện dùng chung cho các chương trình.

#### 11. **/home** - Home Directories
Thư mục `/home` là nơi chứa các thư mục cá nhân của từng người dùng. Mỗi người dùng trên hệ thống có một thư mục con trong `/home`, chứa các tệp và cài đặt cá nhân của họ. Ví dụ, người dùng `john` sẽ có thư mục cá nhân tại `/home/john`.

#### 12. **/root** - Root Home Directory
Thư mục `/root` là thư mục cá nhân của người dùng root. Nó tương tự như các thư mục người dùng trong `/home`, nhưng chỉ dành riêng cho tài khoản quản trị cao nhất trên hệ thống.

#### 13. **/boot** - Boot Loader Files
Thư mục `/boot` chứa tất cả các tệp cần thiết cho quá trình khởi động hệ điều hành, bao gồm kernel (nhân hệ điều hành) và các tập tin cấu hình cho bootloader (như GRUB).

#### 14. **/opt** - Optional Software
Thư mục `/opt` chứa các ứng dụng và gói phần mềm bổ sung mà không được phân phối như một phần mặc định của hệ điều hành. Đây là nơi các phần mềm cài đặt thủ công hoặc các phần mềm của bên thứ ba có thể được đặt.

#### 15. **/mnt** - Mount Points
Thư mục `/mnt` được sử dụng làm điểm gắn kết tạm thời cho các hệ thống tệp. Khi bạn gắn kết một ổ đĩa, một phân vùng hoặc một thiết bị, bạn có thể sử dụng `/mnt` làm nơi tạm thời để truy cập vào nội dung của nó.

#### 16. **/media** - Removable Media
Thư mục `/media` thường được sử dụng để gắn kết các thiết bị di động như USB, CD/DVD, và các loại phương tiện lưu trữ khác khi chúng được cắm vào hệ thống.

#### 17. **/srv** - Service Data
Thư mục `/srv` chứa dữ liệu cho các dịch vụ mạng được cung cấp bởi hệ thống. Ví dụ, nếu bạn đang chạy một máy chủ web, các tệp web có thể được lưu trữ trong `/srv/www`.

#### 18. **/run** - Runtime Data
Thư mục `/run` chứa dữ liệu runtime, như PID files, socket files, và các tệp tạm thời khác mà hệ thống và các dịch vụ yêu cầu trong suốt quá trình hoạt động. Các tệp này thường được khởi tạo khi hệ thống khởi động và bị xóa khi tắt.

---

### **Kết Luận**
Hiểu rõ về cấu trúc thư mục trong Linux giúp bạn quản lý hệ thống hiệu quả hơn và dễ dàng giải quyết các vấn đề khi gặp phải. Việc nắm bắt cách thức hoạt động của từng thư mục có thể giúp bạn không chỉ điều hướng hệ thống mà còn thực hiện các tác vụ quản trị một cách tự tin hơn.
