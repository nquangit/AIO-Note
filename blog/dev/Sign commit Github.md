# Sign commit Github

Để ký commit với GPG trên GitHub, bạn cần làm theo các bước dưới đây. Điều này đảm bảo rằng commit của bạn sẽ hiển thị với dấu "Verified" trên GitHub, chứng minh rằng bạn là người tạo ra commit đó.

### Bước 1: Cài đặt GPG

**Trên macOS:**
```bash
brew install gnupg
```

**Trên Ubuntu/Debian:**
```bash
sudo apt-get install gnupg
```

**Trên Windows:**
- Bạn có thể tải [Gpg4win](https://gpg4win.org/download.html) để cài đặt GPG.

### Bước 2: Tạo một cặp khóa GPG mới

Chạy lệnh sau để tạo cặp khóa GPG:

```bash
gpg --full-generate-key
```

Làm theo hướng dẫn trên màn hình để cấu hình khóa của bạn. Khi được hỏi về kiểu khóa, bạn có thể chọn mặc định (`RSA and RSA`), độ dài khóa (2048 bit hoặc 4096 bit là phổ biến), và thời hạn khóa (hoặc để trống nếu bạn không muốn khóa hết hạn).

### Bước 3: Liệt kê các khóa GPG của bạn

Sau khi tạo khóa, liệt kê các khóa để tìm ID của khóa mà bạn muốn sử dụng:

```bash
gpg --list-secret-keys --keyid-format LONG
```

Bạn sẽ thấy một dòng có dạng như thế này:

```
/home/user/.gnupg/secring.gpg
------------------------------
sec   rsa4096/XXXXXXXXXXXXXXXX 2024-08-19 [SC]
```

Sao chép ID khóa (`XXXXXXXXXXXXXXXX`) của bạn.

### Bước 4: Xuất public key của bạn và thêm vào GitHub

Xuất public key của bạn:

```bash
gpg --armor --export XXXXXXXXXXXXXXXX
```

Sao chép toàn bộ kết quả của lệnh này (bao gồm cả phần `-----BEGIN PGP PUBLIC KEY BLOCK-----` và `-----END PGP PUBLIC KEY BLOCK-----`).

Tiếp theo, đăng nhập vào GitHub và làm theo các bước sau:

1. Vào phần [SSH and GPG keys](https://github.com/settings/keys) trong thiết lập tài khoản của bạn.
2. Nhấp vào "New GPG key".
3. Dán public key đã sao chép vào ô và nhấn "Add GPG key".

### Bước 5: Cấu hình Git để ký commit tự động

Cấu hình Git để sử dụng khóa GPG của bạn cho tất cả các commit:

```bash
git config --global user.signingkey XXXXXXXXXXXXXXXX
git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
git config --global user.email "new-email@example.com"
```

Bạn có thể cấu hình Git để tự động ký tất cả các commit:

```bash
git config --global commit.gpgSign true
```

### Bước 6: Thực hiện commit đã ký

Khi bạn thực hiện commit, Git sẽ tự động ký commit của bạn với khóa GPG:

```bash
git commit -m "Commit message"
```

Nếu bạn chưa bật ký commit tự động, bạn có thể ký commit thủ công bằng cách sử dụng flag `-S`:

```bash
git commit -S -m "Commit đã ký"
```

### Bước 7: Đẩy commit lên GitHub

Cuối cùng, đẩy commit đã ký của bạn lên GitHub:

```bash
git push origin <branch-name>
```

Trên GitHub, commit của bạn sẽ hiển thị với dấu "Verified", xác nhận rằng commit đó đã được ký hợp lệ.