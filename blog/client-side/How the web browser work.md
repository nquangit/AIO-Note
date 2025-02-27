### Cách Trình Duyệt Web Hoạt Động

#### 1. **Giới Thiệu**
Mỗi khi chúng ta nhấp vào một liên kết trên trình duyệt web, hàng loạt quá trình phức tạp xảy ra trong hậu trường để đưa chúng ta từ một trang web này đến một trang web khác. Mặc dù chỉ diễn ra trong vài giây, nhưng những gì xảy ra trong khoảng thời gian đó rất đáng chú ý. Bài viết này sẽ giúp bạn hiểu rõ hơn về cách một trình duyệt hoạt động khi người dùng mở một liên kết, từ việc giải quyết DNS, thiết lập kết nối, tải tài nguyên, đến hiển thị nội dung.

#### 2. **Giai Đoạn 1: Phân Giải DNS**
Khi bạn nhấp vào một liên kết, trình duyệt sẽ cần biết địa chỉ IP của máy chủ mà liên kết đó trỏ tới. Quá trình này được gọi là phân giải DNS (Domain Name System). (Bạn có thể đọc bài viết chi tiết về DNS ở đây [Hiểu về DNS & Cách Máy Tính Làm Việc với Hệ Thống Tên Miền](https://hackmd.io/@nquangit/how-dns-work))

- **Bước 1: Trình duyệt kiểm tra bộ nhớ đệm cục bộ (local cache)**: Đầu tiên, trình duyệt sẽ kiểm tra xem địa chỉ IP của tên miền đã có sẵn trong bộ nhớ đệm của máy tính hay không. Nếu có, quá trình phân giải DNS sẽ được bỏ qua.
- **Bước 2: Kiểm tra bộ nhớ đệm của hệ điều hành**: Nếu trình duyệt không tìm thấy địa chỉ IP trong bộ nhớ đệm của nó, nó sẽ yêu cầu hệ điều hành kiểm tra bộ nhớ đệm của chính nó.
- **Bước 3: Gửi yêu cầu đến máy chủ DNS**: Nếu địa chỉ IP vẫn chưa được tìm thấy, yêu cầu phân giải DNS sẽ được gửi đến máy chủ DNS của nhà cung cấp dịch vụ internet (ISP) hoặc máy chủ DNS mà người dùng đã cấu hình.

Máy chủ DNS sẽ tra cứu địa chỉ IP của tên miền, nếu cần thiết, nó có thể chuyển tiếp yêu cầu đến các máy chủ DNS khác theo một chuỗi phân cấp cho đến khi tìm thấy địa chỉ IP chính xác.

#### 3. **Giai Đoạn 2: Thiết Lập Kết Nối**
Sau khi có địa chỉ IP của máy chủ đích, trình duyệt sẽ bắt đầu quá trình thiết lập kết nối.

- **Bước 1: Thiết lập kết nối TCP**: Trình duyệt sẽ thiết lập một kết nối TCP (Transmission Control Protocol) với máy chủ thông qua quá trình bắt tay ba bước (three-way handshake):
  1. **SYN**: Trình duyệt gửi một gói tin SYN (Synchronize) đến máy chủ để bắt đầu quá trình kết nối.
  2. **SYN-ACK**: Máy chủ phản hồi bằng một gói tin SYN-ACK (Synchronize-Acknowledge) để đồng ý kết nối.
  3. **ACK**: Trình duyệt gửi một gói tin ACK (Acknowledge) để xác nhận kết nối đã được thiết lập.

- **Bước 2: Thiết lập kết nối SSL/TLS (nếu là HTTPS)**: Nếu liên kết sử dụng HTTPS, sau khi kết nối TCP được thiết lập, trình duyệt và máy chủ sẽ thiết lập một kết nối bảo mật thông qua SSL/TLS. Quá trình này bao gồm:
  - **Xác thực máy chủ**: Máy chủ gửi chứng chỉ số cho trình duyệt để xác thực danh tính của mình.
  - **Trao đổi khóa mã hóa**: Sau khi xác thực, hai bên sẽ trao đổi khóa mã hóa và thiết lập một kênh truyền thông mã hóa.

#### 4. **Giai Đoạn 3: Gửi Yêu Cầu HTTP/HTTPS**
Với kết nối đã được thiết lập, trình duyệt sẽ gửi yêu cầu HTTP hoặc HTTPS đến máy chủ.

- **Bước 1: Tạo yêu cầu HTTP**: Trình duyệt tạo ra một yêu cầu HTTP bao gồm:
  - **Method**: Phương thức yêu cầu (thường là GET hoặc POST).
  - **URL**: Đường dẫn cụ thể trên máy chủ mà yêu cầu sẽ truy cập.
  - **Headers**: Các thông tin bổ sung như loại trình duyệt, ngôn ngữ, cookie, v.v.
  
- **Bước 2: Gửi yêu cầu**: Yêu cầu HTTP/HTTPS được gửi đến máy chủ qua kết nối TCP hoặc SSL/TLS.

#### 5. **Giai Đoạn 4: Máy Chủ Xử Lý Yêu Cầu**
Khi nhận được yêu cầu từ trình duyệt, máy chủ sẽ xử lý và phản hồi.

- **Bước 1: Máy chủ xử lý yêu cầu**: Máy chủ sẽ xác định nội dung yêu cầu, có thể truy vấn cơ sở dữ liệu, chạy các đoạn mã xử lý hoặc lấy tài nguyên tĩnh từ hệ thống tệp.
  
- **Bước 2: Tạo phản hồi HTTP**: Máy chủ tạo ra một phản hồi HTTP, bao gồm:
  - **Status code**: Mã trạng thái phản hồi (như 200 OK, 404 Not Found).
  - **Headers**: Thông tin bổ sung như loại nội dung, kích thước nội dung, thời gian cache, v.v.
  - **Body**: Nội dung phản hồi, có thể là HTML, JSON, hình ảnh, v.v.

- **Bước 3: Gửi phản hồi**: Phản hồi HTTP được gửi trở lại trình duyệt qua kết nối TCP hoặc SSL/TLS.

#### 6. **Giai Đoạn 5: Trình Duyệt Xử Lý Phản Hồi**
Sau khi nhận được phản hồi từ máy chủ, trình duyệt sẽ bắt đầu quá trình xử lý và hiển thị nội dung.

- **Bước 1: Phân tích nội dung HTML**: Trình duyệt bắt đầu phân tích cú pháp (parsing) nội dung HTML, tạo ra một cây DOM (Document Object Model) để biểu diễn cấu trúc của trang web.
  
- **Bước 2: Tải các tài nguyên bổ sung**: Trong quá trình phân tích HTML, nếu trình duyệt phát hiện các tài nguyên bổ sung như CSS, JavaScript, hình ảnh, font chữ, nó sẽ gửi các yêu cầu HTTP bổ sung để tải chúng về.
  
- **Bước 3: Xử lý CSS và JavaScript**: Trình duyệt tải và xử lý CSS để áp dụng các `style` vào cây DOM. JavaScript sẽ được tải và thực thi để điều khiển hành vi của trang web.
  
- **Bước 4: Tạo cây kết xuất (Render Tree)**: Trình duyệt kết hợp cây DOM và CSSOM (CSS Object Model) để tạo ra cây kết xuất, sau đó sẽ được sử dụng để hiển thị nội dung trang web.
  
- **Bước 5: Hiển thị nội dung**: Trình duyệt bắt đầu hiển thị nội dung trên màn hình, liên tục cập nhật khi các tài nguyên bổ sung được tải về và các đoạn mã JavaScript được thực thi.

#### 7. **Kết Luận**
Quá trình từ lúc bạn nhấp vào một liên kết cho đến khi trang web được hiển thị trên màn hình bao gồm nhiều giai đoạn phức tạp, từ phân giải DNS, thiết lập kết nối, gửi và nhận dữ liệu HTTP, đến việc xử lý và hiển thị nội dung. Hiểu được các bước này không chỉ giúp bạn biết thêm về cách trình duyệt hoạt động mà còn cung cấp cho bạn những kiến thức cần thiết để tối ưu hóa và bảo mật ứng dụng web của mình.
