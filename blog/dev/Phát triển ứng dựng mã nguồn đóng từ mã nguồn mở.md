Nếu bạn cần duy trì sự riêng tư cho ứng dụng mã nguồn đóng của mình nhưng vẫn muốn nhận các bản cập nhật từ repo upstream, bạn có thể thực hiện theo các bước sau:

1. **Tạo Repo Riêng Tư Mới:**
   - Tạo một repo riêng tư mới trên GitHub (hoặc trên một dịch vụ git khác như GitLab hoặc Bitbucket). Điều này sẽ đảm bảo rằng mã nguồn của bạn không được công khai.

2. **Clone Repo Mã Nguồn Mở:**
   - Clone repo mã nguồn mở từ GitHub về máy tính của bạn:
     ```bash
     git clone <URL-of-the-open-source-repo>
     ```

3. **Thêm Repo Riêng Tư Là Remote:**
   - Di chuyển vào thư mục của repo mã nguồn mở mà bạn vừa clone:
     ```bash
     cd <name-of-repo>
     ```
   - Thay đổi cấu hình remote để thêm repo riêng tư mới của bạn:
     ```bash
     git remote rename origin old-origin
     git remote add origin <URL-of-your-private-repo>
     ```
   - Đây là cách bạn giữ bản sao của mã nguồn mở và cập nhật repo riêng tư của bạn.

4. **Đẩy Mã Nguồn Lên Repo Riêng Tư:**
   - Đẩy mã nguồn từ repo mã nguồn mở lên repo riêng tư của bạn:
     ```bash
     git push -u origin main
     ```
   - Lưu ý rằng bạn có thể cần thay đổi `main` thành tên nhánh chính của repo.

5. **Thiết lập Upstream Remote:**
   - Thêm repo gốc (upstream) làm remote để có thể nhận các bản cập nhật từ repo mã nguồn mở:
     ```bash
     git remote add upstream <URL-of-the-open-source-repo>
     ```

6. **Nhận Cập Nhật Từ Upstream:**
   - Khi có bản cập nhật mới từ repo mã nguồn mở, bạn có thể thực hiện các bước sau để nhận các thay đổi:
     ```bash
     git fetch upstream
     git checkout main
     git merge upstream/main
     ```
   - Đẩy các cập nhật lên repo riêng tư của bạn:
     ```bash
     git push origin main
     ```

7. **Phát Triển và Tùy Chỉnh:**
   - Tiến hành phát triển và tùy chỉnh ứng dụng theo nhu cầu của bạn.

8. **Quản lý Cập Nhật:**
   - Định kỳ nhận cập nhật từ repo mã nguồn mở và duy trì mã nguồn riêng tư của bạn.

Với cách này, bạn có thể duy trì sự riêng tư cho mã nguồn của mình trong khi vẫn nhận được các cập nhật từ repo mã nguồn mở gốc.