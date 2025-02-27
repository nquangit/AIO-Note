Khi triển khai hệ thống trên Linux, có nhiều biện pháp bảo mật bạn có thể áp dụng để bảo vệ hệ thống khỏi các mối đe dọa. Dưới đây là một số biện pháp phổ biến:

1. **Cấu hình tường lửa (Firewall)**:
   - Sử dụng `iptables`, `ufw`, hoặc `firewalld` để kiểm soát lưu lượng mạng, chặn các kết nối không cần thiết và bảo vệ hệ thống khỏi các cuộc tấn công từ bên ngoài.

2. **Cập nhật và vá lỗi hệ thống**:
   - Thường xuyên cập nhật các gói phần mềm và nhân hệ điều hành (kernel) để bảo đảm rằng tất cả các lỗ hổng bảo mật đã được vá.

3. **Sử dụng SELinux hoặc AppArmor**:
   - Cả SELinux và AppArmor đều cung cấp cơ chế kiểm soát truy cập bắt buộc (MAC), giúp bảo vệ các tài nguyên quan trọng bằng cách kiểm soát các hành vi của ứng dụng.

4. **Quản lý người dùng và quyền hạn**:
   - Hạn chế quyền truy cập root, sử dụng `sudo` để cấp quyền quản trị chỉ khi cần thiết, và đảm bảo rằng mỗi người dùng chỉ có quyền truy cập cần thiết cho công việc của họ.

5. **Sử dụng SSH bảo mật**:
   - Sử dụng chứng chỉ SSH thay vì mật khẩu để xác thực.
   - Cấu hình SSH để chặn các đăng nhập từ xa của root (`PermitRootLogin no`).
   - Đổi cổng mặc định của SSH từ 22 sang một cổng khác ít phổ biến hơn để giảm nguy cơ bị tấn công.

6. **Bảo vệ các tệp cấu hình quan trọng**:
   - Thiết lập quyền truy cập chặt chẽ cho các tệp cấu hình quan trọng, như `/etc/passwd`, `/etc/shadow`, và các tệp cấu hình của ứng dụng.

7. **Sử dụng công cụ giám sát và phát hiện xâm nhập**:
   - Cài đặt và cấu hình công cụ như `Fail2Ban`, `Snort`, hoặc `AIDE` để giám sát các hoạt động đáng ngờ và phát hiện các hành vi xâm nhập.

8. **Mã hóa dữ liệu**:
   - Sử dụng LUKS để mã hóa toàn bộ ổ đĩa hoặc các phân vùng quan trọng.
   - Sử dụng `GPG` hoặc `OpenSSL` để mã hóa các tệp dữ liệu nhạy cảm.

9. **Giới hạn dịch vụ và cổng mở**:
   - Tắt hoặc gỡ bỏ các dịch vụ không cần thiết để giảm bề mặt tấn công.
   - Sử dụng `netstat` hoặc `ss` để kiểm tra các cổng đang mở và tắt các cổng không cần thiết.

10. **Backup dữ liệu định kỳ**:
    - Thiết lập các hệ thống sao lưu dữ liệu thường xuyên và lưu trữ chúng ở vị trí an toàn, phòng trường hợp hệ thống bị tấn công hoặc xảy ra sự cố.

Những biện pháp trên sẽ giúp bạn củng cố bảo mật cho hệ thống Linux, bảo vệ chống lại các cuộc tấn công và giảm thiểu các rủi ro an ninh.



# Triển khai

---

### **1. Triển khai SELinux**

**Bước 1: Kiểm tra trạng thái SELinux**
- Để kiểm tra trạng thái hiện tại của SELinux, bạn sử dụng lệnh:
  ```bash
  sestatus
  ```
- Kết quả sẽ cho biết SELinux đang ở chế độ nào: `enforcing` (bắt buộc), `permissive` (cho phép nhưng không bắt buộc), hoặc `disabled` (tắt).

