# Các Giao Thức Ở Layer 4 Mô Hình OSI

Mô hình OSI (Open Systems Interconnection) là một khung lý thuyết giúp chuẩn hóa cách các hệ thống máy tính giao tiếp qua mạng. Trong mô hình OSI, Layer 4, hay còn gọi là **Transport Layer (Lớp Vận Chuyển)**, chịu trách nhiệm quản lý các kết nối mạng và đảm bảo dữ liệu được truyền một cách chính xác giữa các ứng dụng trên hai hệ thống khác nhau. Layer 4 cung cấp các dịch vụ truyền tải tin cậy và không tin cậy, và bao gồm nhiều giao thức quan trọng. Dưới đây là một cái nhìn chi tiết về các giao thức chính ở Layer 4 của mô hình OSI.

#### 1. **Transmission Control Protocol (TCP)**

**TCP** là giao thức kết nối và tin cậy. Nó cung cấp một kênh truyền thông ổn định giữa hai máy tính, đảm bảo rằng tất cả các gói tin dữ liệu được gửi đi và nhận về đúng thứ tự và không bị mất mát. Các đặc điểm chính của TCP bao gồm:

- **Kết nối:** TCP thiết lập một kết nối trước khi truyền dữ liệu. Quy trình này gọi là bắt tay ba bước (three-way handshake).
- **Tin cậy:** TCP cung cấp khả năng phát hiện lỗi và yêu cầu truyền lại dữ liệu nếu phát hiện có lỗi.
- **Điều chỉnh luồng:** TCP điều chỉnh tốc độ truyền dữ liệu để phù hợp với khả năng xử lý của máy nhận, nhằm tránh quá tải.
- **Quản lý lưu lượng:** TCP sử dụng các cơ chế như điều chỉnh tốc độ để kiểm soát lưu lượng dữ liệu.

**Ứng dụng:** TCP được sử dụng rộng rãi trong các ứng dụng yêu cầu độ tin cậy cao, chẳng hạn như web browsing (HTTP/HTTPS), email (SMTP, POP3, IMAP), và truyền tải tệp (FTP).

#### 2. **User Datagram Protocol (UDP)**

**UDP** là giao thức không kết nối và không tin cậy. Nó cung cấp một phương thức truyền dữ liệu nhanh hơn so với TCP nhưng không đảm bảo rằng dữ liệu sẽ đến đúng đích hoặc đúng thứ tự. Các đặc điểm chính của UDP bao gồm:

- **Không kết nối:** UDP gửi dữ liệu mà không thiết lập kết nối trước với máy nhận.
- **Không tin cậy:** UDP không cung cấp cơ chế phát hiện lỗi hoặc yêu cầu truyền lại dữ liệu.
- **Tốc độ cao:** Do không có overhead cho việc thiết lập kết nối và xác nhận dữ liệu, UDP thường có tốc độ truyền tải cao hơn TCP.

**Ứng dụng:** UDP thích hợp cho các ứng dụng yêu cầu tốc độ cao và có thể chấp nhận mất mát dữ liệu như video streaming, gaming, và truyền thông tin thời gian thực (VoIP).

#### 3. **Stream Control Transmission Protocol (SCTP)**

**SCTP** là một giao thức vận chuyển đa mục đích kết hợp các đặc điểm của TCP và UDP. Nó hỗ trợ nhiều luồng và nhiều kết nối trong một phiên kết nối duy nhất. Các đặc điểm chính của SCTP bao gồm:

- **Kết nối và tin cậy:** Giống như TCP, SCTP đảm bảo rằng dữ liệu được gửi đến đúng đích và không bị mất mát.
- **Đa luồng:** SCTP cho phép truyền dữ liệu đồng thời qua nhiều luồng trong cùng một kết nối, giúp giảm thiểu tắc nghẽn.
- **Đa đích:** SCTP hỗ trợ gửi dữ liệu đến nhiều địa chỉ đích khác nhau trong cùng một phiên kết nối, giúp cải thiện khả năng chịu lỗi.

**Ứng dụng:** SCTP được sử dụng trong các ứng dụng yêu cầu tính tin cậy cao và khả năng xử lý đồng thời nhiều luồng dữ liệu, chẳng hạn như truyền thông viễn thông và mạng lõi.

#### Ngoài ra: **Protocol Data Units (PDUs)**

Ở Layer 4, các giao thức sử dụng **Protocol Data Units (PDUs)** để truyền dữ liệu qua mạng. PDUs của Layer 4 bao gồm các thành phần chính sau:

- **Segment (TCP):** Trong TCP, một PDU được gọi là segment. Segment bao gồm phần dữ liệu và các thông tin điều khiển như số hiệu cổng nguồn và đích, số thứ tự, và mã kiểm tra lỗi.
- **Datagram (UDP):** Trong UDP, PDU được gọi là datagram. Datagram bao gồm phần dữ liệu và các thông tin điều khiển như số hiệu cổng nguồn và đích, và mã kiểm tra lỗi.

#### Kết Luận

Layer 4 của mô hình OSI đóng vai trò quan trọng trong việc quản lý việc truyền dữ liệu qua mạng. Các giao thức như TCP, UDP, và SCTP cung cấp các phương thức khác nhau để truyền dữ liệu, mỗi cái có ưu và nhược điểm riêng. Việc hiểu rõ các giao thức này giúp các kỹ sư mạng và các nhà phát triển ứng dụng chọn lựa giải pháp phù hợp nhất cho các yêu cầu truyền tải dữ liệu của mình.