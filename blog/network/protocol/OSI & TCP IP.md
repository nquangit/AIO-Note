# Mô hình OSI và mô hình TCP/IP

## 1. Giới thiệu về Mô hình OSI

Mô hình OSI (Open Systems Interconnection) là một khung tham chiếu lý thuyết được phát triển bởi Tổ chức Tiêu chuẩn Quốc tế (ISO) nhằm chuẩn hóa các giao thức truyền thông trong mạng máy tính. Mô hình này chia quá trình giao tiếp thành bảy lớp, mỗi lớp có một chức năng cụ thể. Các lớp từ thấp đến cao bao gồm:

### 1.1. Lớp Vật lý (Physical Layer)
- **Chức năng:** Chịu trách nhiệm truyền tải các bit dữ liệu qua môi trường truyền thông vật lý như dây cáp, sóng vô tuyến.
- **Địa chỉ:** Không có.
- **Tiêu chuẩn:** IEEE 802.3 (Ethernet), ITU-T G.703 (Digital Carriers).
- **Giao thức:** Không có, vì lớp này chỉ liên quan đến phần cứng và tín hiệu.

### 1.2. Lớp Liên kết dữ liệu (Data Link Layer)
- **Chức năng:** Đảm bảo truyền dữ liệu chính xác từ một nút mạng này đến nút mạng khác.
- **Địa chỉ:** Địa chỉ MAC.
- **Tiêu chuẩn:** IEEE 802.2, IEEE 802.11 (Wi-Fi).
- **Giao thức:** Ethernet, PPP (Point-to-Point Protocol), ARP (Address Resolution Protocol).

### 1.3. Lớp Mạng (Network Layer)
- **Chức năng:** Định tuyến và chuyển tiếp các gói dữ liệu giữa các mạng khác nhau.
- **Địa chỉ:** Địa chỉ IP.
- **Tiêu chuẩn:** IPv4, IPv6.
- **Giao thức:** IP, ICMP (Internet Control Message Protocol), RIP (Routing Information Protocol).

### 1.4. Lớp Giao vận (Transport Layer)
- **Chức năng:** Đảm bảo dữ liệu được truyền tải từ nguồn đến đích một cách đáng tin cậy.
- **Địa chỉ:** Số cổng (Port Number).
- **Tiêu chuẩn:** TCP (Transmission Control Protocol), UDP (User Datagram Protocol).
- **Giao thức:** TCP, UDP.

### 1.5. Lớp Phiên (Session Layer)
- **Chức năng:** Quản lý các phiên giao tiếp giữa hai máy tính.
- **Địa chỉ:** Không có.
- **Tiêu chuẩn:** Không có tiêu chuẩn cụ thể.
- **Giao thức:** NetBIOS, PPTP (Point-to-Point Tunneling Protocol).

### 1.6. Lớp Trình bày (Presentation Layer)
- **Chức năng:** Chuyển đổi dữ liệu giữa định dạng ứng dụng và định dạng mạng.
- **Địa chỉ:** Không có.
- **Tiêu chuẩn:** Không có tiêu chuẩn cụ thể.
- **Giao thức:** SSL/TLS (Secure Sockets Layer/Transport Layer Security), JPEG, MPEG.

### 1.7. Lớp Ứng dụng (Application Layer)
- **Chức năng:** Cung cấp giao diện giữa phần mềm ứng dụng và mạng.
- **Địa chỉ:** Không có.
- **Tiêu chuẩn:** HTTP, FTP, SMTP.
- **Giao thức:** DNS (Domain Name System), HTTP (HyperText Transfer Protocol), FTP (File Transfer Protocol).

## 2. Giới thiệu về Mô hình TCP/IP

Mô hình TCP/IP (Transmission Control Protocol/Internet Protocol) là một bộ giao thức được phát triển để hỗ trợ mạng Internet. Không như mô hình OSI, TCP/IP chỉ có bốn lớp:

1. **Lớp Truy cập mạng (Network Access Layer)**
2. **Lớp Internet (Internet Layer)**
3. **Lớp Giao vận (Transport Layer)**
4. **Lớp Ứng dụng (Application Layer)**

### 2.1. Lớp Truy cập mạng (Network Access Layer)
- **Chức năng:** Xử lý việc truy cập vào môi trường vật lý và việc định dạng dữ liệu để truyền đi.
- **Địa chỉ:** Địa chỉ MAC.
- **Tiêu chuẩn:** Ethernet, Wi-Fi.
- **Giao thức:** Ethernet, ARP.

### 2.2. Lớp Internet (Internet Layer)
- **Chức năng:** Định tuyến gói tin đến đúng địa chỉ IP trong mạng.
- **Địa chỉ:** Địa chỉ IP.
- **Tiêu chuẩn:** IPv4, IPv6.
- **Giao thức:** IP, ICMP.

### 2.3. Lớp Giao vận (Transport Layer)
- **Chức năng:** Đảm bảo truyền tải dữ liệu một cách tin cậy giữa các thiết bị.
- **Địa chỉ:** Số cổng (Port Number).
- **Tiêu chuẩn:** TCP, UDP.
- **Giao thức:** TCP, UDP.

### 2.4. Lớp Ứng dụng (Application Layer)
- **Chức năng:** Tương tác trực tiếp với người dùng và các ứng dụng mạng.
- **Địa chỉ:** Không có.
- **Tiêu chuẩn:** HTTP, FTP, SMTP.
- **Giao thức:** HTTP, FTP, DNS.

## 3. So sánh Mô hình OSI và TCP/IP

| **Tiêu chí**                 | **Mô hình OSI**                           | **Mô hình TCP/IP**                      |
|------------------------------|-------------------------------------------|-----------------------------------------|
| **Số lớp**                   | 7 lớp                                     | 4 lớp                                   |
| **Độ phổ biến**              | Mang tính lý thuyết, ít được triển khai trực tiếp | Được sử dụng phổ biến trên Internet     |
| **Khả năng mở rộng**         | Khả năng mở rộng cao nhờ cấu trúc chia nhỏ thành 7 lớp | Khả năng mở rộng hạn chế hơn            |
| **Giao thức**                | Được xác định rõ ràng cho từng lớp        | Không xác định rõ ràng, giao thức có thể hoạt động trên nhiều lớp |
| **Tính tương tác**           | Tính tương tác giữa các lớp được định nghĩa rõ ràng | Tính tương tác giữa các lớp không rõ ràng |
| **Địa chỉ sử dụng**          | Địa chỉ MAC, Địa chỉ IP, Số cổng          | Địa chỉ MAC, Địa chỉ IP, Số cổng        |

## 4. Kết luận

Mô hình OSI và TCP/IP đều là những khung lý thuyết quan trọng giúp chuẩn hóa các hoạt động truyền thông trong mạng máy tính. Trong khi mô hình OSI chủ yếu mang tính lý thuyết và phân chia rõ ràng thành 7 lớp, thì mô hình TCP/IP được phát triển để thực tế hơn và được sử dụng rộng rãi trên Internet. Việc hiểu rõ cả hai mô hình này là rất cần thiết để nắm bắt cách hoạt động của mạng máy tính hiện đại.