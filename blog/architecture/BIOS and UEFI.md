# Hiểu Rõ Về BIOS và UEFI: Khái Niệm, Cách Hoạt Động, và So Sánh

## 1. Giới Thiệu

BIOS (Basic Input/Output System) và UEFI (Unified Extensible Firmware Interface) là hai loại firmware được sử dụng trong máy tính để khởi động hệ thống và quản lý các thiết lập cơ bản. Trong bài viết này, chúng ta sẽ đi sâu vào cấu trúc, chức năng của BIOS và UEFI, cũng như so sánh chúng để hiểu rõ hơn về sự khác biệt và lợi ích của từng loại.

## 2. BIOS là gì?

**BIOS** là một chương trình firmware được lưu trữ trên một chip ROM trên bo mạch chủ. Nó là phần mềm đầu tiên được kích hoạt khi bạn bật máy tính, với nhiệm vụ kiểm tra và khởi tạo các thành phần phần cứng như CPU, RAM, bàn phím, chuột, và ổ cứng.

### 2.1. Quá Trình Hoạt Động của BIOS

- **Power-On Self Test (POST):** BIOS bắt đầu quá trình khởi động bằng cách thực hiện POST, một loạt các kiểm tra để đảm bảo rằng phần cứng hoạt động bình thường.
- **Khởi tạo phần cứng:** Sau POST, BIOS khởi tạo các thiết bị phần cứng như bộ nhớ, bộ điều khiển lưu trữ, và các thiết bị ngoại vi.
- **MBR và Bootloader:** Sau khi hoàn thành khởi tạo phần cứng, BIOS tìm và tải MBR (Master Boot Record) từ ổ cứng chính. MBR chứa bootloader, giúp khởi động hệ điều hành.

### 2.2. MBR (Master Boot Record)

**MBR** là một cấu trúc dữ liệu nhỏ nằm ở đầu của một ổ đĩa lưu trữ. Nó chứa bảng phân vùng (partition table) của ổ đĩa và một mã khởi động nhỏ (boot code). MBR có một số hạn chế:

- **Giới hạn phân vùng:** Chỉ hỗ trợ tối đa 4 phân vùng chính (primary partitions) trên mỗi ổ đĩa.
- **Giới hạn kích thước:** Hỗ trợ tối đa 2TB cho mỗi ổ đĩa.

## 3. UEFI là gì?

**UEFI** là phiên bản nâng cấp của BIOS, với giao diện người dùng đồ họa và các tính năng tiên tiến hơn. Nó được lưu trữ trong một file có thể nằm trên chip flash trên bo mạch chủ hoặc trong thư mục đặc biệt trên ổ đĩa.

### 3.1. Quá Trình Hoạt Động của UEFI

- **UEFI Boot Manager:** UEFI quản lý các quy trình khởi động qua một UEFI Boot Manager, giúp linh hoạt hơn trong việc quản lý nhiều hệ điều hành.
- **GPT (GUID Partition Table):** UEFI sử dụng GPT thay cho MBR, hỗ trợ số lượng phân vùng và kích thước ổ đĩa lớn hơn.
- **Secure Boot:** Tính năng này giúp ngăn chặn phần mềm độc hại khởi động trước hệ điều hành.

### 3.2. GPT (GUID Partition Table)

**GPT** là một phần của chuẩn UEFI để thay thế MBR. Nó cung cấp một số lợi ích:

- **Hỗ trợ nhiều phân vùng:** GPT có thể hỗ trợ lên đến 128 phân vùng.
- **Không giới hạn kích thước ổ đĩa:** GPT không bị giới hạn bởi kích thước ổ đĩa, cho phép sử dụng ổ đĩa lớn hơn 2TB.

## 4. So Sánh BIOS và UEFI

| **Tiêu chí**            | **BIOS**                       | **UEFI**                        |
|-------------------------|--------------------------------|----------------------------------|
| **Công nghệ lưu trữ**    | ROM (Read-Only Memory)         | Chip flash hoặc ổ đĩa           |
| **Giao diện người dùng** | Dòng lệnh (text-based)         | Đồ họa (graphical)              |
| **Hỗ trợ ổ đĩa**         | Lên đến 2TB với MBR            | Không giới hạn với GPT          |
| **Số phân vùng tối đa**  | 4 phân vùng chính              | 128 phân vùng                   |
| **Tính năng bảo mật**    | Không hỗ trợ                   | Có Secure Boot                  |
| **Khả năng khởi động**   | Từ ổ đĩa và thiết bị lưu trữ    | Từ nhiều nguồn bao gồm mạng, USB|
| **Khả năng mở rộng**     | Hạn chế, khó mở rộng           | Dễ dàng mở rộng với drivers và phần mềm |

## 5. Kết Luận

BIOS và UEFI đều đóng vai trò quan trọng trong quá trình khởi động máy tính, nhưng UEFI mang lại nhiều tính năng và ưu điểm hơn, đặc biệt là trong việc hỗ trợ các công nghệ phần cứng mới và bảo mật. Tuy nhiên, BIOS vẫn còn được sử dụng rộng rãi trong các hệ thống cũ. Việc hiểu rõ sự khác biệt giữa chúng giúp bạn lựa chọn phù hợp cho hệ thống của mình, đặc biệt khi xây dựng hoặc nâng cấp máy tính.

---

Bạn có thể tham khảo thêm về cách cấu hình BIOS hoặc UEFI trong phần thiết lập của bo mạch chủ để tùy chỉnh cho phù hợp với nhu cầu sử dụng của mình.