**Bước 2: Cài đặt và kích hoạt SELinux (nếu chưa có)**
- Trên các hệ thống như CentOS, RHEL hoặc Fedora, SELinux thường đã được cài đặt sẵn. Nếu chưa, bạn có thể cài đặt bằng cách:
  ```bash
  sudo yum install selinux-policy selinux-policy-targeted
  ```

**Bước 3: Kích hoạt SELinux**
- Chỉnh sửa tệp cấu hình `/etc/selinux/config`:
  ```bash
  sudo nano /etc/selinux/config
  ```
- Đảm bảo rằng dòng `SELINUX` được thiết lập là `enforcing` hoặc `permissive`:
  ```bash
  SELINUX=enforcing
  ```
- Khởi động lại hệ thống để áp dụng thay đổi:
  ```bash
  sudo reboot
  ```

**Bước 4: Quản lý chính sách SELinux**
- Các chính sách SELinux có thể được quản lý bằng cách sử dụng các lệnh như `semanage`, `setsebool`, và `audit2allow`.
- Ví dụ, để cho phép một dịch vụ cụ thể, bạn có thể sử dụng:
  ```bash
  sudo setsebool -P httpd_can_network_connect on
  ```

**Bước 5: Kiểm tra và khắc phục sự cố**
- Sử dụng lệnh `audit2allow` để tạo các quy tắc cho phép cho các sự kiện bị chặn bởi SELinux:
  ```bash
  sudo grep AVC /var/log/audit/audit.log | audit2allow -M mypol
  sudo semodule -i mypol.pp
  ```

---

### **2. Triển khai AppArmor**

**Bước 1: Cài đặt AppArmor**
- Trên các hệ thống như Ubuntu, AppArmor thường đã được cài đặt sẵn. Nếu chưa, bạn có thể cài đặt bằng cách:
  ```bash
  sudo apt-get install apparmor apparmor-utils
  ```

**Bước 2: Kích hoạt AppArmor**
- Đảm bảo rằng AppArmor được kích hoạt và khởi động cùng hệ thống. Bạn có thể kiểm tra trạng thái AppArmor bằng lệnh:
  ```bash
  sudo systemctl status apparmor
  ```
- Nếu AppArmor chưa chạy, bạn có thể kích hoạt bằng cách:
  ```bash
  sudo systemctl enable apparmor
  sudo systemctl start apparmor
  ```

**Bước 3: Quản lý các profile AppArmor**
- AppArmor sử dụng các profile để kiểm soát quyền truy cập của các ứng dụng. Bạn có thể xem danh sách các profile hiện tại bằng lệnh:
  ```bash
  sudo aa-status
  ```
- Để thiết lập hoặc chỉnh sửa một profile, bạn có thể sử dụng lệnh `aa-genprof`:
  ```bash
  sudo aa-genprof /usr/sbin/nginx
  ```
- Profile có thể ở chế độ `complain` (chỉ ghi nhận nhưng không chặn) hoặc `enforce` (bắt buộc). Bạn có thể chuyển đổi giữa hai chế độ này bằng lệnh `aa-complain` hoặc `aa-enforce`:
  ```bash
  sudo aa-enforce /etc/apparmor.d/usr.sbin.nginx
  ```

**Bước 4: Tạo và áp dụng profile mới**
- Bạn có thể tạo profile mới dựa trên hành vi của ứng dụng bằng cách sử dụng `aa-genprof` hoặc `aa-logprof` để phân tích các log:
  ```bash
  sudo aa-genprof /path/to/application
  ```
- Để áp dụng profile, đơn giản chỉ cần lưu và thoát. Sau đó, profile sẽ tự động được áp dụng khi ứng dụng được khởi động lại.

**Bước 5: Khắc phục sự cố**
- Sử dụng `dmesg` hoặc các lệnh liên quan để kiểm tra log và tạo các ngoại lệ nếu cần thiết.

---

Cả SELinux và AppArmor đều là những công cụ mạnh mẽ giúp tăng cường bảo mật cho hệ thống Linux. Tùy vào yêu cầu và mức độ phức tạp của hệ thống, bạn có thể lựa chọn giải pháp phù hợp để triển khai.