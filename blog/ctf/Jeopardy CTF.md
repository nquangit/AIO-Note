# Jeopardy CTF

Jeopardy-style Capture The Flag (CTF) là một hình thức thi đấu bảo mật phổ biến, trong đó người chơi giải quyết các thử thách khác nhau để kiếm điểm. Các thử thách này thường được chia thành nhiều thể loại, mỗi thể loại yêu cầu kỹ năng và công cụ khác nhau. Dưới đây là một cái nhìn chi tiết về các thể loại thử thách phổ biến trong Jeopardy CTF, cùng với các kỹ năng cần thiết, công cụ và tài nguyên hữu ích.

---

## 1. **Web Exploitation**
Web Exploitation là một thể loại thử thách phổ biến trong Jeopardy CTF, tập trung vào khai thác các lỗ hổng bảo mật trong các ứng dụng web.

- **Kỹ năng cần thiết:**
  - Hiểu biết về các lỗ hổng web phổ biến như SQL Injection, Cross-Site Scripting (XSS), Command Injection, Directory Traversal, và các lỗ hổng liên quan đến quản lý phiên (Session Management).
  - Kiến thức về các giao thức HTTP/HTTPS, các phương thức HTTP (GET, POST, PUT, DELETE), và cách hoạt động của ứng dụng web.
  - Kỹ năng đọc và phân tích mã nguồn, đặc biệt là mã PHP, JavaScript, và các ngôn ngữ phổ biến khác trong phát triển web.

- **Công cụ:**
  - **Burp Suite**: Một bộ công cụ tích hợp cho việc kiểm thử bảo mật web, hỗ trợ phát hiện và khai thác các lỗ hổng web.
  - **OWASP ZAP**: Một công cụ mã nguồn mở cho việc tìm kiếm các lỗ hổng bảo mật web.
  - **SQLMap**: Một công cụ tự động hóa quá trình phát hiện và khai thác lỗ hổng SQL Injection.
  - **WFuzz**: Một công cụ fuzzing để kiểm thử ứng dụng web.

- **Tài nguyên hữu ích:**
  - **OWASP Top 10**: Danh sách các lỗ hổng bảo mật web phổ biến nhất do OWASP phát hành.
  - **PortSwigger Web Security Academy**: Nền tảng học tập miễn phí với các bài học và bài tập thực hành về bảo mật web.

## 2. **Reverse Engineering**
Reverse Engineering là thể loại thử thách yêu cầu người chơi phân tích ngược một chương trình để hiểu cách thức hoạt động của nó hoặc tìm ra cách vượt qua các biện pháp bảo mật.

- **Kỹ năng cần thiết:**
  - Hiểu biết về ngôn ngữ lập trình cấp thấp như Assembly.
  - Kỹ năng phân tích mã máy và mã nguồn.
  - Kỹ năng sử dụng các công cụ dịch ngược và gỡ lỗi.

- **Công cụ:**
  - **IDA Pro** hoặc **Ghidra**: Công cụ dịch ngược mã nguồn mạnh mẽ, hỗ trợ nhiều kiến trúc và định dạng tệp.
  - **OllyDbg** hoặc **x64dbg**: Trình gỡ lỗi mạnh mẽ cho các hệ thống Windows.
  - **Binary Ninja**: Một công cụ phân tích nhị phân khác, thân thiện với người dùng hơn nhưng cũng rất mạnh mẽ.

- **Tài nguyên hữu ích:**
  - **"Practical Reverse Engineering"**: Một cuốn sách nổi tiếng trong lĩnh vực phân tích mã nguồn và khai thác lỗ hổng.
  - **"Reversing: Secrets of Reverse Engineering"**: Một cuốn sách cung cấp nền tảng và kiến thức sâu rộng về Reverse Engineering.

## 3. **Forensics**
Forensics tập trung vào việc phân tích dữ liệu số để tìm ra thông tin ẩn, truy vết hành vi hoặc khôi phục dữ liệu bị xóa.

- **Kỹ năng cần thiết:**
  - Kỹ năng phân tích tập tin, hệ thống tệp, và các định dạng dữ liệu khác nhau.
  - Hiểu biết về hệ điều hành, đặc biệt là cách chúng quản lý tập tin và bộ nhớ.
  - Kỹ năng đọc và phân tích nhật ký (log files) và lưu lượng mạng.

- **Công cụ:**
  - **Autopsy**: Một giao diện đồ họa cho công cụ phân tích pháp lý The Sleuth Kit.
  - **Wireshark**: Công cụ phân tích lưu lượng mạng mạnh mẽ, hỗ trợ nhiều giao thức.
  - **Binwalk**: Công cụ phân tích tập tin firmware, tìm kiếm và trích xuất các nội dung ẩn.

- **Tài nguyên hữu ích:**
  - **"The Art of Memory Forensics"**: Cuốn sách chi tiết về kỹ thuật phân tích bộ nhớ trong bảo mật số.
  - **Digital Forensics and Incident Response (DFIR)**: Cộng đồng và tài nguyên hữu ích về phân tích pháp lý số.

## 4. **Cryptography**
Cryptography yêu cầu người chơi giải mã các thông điệp mã hóa hoặc phá vỡ các thuật toán mã hóa.

- **Kỹ năng cần thiết:**
  - Kiến thức về các thuật toán mã hóa cổ điển và hiện đại, như Caesar Cipher, RSA, AES, và các hệ mật khóa công khai và đối xứng.
  - Hiểu biết về lý thuyết số, đặc biệt là số nguyên tố, mod, và các phép toán số học cơ bản trong mật mã.
  - Kỹ năng lập trình để triển khai và phá vỡ các thuật toán mã hóa.

- **Công cụ:**
  - **CyberChef**: Một công cụ trực tuyến cho phép thực hiện nhiều phép biến đổi và phân tích dữ liệu, đặc biệt hữu ích cho việc giải mã.
  - **John the Ripper**: Công cụ bẻ khóa mật khẩu phổ biến, hỗ trợ nhiều định dạng mật khẩu.
  - **Hashcat**: Công cụ bẻ khóa mật mã mạnh mẽ, hỗ trợ GPU acceleration.

- **Tài nguyên hữu ích:**
  - **Cryptopals**: Một bộ sưu tập các thử thách về mật mã, cung cấp kiến thức từ cơ bản đến nâng cao.
  - **"Cryptography and Network Security"**: Cuốn sách học thuật cung cấp nền tảng vững chắc về lý thuyết và ứng dụng của mật mã.

## 5. **Binary Exploitation (Pwn)**
Binary Exploitation tập trung vào việc khai thác các lỗ hổng trong phần mềm, thường là lỗi tràn bộ đệm (Buffer Overflow) hoặc lỗi quản lý bộ nhớ.

- **Kỹ năng cần thiết:**
  - Hiểu biết về cách hoạt động của bộ nhớ, quản lý ngăn xếp và heap trong các chương trình.
  - Kỹ năng lập trình bằng các ngôn ngữ như C, C++, và Assembly.
  - Kỹ năng sử dụng các kỹ thuật khai thác như Return-Oriented Programming (ROP) và Format String Exploitation.

- **Công cụ:**
  - **Pwntools**: Một thư viện Python hỗ trợ viết khai thác một cách nhanh chóng và dễ dàng.
  - **GDB**: Trình gỡ lỗi GNU Debugger, thường được sử dụng để phân tích và khai thác chương trình.
  - **ROPgadget**: Công cụ tìm kiếm các chuỗi lệnh cần thiết để xây dựng ROP chain.

- **Tài nguyên hữu ích:**
  - **"Hacking: The Art of Exploitation"**: Cuốn sách cung cấp kiến thức về khai thác lỗ hổng phần mềm, từ cơ bản đến nâng cao.
  - **CTF pwn challenges**: Các thử thách CTF về Pwn thường có trên các nền tảng như CTFtime, là nơi tuyệt vời để thực hành kỹ năng khai thác.

## 6. **Miscellaneous (Misc)**
Miscellaneous là thể loại thử thách không thuộc vào các danh mục truyền thống và thường yêu cầu sự sáng tạo và khả năng tư duy ngoài khuôn khổ.

- **Kỹ năng cần thiết:**
  - Tư duy sáng tạo và khả năng suy luận.
  - Kỹ năng tìm kiếm thông tin và giải quyết vấn đề từ nhiều góc độ khác nhau.
  - Khả năng đọc và hiểu mã nguồn và tài liệu trong nhiều ngôn ngữ lập trình khác nhau.

- **Công cụ:**
  - **Google và các công cụ tìm kiếm**: Đôi khi, câu trả lời có thể nằm ở một tài liệu hay bài viết trực tuyến.
  - **Stegsolve**: Công cụ hỗ trợ phân tích steganography và các tập tin hình ảnh.
  - **Strings**: Công cụ để tìm kiếm các chuỗi văn bản ẩn trong các tệp nhị phân.

- **Tài nguyên hữu ích:**
  - **CTF Writeups**: Tham khảo các bài viết giải thích cách giải quyết các thử thách tương tự từ những người chơi khác.
  - **Miscellaneous CTF challenges**: Thực hành trực tiếp trên các nền tảng CTF trực tuyến.

---

# Lời Kết
Tham gia Jeopardy CTF là một cách tuyệt vời để phát triển và rèn luyện kỹ năng bảo mật. Mỗi thể loại thử thách đều yêu cầu một bộ kỹ năng riêng, nhưng tất cả đều đóng góp vào việc tạo nên một chuyên gia bảo mật toàn diện. Hãy không ngừng học hỏi, thực hành, và sử dụng các công cụ và tài nguyên phù hợp để nâng cao kiến thức và kĩ năng về bảo mật.

