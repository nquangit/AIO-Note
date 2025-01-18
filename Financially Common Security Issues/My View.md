# Time-of-Check-Time-of-Use (TOCTOU) and Race Condition Issues

> CWE: 367 and 557

Lỗ hổng khi ứng dụng kiểm tra tính khả dụng (trạng thái) của tài nguyên trước khi sử dụng, nhưng trạng thái bị thay đổi trong khoảng giữa (khoảng thời gian sau khi kiểm tra và thực hiện hành động). Làm mất hiệu lực của việc kiểm tra đó. 
Lỗi này thường xảy ra trên các ứng dụng đa luồng hay xử lý đồng thời -> Chia sẻ tài nguyên, truy cập tài nguyên đồng thời mà không có kiểm soát.

Trình tự của thời gian và thứ tự là điều rất quan trọng để đảm bảo các hệ thống tài chính. Có nhiều giao dịch tài chính dựa vào việc kiểm tra số dư và giá trị (theo thời gian thực) trước khi bắt đầu xử lý.
Nếu có sự chậm trễ, delay, hay cơ hội để sửa lại giá trị giữa các lần kiểm tra hoặc sự phối hợp trong việc quản lý tài nguyên không được triển khai đúng cùng với các giải pháp đa luồng thì có thể trở thành mục tiêu của việc thao túng logic ứng dụng, có thể vì mục đích kiếm tiền, hay mục đích tài chính khác.

Các case có thể xảy ra dùng để thao túng vấn đề này:
## 1. Chuyển tiền/điểm hoặc mua hàng cùng lúc

Đây là một lỗi thường xuyên gặp trong các ứng dụng thương mại điện tử cho phép lưu giữ số dư của người dùng và cho phép chuyển tiền hay mua hàng cùng lúc.

**Ví dụ:**
Một người dùng được xác thực với mội ứng dụng tài chính ở 2 thiết bị khác khau, và có một giao dịch được tạo ra để thực hiện chuyển tiền từ tài khoản `X` đến tài khoản `Y` với giá trị là `$100`.
Giả sử đoạn mã xử lý phía server như sau và tài khoản của người dùng đó có `$100`:

```C
if (amount <= account_balance) {
    account_balance = account_balance – amount
}
```

Và ở thiết bị đã được xác thực, đồng thời thực hiện 2 yêu cầu giao dịch giống nhau và đồng thời gửi lên yêu cầu đó. Và khi này có khả năng rằng dòng code số 1 `if` có thể xảy ra đồng thời, hoặc lệnh `if` được thực thi 2 lần trước khi lệnh trừ tiền (dòng 2) được thực hiện. Nên 2 cũng sẽ được thực thi 2 lần mặc dù không hợp lý về mặt logic. Như vậy người dùng có khả năng chuyển đi nhiều hơn lượng mà người dùng đang có (hay mức cho phép).

Vấn đề này có thể được khai thác thông qua việc viết một đoạn mã đơn giản chạy đa luồng và sử dụng nhiều phiên (session) hợp lệ từ cùng một người dùng (Ví dụ bằng cách mô phỏng các lần đăng nhập đồng thời trên nhiều thiết bị). Và thậm chí trong một số trường hợp chúng ta có thể thực hiện chỉ với duy nhất một phiên đăng nhập (khi chúng có thể được ứng dụng xử lý cùng lúc).

**Hậu quả:**
- Tuỳ vảo bản chất của ứng dụng có thể gây ra gian lận, thất thoát.
- Mở ra khả năng trộm cắp hoặc sử dụng số tiền một cách phi pháp
- Tạo ra cơ chế tiềm ẩn cho việc rửa tiền, và các hoạt động gian lận khác.

Vấn đề này có thể được phát hiện nhiều trong các ứng dụng tài chính, như ngân hàng cho phép chuyển khoản giữa nhiều tài khoản, trang web mua sắm cho phép mua nhiều mặt hàng cùng lúc, hoặc các trang web cho phép kiếm và chuyển điểm thưởng.

Thậm chí có một số ứng dụng còn ngăn việc làm tài khoản người dùng có giá trị âm bằng cách đổi giá trị về thành `0`. Nếu ở trong trường hợp như ví dụ trên, người dùng có thể kiếm thêm `$100`.
Các vấn đề tương tự cũng xảy ra đối với các mã phiếu giảm giá chỉ có thể được sử dụng 1 hay 2 lần. Do đó, có thể tác động và sử dụng mã/phiếu giảm giá nhiều hơn bằng cách khai thác vấn đề này.

## 2. Thay đổi đơn hàng sau khi thanh toán

Các ứng dụng cho phép người dùng thay đổi đơn hàng trong khi thanh toán cho một mặt hàng cũng có thể dễ bị tấn công khi không có xác minh nào ở cuối quy trình. Mặc dù Race Condition trong việc thay đổi giỏ hàng trong khi thanh toán đang được xử lý có vẻ hơi khó khăn, nhưng thường thì không cần thiết phải làm như vậy, đặc biệt nếu trang thanh toán không phải là một phần của ứng dụng mà là trang web của bên thứ ba hoặc mô-đun bên ngoài. Trong trường hợp này, đơn hàng có thể được thay đổi trong khi người dùng đang ở trang thanh toán và trước khi nhấp vào nút "thanh toán" để hoàn tất thanh toán. Việc thay đổi các mặt hàng trong giỏ hàng, phương thức giao hàng và địa chỉ gửi hàng, số lượng mặt hàng, v.v. có thể ảnh hưởng đến giá cuối cùng trong khi ứng dụng vẫn sử dụng mức giá rẻ hơn ban đầu.

**Trường hợp sau đây là ví dụ về lỗ hổng bảo mật này được phát hiện trên một trang web đang hoạt động:**

Một người dùng truy cập vào một trang web thương mại điện tử và tiến hành cho một mặt hàng giá rẻ vào trong giỏ hàng và tiến hành thanh toán. Sau đó người dùng đã đến trang thanh toán để tiến hành thanh toán cho mặt hàng (giá rẻ) đã chọn. Nhưng người dùng không thực hiện thanh toán ngay mà mở thêm một tab mới vào lại trang web chính trong cùng một cửa sổ (cùng một session token) và tiến hành thêm một vài món hàng khác vào giỏ hàng. Sau khi đã thêm các mặt hàng mới, người dùng này quay trở lại trang thanh toán và thực hiện thanh toán đơn hàng. Và sau khi hoàn tất thanh toán, tất cả các dơn hàng trong giỏ hàng đều được thanh toán trong biên lai cuối cùng. Người dùng có thể mua thêm các mặt hàng miễn phí trong khi chỉ trả tiền cho mặt hàng ban đầu.

Lỗ hổng này cũng có thể tồn tại trong quá trình gửi tiền khi ứng dụng có thể giữ số dư của người dùng.

Một case khác là một ứng dụng xác thực các giá trị đầu vào và lưu trữ chúng trong phiên bất kể kết quả xác thực. Trong trường hợp này, ứng dụng không chuyển sang giai đoạn tiếp theo khi giá trị đầu vào không hợp lệ. Tuy nhiên, nếu người dùng chuyển sang giai đoạn tiếp theo bằng cách cung cấp các giá trị hợp lệ, sau đó phát lại yêu cầu trước đó với các giá trị không hợp lệ, ứng dụng đã
lưu trữ các giá trị không hợp lệ trong phiên và không xác thực chúng nữa vì người dùng đã vượt qua giai đoạn đó. Điều này gây ra các vấn đề logic nghiêm trọng cho ứng dụng.

## 3. Thay đổi đơn hàng sau khi hoàn tất thanh toán

Việc cập nhật thông tin chi tiết trong đơn hàng đã hoàn tất, hóa đơn hoặc báo giá đã tạo có thể dẫn đến tổn thất tài chính.

Điều này có thể xảy ra khi ứng dụng không xác minh trạng thái của giao dịch đã hoàn tất. Do đó, bạn có thể thêm nhiều mặt hàng vào đơn hàng đã hoàn tất, sửa đổi các mặt hàng hiện có để lợi dụng ưu đãi hiện có hoặc thay đổi các chi tiết khác mà không phải trả thêm phí.

**Trường hợp sau đây là ví dụ về lỗ hổng bảo mật này được phát hiện trên một trang web đang hoạt động:**

Một chứng chỉ bảo hiểm đã được tạo cho một chiếc xe giá rẻ với thông tin sai để giảm chi phí bảo hiểm. Sau khi đơn hàng hoàn tất, các yêu cầu đã gửi trước đó đã được sửa đổi và phát lại để bỏ qua các lần kiểm tra được áp dụng nhằm xác định trạng thái của đơn xin bảo hiểm. Do đó, có thể thay đổi thông tin chi tiết trong chứng chỉ bảo hiểm đã thanh toán để bao gồm những chiếc xe đắt tiền hơn hoặc thay đổi thời hạn hết hạn mà không phải trả thêm phí.

# Thao túng tham số

> CWE: 20 , 691 , 693 , 179 , 345 , 807 , 115 , 133 , 166 , 167 , 168 , 171, 915

Thao tác tham số là một kỹ thuật quan trọng để khai thác nhiều vấn đề bảo mật được nêu trong bài báo này. Dưới đây chúng tôi thảo luận về các tham số thú vị nhất cần được xem xét và thử nghiệm trong quá trình đánh giá ứng dụng tài chính.

## 1. Thao túng giá

Đây là một bài kiểm tra quan trọng đối với bất kỳ ứng dụng thương mai điện tử nào mà người dùng có thể mua sản phẩm. Các ứng dụng thường gửi dữ liệu đơn hàng, giá đến các trang thanh toán, đặc biệt là khi những module thanh toán không phải là một phần của ứng dụng web mà được sử dụng từ một bên thứ 3 do đó không có khả năng truy cập và cơ sở dữ liệu hay phiên của người dùng để xác thực. Cũng có thể tìm thấy các ứng dụng gửi dữ liệu giá khi chọn một mặt hàng để thêm vào giỏ hàng.

Đôi khi có thể mua cùng một mặt hàng với giá rẻ hơn hoặc thậm chí miễn phí bằng cách thao túng giá của nó. Mặc dù hiện nay rất hiếm khi tìm thấy một ứng dụng chấp nhận số âm thông qua các trường giá, điều này luôn cần được kiểm tra vì nó có thể thay đổi hoàn toàn luồng ứng dụng.

**Real Case**

Cơ chế "thêm vào giỏ hàng" của trang thương mại điện tử có chứa tham số "giá" trong một trường ẩn, nhưng ứng dụng đã bỏ qua giá đã bị thao túng trong yêu cầu và thay vào đó sử dụng giá trị
đúng. Tuy nhiên, sau đó người ta phát hiện ra rằng bằng cách thêm một số mặt hàng giảm giá (mặt hàng có chiết khấu bổ sung) vào giỏ hàng, ứng dụng bắt đầu sử dụng tham số giá trong yêu cầu và
cho phép thao túng giá và giá trị âm (xem phần "Giá động, Giá có dung sai hoặc Chương trình giới thiệu" để biết thêm thông tin).

Đôi khi, khi ứng dụng được triển khai không tốt, có thể thay đổi giá trị giá trên lệnh gọi lại từ máy chủ thanh toán (thông qua trình duyệt của người dùng chứ không phải qua API phụ trợ). Trong trường hợp này, người dùng có thể thay đổi giá trước khi đến trang thanh toán và sau khi hoàn tất giao dịch, giá trong URL lệnh gọi lại sẽ được thay đổi để phản ánh giá trị ban đầu của nó. Sau đó, người dùng có thể yêu cầu hoàn lại tiền và nhận lại số tiền này. Mặc dù hiếm khi thấy một ứng dụng dễ bị tấn công như thế này ngày nay, nhưng luôn đáng để kiểm tra loại lỗ hổng này.

## 2. Thao túng loại tiền tệ

Mặc dù một trang web thương mại điện tử có thể không chấp nhận các loại tiền tệ khác nhau, nhưng các ứng dụng thanh toán thường chấp nhận chúng và chúng thường yêu cầu tham số tiền tệ phải được chỉ định trong yêu cầu ban đầu. Nếu một trang web không xác thực tham số tiền tệ sau khi hoàn tất giao dịch, người dùng có thể gian lận bằng cách gửi tiền bằng loại tiền tệ có giá trị thấp hơn nhiều so với loại tiền tệ được yêu cầu. Ví dụ sau đây cho thấy phương thức thanh toán PayPal được triển khai kém có thể bị khai thác:

Một người dùng thực hiện thanh toán 20 bảng Anh cho một trang web, sử dụng tùy chọn thanh toán PayPal. Yêu cầu mà trang web gửi đến trang web PayPal đã bị chặn và tham số tiền tệ đã được thay đổi thành "INR" (Rupee Ấn Độ) từ "GBP" (Bảng Anh). Sau khi hoàn tất giao dịch trên trang web PayPal với 20 Rupee Ấn Độ, trang web đã cho phép giao dịch mà không cần kiểm tra loại tiền tệ và 20 bảng Anh đã được gửi vào tài khoản của người dùng trong khi chỉ có 0,22 bảng Anh được rút khỏi tài khoản PayPal.

## 3. Thao túng số lượng

Các trang web tính toán giá cuối cùng dựa trên số lượng mặt hàng đã mua. Do đó, có thể điều chỉnh tham số này để chứa các giá trị nhỏ hoặc âm, nhằm ảnh hưởng đến giá trên trang thanh toán cuối
cùng.

Trang web có thể xóa các mục có giá trị bằng không hoặc âm trong các tham số số lượng. Trong trường hợp này, các giá trị thập phân như "0,01", "0,51" hoặc "0,996" có thể được kiểm tra để xem chúng có ảnh hưởng gì đến giá cuối cùng hay không. Phương pháp này có thể nguy hiểm hơn khi sử dụng trên các mục thường không được xem xét thủ công.

## 4. Thao túng địa chỉ giao hàng và phương thức gửi

Việc thay đổi địa chỉ giao hàng và phương thức gửi có thể làm thay đổi chi phí của các mặt hàng. Do đó, điều quan trọng là phải kiểm tra thao tác này trong giai đoạn cuối của quy trình thanh toán để kiểm tra xem nó có làm thay đổi chi phí hay không. Đôi khi có thể thay đổi địa chỉ giao hàng sau khi đặt hàng và trước khi nhận hóa đơn, bằng cách thay đổi địa chỉ hồ sơ người dùng, do đó cũng cần phải kiểm tra điều này. Đây cũng có thể là sự cố TOCTOU – xem phần trên.

Giá trị thuế cũng có thể dựa trên địa chỉ. Điều này cần được kiểm tra để đảm bảo rằng kẻ tấn công không dễ dàng trốn tránh các loại thuế bắt buộc, chẳng hạn như VAT hoặc phí nhập khẩu, bằng cách thao túng địa chỉ trong quá trình này.

## 5. Thao túng chi phí bổ sung

Bất kỳ thông số bổ sung nào có thể ảnh hưởng đến giá thành cuối cùng của sản phẩm, chẳng hạn như giao hàng vào thời điểm cụ thể hoặc thêm giấy gói quà cũng cần được kiểm tra để đảm bảo rằng không thể thêm chúng miễn phí ở bất kỳ giai đoạn nào của quá trình thanh toán.

## 6. Thao túng phản hồi

Đôi khi, các quy trình thanh toán ứng dụng, kiểm tra giấy phép ứng dụng hoặc mua tài sản trong ứng dụng cũng có thể bị bỏ qua bằng cách thao túng phản hồi của máy chủ. Mối đe dọa này thường
xảy ra khi ứng dụng không xác minh phản hồi của bên thứ ba và phản hồi chưa được ký bằng mật mã.

Ví dụ, có những ứng dụng có phiên bản dùng thử giới hạn thời gian không xác thực bằng mật mã phản hồi của máy chủ khi mua giấy phép. Do đó, có thể kích hoạt ứng dụng mà không phải trả bất
kỳ khoản tiền nào, bằng cách chặn và thao túng phản hồi của máy chủ đối với yêu cầu mua giấy phép.

Các ví dụ khác bao gồm các trò chơi di động tải xuống cài đặt người dùng từ máy chủ sau khi mở ứng dụng. Đối với các
ứng dụng dễ bị tấn công, có thể thao túng phản hồi của máy chủ để sử dụng các mục không miễn phí hoặc bị khóa mà
không phải trả bất kỳ khoản tiền nào.

## 7. Lặp lại một tham số đầu vào nhiều lần (như HTTP Parameter Pollution)

Trường hợp này rất hiếm khi xảy ra, nhưng việc lặp lại tham số đầu vào trong yêu cầu gửi đến ứng dụng hoặc cổng thanh toán có thể gây ra các vấn đề về logic, đặc biệt là khi ứng dụng sử dụng các cơ sở mã hoặc công nghệ khác nhau để phân tích cú pháp đầu vào ở phía máy chủ.

Các công nghệ khác nhau có thể hoạt động khác nhau khi chúng nhận được các tham số đầu vào lặp lại. Điều này trở nên đặc biệt quan trọng khi ứng dụng gửi yêu cầu phía máy chủ đến các ứng dụng khác có các công nghệ khác nhau hoặc khi có mã tùy chỉnh để xác định đầu vào.

Ví dụ, tham số “số tiền” được lặp lại trong URL sau:

```
/page.extension?amount=2&amount=3&amount[]=4
```

Điều này có ý nghĩa khác nhau đối với mã được viết bằng ASP, ASP.Net hoặc PHP, như được hiển thị bên dưới:

```
ASP - số lượng = 2, 3
ASP.Net - số lượng = 2,3
PHP (Apache) - số lượng = Mảng
```

Bài kiểm tra này cho thấy một ví dụ điển hình về ô nhiễm tham số HTTP (HTTP Parameter Pollution). Tuy nhiên, việc lặp lại các tham số đầu vào không chỉ giới hạn ở các tham số GET hoặc POST thông thường mà còn có thể được sử dụng trong các tình huống khác như lặp lại một số thẻ và thuộc tính XML trong một yêu cầu XML hoặc một đối tượng JSON khác trong các đối tượng JSON gốc.

## 8. Bỏ qua một tham số đầu vào hoặc giá trị của nó

Tương tự như việc lặp lại các tham số đầu vào, việc bỏ qua các tham số cũng có thể gây ra các vấn đề logic khi ứng dụng không thể tìm thấy đầu vào hoặc coi ký tự null là giá trị. Các trường hợp sau đây có thể được kiểm tra các đầu vào nhạy cảm để vượt qua một số cơ chế bảo vệ:

- Xóa bỏ giá trị
- Thay thế giá trị bằng một ký tự null
- Xóa ký tự dấu bằng sau tham số đầu vào
- Xóa hoàn toàn tham số đầu vào khỏi yêu cầu

## 9. Mass Assignment, Autobinding, or Object Injection

Điều này xảy ra khi một ứng dụng chấp nhận các tham số bổ sung khi chúng được đưa vào yêu cầu. Điều này có thể xảy ra trong một số ngôn ngữ hoặc framework như Ruby on Rails, NodeJS, Spring MVC, ASP NET MVC và PHP.

Điều này có thể gây ra vấn đề cho ứng dụng tài chính khi dữ liệu liên quan đến chi phí có thể bị thao túng.

Ví dụ, lỗi này đã được khai thác trên một trang web thực tế để thay đổi địa chỉ giao hàng và ngày "phải thanh toán" trên hóa đơn khiến hóa đơn gần như không thể thanh toán được vì ngày thanh toán được đặt ở tương lai xa.

## 10. Theo dõi hành vi trong khi thay đổi các tham số để phát hiện các lỗi logic

Cũng giống như khi thử nghiệm các ứng dụng phi tài chính, tất cả các tham số đầu vào trong quy trình thanh toán phải được thử nghiệm riêng biệt để phát hiện các lỗi logic. Trong ví dụ dưới đây, luồng quy trình thanh toán có thể được thay đổi bằng cách thao tác một số tham số:

Trong ứng dụng web, có một tham số được sử dụng để yêu cầu máy chủ sử dụng cơ chế 3D-Secure, có thể được điều chỉnh để tránh quá trình kiểm tra này.

Đôi khi các ứng dụng web chứa một tham số hiển thị số trang hoặc giai đoạn hiện tại. Người dùng có thể bỏ qua một số giai đoạn hoặc trang nhất định bằng cách thao tác tham số này trong yêu cầu tiếp theo.

Thông thường không nên thay đổi nhiều hơn một tham số trong một khung thời gian thử nghiệm giới hạn; tuy nhiên, một số lỗi logic chỉ có thể được tìm thấy bằng cách thay đổi nhiều hơn một tham số cùng một lúc. Điều này hữu ích khi ứng dụng phát hiện thao tác tham số đối với các tham số như trường giá. Mặc dù có thể không khả thi khi kiểm tra các kết hợp khác nhau của tất cả các tham số đầu vào, nhưng nên sửa đổi ít nhất một vài đầu vào thú vị cùng một lúc. Để tự động hóa thử nghiệm này, trường mục tiêu như tham số giá hoặc số lượng có thể được đặt thành một số tiền cụ thể mà thông thường không được phép, sau đó có thể thay đổi từng tham số khác để phát hiện bất kỳ khả năng bỏ qua nào của các cơ chế xác thực hiện tại khi ứng dụng chấp nhận các mục đã thao tác.

The following shows an example of this kind of vulnerability.

Suppose the server-side code is as follows:

```csharp
1: Try
2: ' Delivery type should be an integer
3: deliveryType = Int(deliveryType)
4: ' Quantity should be an integer
5: quantity = Int(quantity)
6: Catch ex As Exception
7: ' Empty catch!
8: End Try
9:' Continue ...
```

Mã này đảm bảo rằng biến “deliveryType” chứa một số nguyên, sau đó thực hiện tương tự đối với biến “quantity”. Do đó, nếu các số thập phân được gửi đi, chúng sẽ được chuyển đổi thành các giá trị
số nguyên để ngăn chặn vấn đề bảo mật trong đó người dùng có thể trả ít hơn bằng cách thay đổi tham số “quantity” thành giá trị thập phân như “0,1”. Tuy nhiên, do một giá trị rỗngNắm lấyphần ở
dòng 7, tham số “quantity” vẫn có thể chứa số thập phân như “0,1” khi tham số “deliveryType” chứa chuỗi như “foobar”. Trong trường hợp này, ứng dụng nhảy đếnNắm lấyphần do lỗi khi chuyển đổi
giá trị chuỗi thành số nguyên ở dòng 3, trước khi chuyển đổi tham số “số lượng” thành số nguyên.

# Replay Attacks (Capture-Replay)

Tấn công phát lại xảy ra khi toàn bộ hoặc một phần tin nhắn giữa máy khách và máy chủ được sao chép và phát lại sau đó. Các tham số cũng có thể được thay đổi khi không có kỹ thuật ngăn chặn thao túng
tham số như xác thực chữ ký tin nhắn nào có trên phía máy chủ. Mặc dù tin nhắn có thể được ký hoặc mã hóa để ngăn chặn thao túng tham số, nhưng điều này sẽ không dừng phát lại tin nhắn ban đầu được tạo bởi một bên đáng tin cậy.

Một ứng dụng có thể gặp phải các vấn đề bảo mật nghiêm trọng khi tin tưởng các yêu cầu được phát lại mà không thực hiện bất kỳ xác thực nào để kiểm tra xem chúng đã được nhận hoặc gửi theo đúng thứ tự hay chưa.

## 1. Replaying the Call-back Request

Hệ thống thanh toán thường chuyển hướng người dùng đến một trang cụ thể khi thanh toán đã được xử lý thành công hoặc không thành công. Đôi khi có thể phát lại yêu cầu thanh toán thành
công để ủy quyền cho một giao dịch chưa được xử lý.

Ví dụ, một trang web đã ký tất cả các tham số đầu vào ngoại trừ tham số "transaction-id" trong yêu cầu gọi lại thành công. Tham số này có thể được thay thế bằng một transaction-id mới để hoàn tất thanh toán mà không tốn bất kỳ khoản tiền nào.

## 2. Replaying an Encrypted Parameter (Phát lại một tham số được mã hóa)

Đôi khi các trang web mã hóa một số thông số quan trọng mà không tạo ra cơ chế để phát hiện các cuộc tấn công phát lại. Ví dụ, có một trang web mã hóa các giá trị giá trên phía máy chủ để đưa
chúng vào các trường nhập liệu ẩn. Mặc dù không thể thao túng giá trực tiếp khi các thông số giá được mã hóa, nhưng vẫn có thể sử dụng thông số giá được mã hóa của các mặt hàng rẻ hơn để
mua các mặt hàng đắt hơn (giá riêng lẻ được mã hóa, nhưng không phải toàn bộ yêu cầu).

# Rounding Errors (Lỗi làm tròn)

> CWE: 187 and 681

Giá trị số có thể được lưu trữ trong các biến số nguyên hoặc số thực. Mặc dù các biến số thực có thể chứa các số có một số chữ số sau dấu thập phân, số lượng chữ số vẫn hữu hạn và dựa trên loại biến
và độ chính xác của nó. Biến số nguyên chỉ có thể chứa các giá trị số không có bất kỳ chữ số nào sau dấu thập phân.

Khi một giá trị toán học được lưu trữ trong một biến số, nó cần được làm tròn dựa trên độ chính xác của kiểu biến. Do đó, số được lưu trữ mới có thể lớn hơn hoặc nhỏ hơn một chút so với giá trị ban
đầu. Hành vi bình thường này đôi khi có thể bị kẻ tấn công lợi dụng.

## 1. Currency Rounding Issues (Vấn đề làm tròn khi chuyển đổi tiền tệ)

Nếu một ứng dụng tài chính thực sự chuyển đổi các loại tiền tệ khác nhau cho nhau mà không mất phí hoa hồng hoặc không có tỷ giá mua và bán khác nhau có lợi cho công ty, điều này có thể dẫn đến lợi nhuận tài chính cho kẻ tấn công.

Các ứng dụng mua sắm hỗ trợ nhiều loại tiền tệ cũng có thể gặp phải vấn đề làm tròn tiền tệ, khi người dùng có thể mua một mặt hàng bằng một loại tiền tệ và hoàn lại tiền bằng loại tiền tệ khác.

Ngoài ra, các ứng dụng mà người dùng có thể gửi tiền vào tài khoản của họ (như ngân hàng, công ty thẻ gọi điện thoại quốc tế hoặc trang web cờ bạc) có thể trở nên dễ bị tấn công nếu chúng hỗ trợ nhiều loại tiền tệ với tỷ giá hối đoái khác nhau và người dùng có thể rút tiền đã gửi từ tài khoản của họ ngay lập tức mà không mất bất kỳ chi phí nào. Việc thay đổi loại tiền tệ của tài khoản sau lần gửi tiền đầu tiên cũng có thể dẫn đến lỗ hổng này. Điều này có thể gây ra nhiều vấn đề hơn khi ứng dụng sử dụng tỷ giá hối đoái khác với cổng thanh toán (xem phần “Chênh lệch tiền tệ trong Nạp tiền/Mua và Rút tiền/Hoàn tiền”).

## 2. Generic Rounding Issues (Các vấn đề chung khi làm tròn)

Các vấn đề làm tròn không phải lúc nào cũng giới hạn ở việc trao đổi tiền tệ. Ngay cả các ứng dụng mua sắm chỉ hỗ trợ một loại tiền tệ cũng có thể bị ảnh hưởng bởi sự không nhất quán giữa các phần khác nhau của ứng dụng.

Sau đây là một ví dụ về loại mâu thuẫn này, cần được kiểm tra:

Người dùng chọn gửi 10,0049 bảng Anh vào một trang web có thể giữ số dư của người dùng; trang web giữ số tiền này trong cơ sở dữ liệu để ủy quyền và thêm vào số dư của người dùng khi giao dịch chuyển tiền từ ngân hàng hoàn tất. Tuy nhiên, API ngân hàng chỉ chấp nhận các số có hai chữ số sau dấu thập phân dựa trên tiêu chuẩn của nó. Do đó, ứng dụng chuyển đổi số tiền thành 10,00 bảng Anh và chờ người dùng và cổng thanh toán hoàn tất giao dịch này. Sau khi giao dịch hoàn tất, 10,00 bảng Anh sẽ được khấu trừ khỏi tài khoản ngân hàng của người dùng nhưng 10,0049 bảng Anh sẽ được gửi vào số dư của trang web. Sau khi lặp lại quy trình này 205 lần, người dùng có thể kiếm được 1,00 bảng Anh.

Vấn đề tương tự phát sinh khi tính toán tiền tệ trong cùng một ứng dụng được thực hiện bởi các ứng dụng khác nhau hoặc các mã khác nhau. Một ví dụ có thể là việc sử dụng các thủ tục lưu trữ cơ sở dữ liệu đối với một số phép tính (ví dụ chuyển tiền) và mã C# với các quy tắc khác nhau cho các phép tính tiền tệ khác (như rút tiền hoặc hủy chuyển tiền).

# Numerical Processing (Xử lý số)

> CWE:189

Rõ ràng là các con số đóng vai trò quan trọng trong các hệ thống tài chính. Việc thao túng các con số cho các ứng dụng thương mại điện tử có thể dẫn đến các vấn đề logic khác nhau và mất tiền trong các trường hợp nghiêm trọng. Do đó, các trường hợp thử nghiệm khác nhau nên được thiết kế để kiểm tra việc thao túng tham số số trong các trường số như giá, số lượng, mã chứng từ, v.v.

## 1. Số âm

Số âm có thể dẫn đến một số vấn đề logic. Hầu hết thời gian, chúng đảo ngược logic ứng dụng, ví dụ, người dùng có thể gửi "£100" bằng cách hoàn lại "-£100" từ hệ thống. Bất kỳ giá trị tham số liên
quan nào như tham số số lượng cũng có thể được sử dụng cho mục đích này.

Khi logic ứng dụng bị đảo ngược, việc chuyển “-£100” vào một tài khoản khác có thể giống như chuyển tiền từ tài khoản mục tiêu để đánh cắp tiền của họ. Vấn đề logic tương tự cũng áp dụng cho điểm thưởng hoặc trong các ứng dụng trò chơi trong đó chip hoặc các loại tiền ảo khác được sử dụng thay vì tiền để mua các vật phẩm ảo.

Mặc dù việc sử dụng số âm trong các tham số khác nhau không phải lúc nào cũng đảo ngược logic của ứng dụng, nhưng nó có thể gây ra các lỗi logic hữu ích khác và luôn cần phải được kiểm tra.

Giá trị “-1” cũng cần được kiểm tra riêng vì nó có thể có ý nghĩa cụ thể đối với ứng dụng vì các nhà phát triển thường sử dụng nó để khởi tạo các tham số số hoặc khi một điều kiện nào đó không được đáp ứng.

## 2. Số thập phân

Ngoài các vấn đề làm tròn đã được thảo luận trước đó, số thập phân có thể gây ra các vấn đề logic cho các ứng dụng, đặc biệt là khi một tham số như số lượng chỉ nên chấp nhận các giá trị số nguyên. Các giá trị thập phân cũng có thể được sử dụng để khai thác các vấn đề làm tròn – xem phần trên. Một cách sử dụng bổ sung của các giá trị thập phân là tạo cùng một giao dịch nhiều lần khi có hạn chế về tính duy nhất của các mục trong một đơn hàng; trong trường hợp này, nó có thể được sử dụng trong các tham số id số để trỏ đến cùng một mục nhiều lần bằng cách có các giá trị như "1234", "1234.00" hoặc "01234.000001", có thể có cùng ý nghĩa khi được xử lý bởi hệ thống thanh toán hoặc cơ sở dữ liệu.

## 3. Large or Small Numbers

Kiểm tra xác thực phạm vi là một thử nghiệm quan trọng, phải được thực hiện bằng cách sử dụng giá trị lớn hơn hoặc nhỏ hơn một chút so với giá trị tối đa và tối thiểu (cũng có thể sử dụng số thập phân ở đây)

## 4. Overflows and Underflows

Tràn hoặc thiếu số có thể xảy ra khi giá trị hoặc kết quả của phép tính lớn hơn hoặc nhỏ hơn giá trị có thể lưu trữ cho loại biến đó trong bộ nhớ hoặc cơ sở dữ liệu.

Ví dụ, trong Java hoặc C# (không phải VB.NET), nếu giá trị số nguyên đạt đến giá trị tối đa (“2^31-1 = 2147483647”) và được tăng lên, tràn số xảy ra mà không gây ra bất kỳ lỗi nào, khiến giá trị chuyển sang giá trị tối thiểu nhỏ nhất (“-2^31= -2147483648”). Những con số này có thể được sử dụng để bỏ qua một số xác thực. Một hành vi tương tự có thể xảy ra trong các ngôn ngữ lập trình khác.

## 5. Zero, Null, or Subnormal Numbers

“0”, “NaN” hoặc ký tự null có thể được sử dụng trong các ngữ cảnh khác nhau, đặc biệt là để thao túng giá. Các số khác không có độ lớn nhỏ hơn số chuẩn nhỏ nhất và gần bằng không, chẳng hạn
như “0.00000000000000000000000000000000001” hoặc “1e-50”, cũng nên được kiểm tra.

## 6. Exponential Notation (Ký hiệu mũ)

Ký hiệu mũ khá hữu ích để bỏ qua các hạn chế về độ dài trong đó các giá trị số không thể chứa một số chữ số nhất định.
Ví dụ, khi chỉ được phép có bốn ký tự, ký hiệu sau có thể bỏ qua giới hạn “9999” làm giá trị tối đa:

```
9e99 = 9 * 10^99 - 100 chữ số
```

Một ví dụ khác là khi ký tự chấm (“.”) không được phép tạo số thập phân:

```
1e-1 = 0,1
```

## 7. Reserved Words (từ khoá)

Các từ dành riêng sau đây có thể được sử dụng trong các ứng dụng Java và C# để biểu diễn một số, điều này có thể gây ra các vấn đề logic nghiêm trọng:

```
NaN
Infinity
-NaN
-Infinity
```

## 8. Numbers in Different Formats(Số ở các định dạng khác nhau)

Số trong các công nghệ khác nhau có thể được viết ở các định dạng khác nhau để bỏ qua các cơ chế xác thực. Ví dụ, khi gửi "0" dưới dạng giá trị bị hạn chế, "0,00", "-0,00" hoặc thậm chí "$0" hoặc "£0" có thể được phép.

Columns Description:
A. VBScript – ASP Classic IsNumeric function
B. C# – .NET IsNumeric function
C. C# – .NET Double.TryParse function + result value
D. Java – Float.valueOf function + result value
E. PHP – is_numeric function
F. PHP– floatval function + result value

| **String**                                      | **A**    | **B**    | **C**               | **D**               | **E**    | **F**          | **Comment**                                                                                                     |
|-------------------------------------------------|----------|----------|---------------------|---------------------|----------|----------------|-----------------------------------------------------------------------------------------------------------------|
| **001.0000**                                    | **True** | **True** | **True (1)**        | **True (001.0000)** | **True** | **True (1)**   | Decimal symbol with leading zeros based on the regional settings of the server                                  |
| **$10**                                         | False    | **True** | False (10)          | False               | False    | False          | Currency symbol based on the regional settings of the server (culture format).                                  |
| **1,,2,,,3,,**                                  | **True** | **True** | **True (123)**      | False               | False    | **True (1)**   | Digit grouping symbol based on the regional settings of the server (culture format). Can be created by HPP too. |
| **-10.0**                                       | **True** | **True** | **True (-10)**      | **True (-10.0)**    | **True** | **True (-10)** | Negative symbol based on the regional settings of the server. It could be a positive sign.                      |
| **(10)**                                        | **True** | **True** | False (-10)         | False               | False    | False          | Negative symbol based on the regional settings of the server.                                                   |
| **10-**                                         | **True** | **True** | False (-10)         | False               | False    | **True (10)**  | Negative symbol based on the regional settings of the server. It could be a positive sign.                      |
| **1e2**                                         | **True** | **True** | **True (100)**      | **True (1e2)**      | **True** | **True (100)** | String length can be less than the number’s length                                                              |
| **%20%091**                                     | **True** | **True** | **True (1)**        | **True (1)**        | **True** | **True (1)**   | Space characters (09-0D and 20) Space characters (09-0D and 20) %20=Space %09=Tab                               |
| **1%20%00%00**                                  | **True** | **True** | **True (1)**        | **True (1)**        | False    | **True (1)**   | Space characters (09-0D and 20) followed by Null Character(s)                                                   |
| **&hff**                                        | **True** | **True** | False (255)         | False               | False    | False          | &h and &o can be used in VBScript to represent a number in Hex or Octal.                                        |
| **Infinity**                                    | False    | **True** | **True (Infinity)** | **True (Infinity)** | False    | False          | Infinity: a reserved Word for C# and Java                                                                       |
| **NaN**                                         | False    | **True** | **True (NaN)**      | **True (NaN)**      | False    | False          | NaN (not a number): a reserved Word for C# and Java                                                             |
| **0x0A**                                        | False    | False    | False               | False               | **True** | False          | Hex format                                                                                                      |
| **An Array**                                    | False    | False    | False               | False               | False    | **True (1)**   | Providing an input as an array. e.g.: p.php?in[]=val                                                            |
| **%0B%09%20-0001,,,,2.8e0002%09%20%0C%00%00**   | **True** | **True** | **True (-1280)**    | False               | False    | **True (-1)**  | An example using the above notations                                                                            |
| **%0B$%09%20(0001,,,,2.8e0002%09%20)%0C%00%00** | False    | **True** | False (-1280)       | False               | False    | False          | An example using the above notations                                                                            |
Note 1: “Integer.parseInt” in Java cannot convert any of the numbers in the above table.
Note 2: “Convert.ToInt32("0X0A", 16)” in C# .Net returns “10”. This function cannot convert other numbers in the above table though.
Note 3: PHP 5.4 supports a binary prefix (“0b”) that can be used to create a number as well.

# Card Number-Related Issues

Số thẻ thanh toán là một trong những dữ liệu hấp dẫn nhất đối với kẻ tấn công. Ngoài việc được sử dụng để mua sắm trực tuyến, chúng có thể được bán trên thị trường chợ đen ngay cả khi không có mã xác minh thẻ hoặc giá trị (số ba chữ số hoặc bốn chữ số được in ở mặt trước hoặc mặt sau của thẻ thanh toán).

Ngày nay, nhiều trang web thương mại điện tử tuân thủ Tiêu chuẩn bảo mật dữ liệu ngành thẻ thanh toán (PCI DSS) [8], giúp chúng an toàn hơn và để thu hút nhiều nhà cung cấp và khách hàng
hơn, đồng thời giảm nguy cơ vi phạm dữ liệu thẻ. Do đó, chúng không được lưu trữ vĩnh viễn mã xác minh thẻ được sử dụng để xác minh các giao dịch không có thẻ. Ngoài ra, chúng phải mã hóa số thẻ
trong bộ nhớ của mình. Các ví dụ sau đây thảo luận về hai vấn đề bảo mật khác nhau mà các ứng dụng web tuân thủ PCI vẫn có thể gặp phải.

## 1. Showing a Saved Card Number during the Payment Process (Hiển thị số thẻ đã lưu trong quá trình thanh toán)

Các trang web thương mại điện tử có thể tiết lộ số thẻ ngân hàng đã lưu của người dùng trong quá trình thanh toán. Hầu hết thời gian, điều này xảy ra do triển khai không tốt và số thẻ không bắt buộc
phải hiển thị. Tuy nhiên, đôi khi, số thẻ phải được giải mã trên trang thanh toán; ví dụ nếu số thẻ được gửi đến trang web xác thực 3D-Secure.

Điều này có thể gây ra vấn đề vì kẻ tấn công có thể chiếm đoạt phiên làm việc hoặc thông tin đăng nhập của người dùng hoặc khai thác lỗ hổng tấn công cross-site scripting (XSS) để lấy được số thẻ.
Rủi ro có thể được giảm thiểu nếu số thẻ chỉ được hiển thị một phần (ví dụ: số cuối cho các chữ số) khi cần thiết, các trang chứa số thẻ được bảo vệ bằng mật khẩu và quy trình xác thực 3D-Secure
hoặc các cơ chế tương tự không thể được kích hoạt trực tiếp bằng cách truy cập vào các trang đó khi không cần thiết.

NCC Group cũng thường tìm thấy số thẻ chưa lưu trong phản hồi HTTP sau khi sử dụng số thẻ trong quy trình thanh toán và trước khi đăng xuất khỏi trang web. Hành vi này cũng có thể nguy hiểm, đặc biệt là khi trang web dễ bị tấn công XSS hoặc chiếm quyền điều khiển phiên (session-hijacking). Cần lưu ý rằng mã CVV (CV2) (mã xác minh thẻ) không bao giờ được xuất hiện trong bất kỳ phản hồi nào từ máy chủ.

## 2. Card Number Enumeration via Registering Duplicate Cards (Truy tìm số thẻ thông qua đăng ký trùng)

Một số trang web không cho phép khách hàng lưu cùng một số thẻ trong nhiều tài khoản. Một trong những lý do là để phát hiện các tài khoản trùng lặp hoặc để ngăn chặn việc lợi dụng các ưu đãi của người mua lần đầu.

Chức năng này, khi được triển khai không tốt, có thể bị lạm dụng để lấy cắp số thẻ người dùng khác đã được đăng ký trên trang web.

# Dynamic Prices, Prices with Tolerance, or Referral Schemes (Giá động, giá có dung sai hoặc chương trình giới thiệu)

> CWE: 840

Đôi khi giá cả và chiết khấu có thể thay đổi do tỷ giá hối đoái, số lượng mặt hàng bán được, chương trình giới thiệu và sự chậm trễ trong việc gửi giá trong hệ thống giao dịch năng động.

Do đó, cần xem xét lại thông số kỹ thuật của ứng dụng để xem liệu nó có hỗ trợ giá động hay không. Hầu hết thời gian, một tham số đầu vào bổ sung giúp ứng dụng nhận ra việc sử dụng giá động. Ví
dụ, hệ thống có thể bắt đầu sử dụng giá động khi ứng dụng không sử dụng loại tiền tệ mặc định hoặc khi khách hàng sử dụng thiết bị di động hoặc cư trú tại một quốc gia nào đó có tốc độ Internet
chậm hơn. Hệ thống cũng có thể cân nhắc sử dụng giá đã gửi khi có tiêu đề giới thiệu hoặc tham số giới thiệu. Để tìm các hệ thống này, cần gửi một số gần với giá gốc (giá ± 0,01) trong khi thay đổi các
tham số khác.

Các tham số khác ảnh hưởng đến giá cuối cùng cũng có thể là động hoặc có biên độ ngưỡng. Ví dụ, khá
bình thường khi thấy hành vi này trong tham số "tỷ lệ cược" của ứng dụng cá cược trực tiếp.

Chính sách ứng dụng nên được xem xét bất cứ khi nào giá động được tìm thấy, để đảm bảo rằng giá thay
đổi nằm trong biên độ cho phép. Ngoài ra, nên sử dụng phương pháp mã hóa an toàn khi giá được tạo
bởi một bên đáng tin cậy hoặc thậm chí bởi chính trang web, để xác định bất kỳ thao túng nào của các
bên không đáng tin cậy.

# Discount Codes, Vouchers, Offers, Reward Points, and Gift Cards

> Mã giảm giá, Phiếu mua hàng, Ưu đãi, Điểm thưởng và Thẻ quà tặng

Người dùng có thể kiếm được điểm thưởng trong nhiều ứng dụng thương mại điện tử khi điểm có thể được sử dụng để mua hàng, chúng phải được xử lý và kiểm tra chính xác như số dư của người dùng. Do đó, các vấn đề về số âm, làm tròn, đồng thời, v.v. đều phải được kiểm tra.

## 1. Enumeration and Guessing (Thu thập và đoán)

Mã giảm giá và phiếu mua hàng có thể được sử dụng để giảm giá cuối cùng nên được kiểm tra để đảm bảo chúng không thể dự đoán được và không thể dễ dàng liệt kê.

Tương tự như vậy, số thẻ quà tặng hoặc thẻ khách hàng thân thiết phải không thể đoán trước và rất khó để liệt kê, nếu không kẻ tấn công có thể tạo một thẻ trùng lặp để sử dụng số dư của nạn nhân. Khi những thẻ này có số dư có thể chi tiêu, chúng phải được xử lý tương tự như số thẻ ngân hàng và phải được bảo vệ bằng mã PIN hoặc mật khẩu.

## 2. Vouchers and Offers Stacking (Phiếu giảm giá và Ưu đãi xếp chồng)

Các ứng dụng thương mại điện tử thường ngăn chặn việc sử dụng nhiều phiếu giảm giá hoặc ưu đãi trong một giao dịch. Tuy nhiên, đôi khi xảy ra lỗi logic khi ví dụ như ưu đãi mua 1 tặng 1 được kết hợp với ưu đãi mua 3 tặng 2 hoặc mua 3 tặng 1 có thể dẫn đến ưu đãi mua 3 tặng 1 hoặc mua 3 tặng 0,5.

## 3. Earning More Points or Cash Return than the Price when Buying an Item

> Kiếm được nhiều điểm hoặc tiền mặt hơn giá khi mua một mặt hàng

Việc tích điểm khi sử dụng điểm để mua một mặt hàng không nên khả thi vì có thể dẫn đến sai sót về mặt logic. Một ví dụ có thể là một ưu đãi khuyến mại mà việc mua bằng điểm sẽ dẫn đến việc tích lũy cùng một lượng điểm. Điều này cũng có thể xảy ra trong các hệ thống có thể chấp nhận tiền mặt khi tiền mặt khuyến mại được trả lại hoặc điểm đã tích lũy có thể được sử dụng để mua cùng một mặt hàng.

Một ví dụ thú vị khác là việc mua thẻ tiền mặt trả trước có thể được sử dụng như tiền thật. Những thẻ này có thể được mua với giá thấp hơn giá trị thực của chúng khi có ưu đãi cho tất cả các thẻ quà tặng. Điều này thậm chí có thể gây ra nhiều vấn đề hơn khi thẻ quà tặng có thể được sử dụng để mua thêm thẻ quà tặng để tạo ra lợi nhuận liên tục cho đến khi hết hàng.

## 4. Sử dụng Mã hết hạn, Mã không hợp lệ hoặc Mã của Người dùng khác

Cần xem xét lại hành vi ứng dụng sau khi áp dụng bất kỳ phương pháp giảm giá nào để xem có bất kỳ tham số thú vị nào có thể được thao tác hoặc phát lại để sử dụng mã giảm giá cho các sản phẩm khác nhau hay không, sau một ngày nhất định khi mã hết hạn hoặc nhiều lần khi mã hết hạn sau lần sử dụng đầu tiên (vấn đề đồng thời cũng có thể được kiểm tra tại đây).

Phiếu giảm giá và ưu đãi nên được thử để đảm bảo chúng không thể được sử dụng để mua các mặt hàng bất hợp pháp, ví dụ như sử dụng mã giảm giá sản phẩm mới để gia hạn dịch vụ cũ. Một ví dụ khác về vấn đề xác minh là khi mã khuyến mại của nhà cung cấp A có thể được sử dụng trên trang web của nhà cung cấp B, ngay cả khi người dùng không có tài khoản với nhà cung cấp A.

## 5. State and Basket Manipulation (Thao túng trạng thái và giỏ hàng)

Các ứng dụng cần được kiểm tra để đảm bảo rằng giá trị chiết khấu được tính toán ở giai đoạn mua hàng cuối cùng khi người dùng thay đổi đơn hàng ban đầu theo bất kỳ cách nào (thêm/xóa mặt hàng hoặc thay đổi số lượng).

Vấn đề này có thể bị khai thác khi việc xóa các mục khỏi một gói không làm giảm chiết khấu cho các mục còn lại đã chọn. Trong trường hợp này, các mục bổ sung được thêm vào giỏ hàng để đáp ứng chương trình khuyến mãi và chiết khấu vẫn được tôn trọng khi chúng bị xóa.

Một biến thể khác là khi các mặt hàng được giảm giá và không được giảm giá có thể được thêm vào giỏ hàng để nhận được mức giảm giá bổ sung cho toàn bộ giỏ hàng. Ví dụ, điều này có thể được khai thác tương tự như việc tích lũy phiếu giảm giá hoặc khuyến mại khi một mã phiếu giảm giá khác có thể được áp dụng cho toàn bộ giỏ hàng, vì có một mặt hàng không được giảm giá. Trong một số trường hợp, mặt hàng ban đầu không được giảm giá có thể bị xóa khỏi giỏ hàng sau đó mà không mất mức giảm giá cho mặt hàng đã được giảm giá.

## 6. Refund Abuse (Lạm dụng hoàn tiền)

Quá trình hoàn tiền cũng nên được kiểm tra để đảm bảo rằng người dùng không thể kiếm được điểm miễn phí bằng cách mua và hoàn tiền cho các mặt hàng. Điểm có thể được sử dụng trong khoảng thời gian giữa việc mua và hoàn tiền cho các mặt hàng; trong trường hợp này, người dùng có thể không có đủ điểm trong thẻ thưởng của họ khi hoàn tiền cho một mặt hàng và cần có chính sách phù hợp để khôi phục lại số điểm đã mất. Bất kỳ mặt hàng miễn phí nào đã thu thập cũng nên được coi là đã được trả lại khi hoàn tiền hoặc hủy đơn hàng sắp diễn ra.

## 7. Buy-X-Get-Y-Free

Các chương trình khuyến mại như mua một tặng một trong đó người dùng chỉ trả tiền cho sản phẩm đắt nhất cũng có thể bị lợi dụng để mua miễn phí những sản phẩm không áp dụng hoặc trả tiền cho sản phẩm rẻ nhất để được miễn phí những sản phẩm đắt hơn.

Các vấn đề logic sau đây chỉ ra một loạt các ví dụ có thể xảy ra ở đây:

- Không giảm giá mặt hàng rẻ nhất theo chương trình mua 2 tặng 1 (3). Điều này có thể dẫn đến việc mua một mặt hàng đắt tiền với giá rẻ hơn. Ví dụ, khi giảm giá được áp dụng cho mặt hàng cuối cùng được thêm vào giỏ hàng hoặc khi mặt hàng rẻ nhất không phải là mặt hàng cuối cùng theo thứ tự bảng chữ cái trong danh sách các mặt hàng trong giỏ hàng.
- Mua 2 tặng 1 có thể trở thành mua 1 tặng 1 khi mua thêm một sản phẩm miễn phí và sản phẩm miễn phí đó được tính là một trong 3.
- Mua 2 tặng 1 có thể được giảm giá 33% cho toàn bộ giỏ hàng. Mặc dù đây có thể là lỗi của con người, một số ứng dụng có thể có lỗi phần mềm cho phép điều này khi các mặt hàng khác nhau được trộn lẫn và kết hợp. Do đó, có thể thêm một mặt hàng đắt tiền và hai mặt hàng rẻ tiền vào giỏ hàng để mua mặt hàng đắt tiền với giá rẻ hơn.
- Mua 2 tặng 1 có thể trở thành 2 tặng 2 khi thêm 4 mục vào danh sách thay vì 3.
- Mua 2 tặng 1 có thể trở thành mua 1 tặng 2 khi có lỗi phần mềm. Mặc dù loại vấn đề này phổ biến, nhưng rất có thể là do lỗi của con người.

## 8. Ordering Out of Stock or Unreleased Items

> Đặt hàng các mặt hàng hết hàng hoặc chưa phát hành

Một số trang web có thể giảm giá các mặt hàng hết hàng để thu hút thêm khách hàng. Điều này có thể bị lạm dụng nếu đơn hàng có thể được thực hiện bằng các mặt hàng hết hàng khi đơn hàng vẫn có thể được chuyển đến kho của họ trong khi các mặt hàng vẫn tồn tại mặc dù đã được chọn là hết hàng trên trang web.

Bạn cũng có thể lạm dụng điều này để nhận được các mặt hàng miễn phí hoặc giảm giá bằng cách thêm một mặt hàng hết hàng vào giỏ hàng như một phần của chương trình giảm giá hoặc ưu đãi đặc biệt.

Cần lưu ý rằng vấn đề này cũng có thể bị khai thác bằng cách đặt hàng rồi hủy toàn bộ một mặt hàng cụ thể trên trang web nhằm tạo ra một mặt hàng tạm thời hết hàng trong khi trang web đang
xử lý yêu cầu hủy.

## 9. Bypassing Other Restrictions

Cần phải thực hiện các thử nghiệm bổ sung để bỏ qua mọi hạn chế có sẵn như số lượng mặt hàng cụ thể được bán hạn chế, sử dụng các ưu đãi dành riêng cho khách hàng hoặc sử dụng nhiều lần các phiếu mua hàng một lần.

## 10. Chuyển điểm

Nếu người dùng nhận được điểm thưởng bằng cách giới thiệu người khác đăng ký hoặc tự đăng ký lần đầu, họ có thể lợi dụng chương trình điểm thưởng bằng cách sử dụng chức năng chuyển điểm. Mặc dù chức năng chuyển điểm có thể không được người dùng truy cập trực tiếp trong ứng dụng, nhưng có thể sử dụng khi đóng tài khoản hoặc khi thẻ khách hàng thân thiết bị mất hoặc bị đánh cắp. Chức năng chuyển điểm cũng nên được kiểm tra để tìm các vấn đề về tình trạng race condition đã giải thích trước đó.

# Cryptography Issues

> CWE: 310

Các phương pháp mã hóa như mã hóa, mã hóa, ký và băm thường được thấy trong các hệ thống thanh toán. Tuy nhiên, lỗi thiết kế và lỗi triển khai, do lỗi của con người hoặc thiếu kiến thức về
vectơ tấn công, khá phổ biến trong lĩnh vực này, đặc biệt là trong các ứng dụng triển khai các phương pháp mã hóa riêng của chúng thay vì sử dụng các thư viện được triển khai trước đó.

Ví dụ, khi một ứng dụng băm một số tham số đã biết bằng khóa bí mật ngắn và không an toàn, khóa này có thể dễ dàng bị tấn công bằng phương pháp brute-force khi thuật toán đã biết. Đôi khi các ứng dụng không sử dụng khóa bí mật dài và mạnh khi việc triển khai không thực thi khóa đó.

Một ví dụ khác là cuộc tấn công mở rộng độ dài, trong đó hàm băm của khóa bí mật được nối với các giá trị khác có thể được khai thác để thêm dữ liệu vào yêu cầu ban đầu bằng cách thêm dữ liệu ban đầu và tính toán hàm băm mới (xem [5] và [6] để biết thêm chi tiết).

Các giá trị nối trong băm chữ ký cũng nên sử dụng các dấu phân cách không thể làm giả. Nếu không, có thể di chuyển một phần giá trị của tham số sang giá trị của tham số khác mà không thay đổi chữ ký vì chuỗi nối vẫn giữ nguyên.

Ví dụ sau đây hiển thị một hàm băm chữ ký dựa trên các tham số nối tiếp mà không có bất kỳ dấu phân cách nào có thể khiến ứng dụng dễ bị tấn công:

```
HMAC_SHA256(SecretKey, Other Parameters + ReferenceString + NumericalAmount)
```

Khi tham số “ReferenceString” có thể chứa một chuỗi tùy ý, tham số “NumericalAmount” có thể được
thao tác như hiển thị bên dưới để tạo cùng một hàm băm chữ ký:

```
OtherParams=OtherValues&...&ReferenceString=SomeStringHere&NumericalAmount=89
OtherParams=OtherValues&...&ReferenceString=SomeStringHere8&NumericalAmount=9
```

Khi các giá trị được mã hóa được sử dụng ở nhiều nơi trong các tham số đầu vào (trong cookie hoặc yêu cầu POST/GET), ứng dụng thường giải mã chúng ở nhiều nơi. Người dùng có thể sử dụng các trang đó để giải mã các giá trị được mã hóa không xác định để hiểu cách ứng dụng hoạt động. Vấn đề có thể trở nên nghiêm trọng nếu người dùng có thể định hình và mã hóa dữ liệu tùy ý bằng cách sử dụng các tham số đầu vào được cung cấp để thay thế các tham số được mã hóa hiện tại.

Như đã thảo luận trong phần “Tấn công phát lại”, đôi khi cũng không cần phải phá vỡ các phương pháp mã hóa vì chúng có thể bị phát lại.

# Downloadable and Virtual Goods

> CWE:425

Các ứng dụng thương mại điện tử bán hàng hóa ảo như tệp ứng dụng, MP3, video phát trực tuyến hoặc tệp PDF và tài liệu thường dễ bị tấn công tham chiếu đối tượng trực tiếp. Trong trường hợp này, kẻ tấn công có thể tải xuống hoặc sử dụng các tài liệu không miễn phí miễn phí chỉ bằng cách đoán hoặc tìm URL thực tế của các sản phẩm ảo.

# API Backend ẩn và không an toàn

> CWE:656

Các API phụ trợ được sử dụng bởi các hệ thống điểm bán hàng điện tử hoặc máy chủ thanh toán thường cũ và không an toàn vì người dùng không thể truy cập trực tiếp vào chúng. Đôi khi ngay cả các API ứng dụng di động hoặc máy tính bảng cũng không an toàn vì nhà phát triển không nghĩ đến bảo mật ở lớp ứng dụng phía máy chủ khi triển khai chúng.

Một số API và dịch vụ web này không có bất kỳ biện pháp bảo vệ nào chống lại nhiều kỹ thuật tấn công được mô tả và một số trong số chúng thậm chí còn gặp phải vấn đề về kiểm soát truy cập, cho phép kẻ tấn công thực hiện các tác vụ quản trị như điều chỉnh số dư.

# Using Test Data in Production Environment

> CWE:531

Để triển khai một ứng dụng thương mại điện tử, các phương thức thanh toán thử nghiệm và dữ liệu thẻ giả thường được sử dụng trong môi trường thử nghiệm hoặc dàn dựng để ngăn chặn việc gửi yêu cầu thử nghiệm đến các API thanh toán trực tiếp hoặc ngân hàng. Các nhà phát triển thường bỏ sót việc xóa mã khỏi môi trường sản xuất được cho là chỉ khả dụng trong môi trường thử nghiệm. Do đó, đôi khi có thể thay đổi một số tham số trong yêu cầu để buộc ứng dụng trực tiếp sử dụng dữ liệu thử nghiệm. Ngoài ra, một ứng dụng thương mại điện tử có thể không hiển thị tất cả các phương thức thanh toán của mình, đặc biệt là khi chúng không được bật cho một người dùng cụ thể hoặc khi chúng không được triển khai đầy đủ. Một số trang thử nghiệm mà các nhà phát triển sử dụng để thử nghiệm và gỡ lỗi chức năng của API của bên thứ ba để đảm bảo chúng hoạt động đúng cách cũng có thể khả dụng trên các trang web thương mại điện tử. Các chức năng gỡ lỗi và trang thử nghiệm này có thể khiến trang web gặp nguy hiểm khi bị kẻ tấn công tìm thấy.

Sau đây là ví dụ về lỗ hổng bảo mật này:

Một trang web đã gửi một loại thanh toán số đến máy chủ, cùng với các thông số khác cần thiết để hoàn tất giao dịch. Tuy nhiên, việc thay đổi loại thanh toán thành các giá trị số khác có thể buộc ứng dụng phải sử dụng cổng thanh toán thử nghiệm sử dụng các tài khoản thử nghiệm để mô phỏng môi trường thực tế. Điều này cho phép kẻ tấn công hoàn tất giao dịch mà không cần chi tiền thật, chỉ bằng cách kết nối ứng dụng với môi trường thử nghiệm của nó.

Trang đích và tất cả dữ liệu đầu vào trong yêu cầu thanh toán phải được kiểm tra và thử nghiệm để đảm bảo không thể buộc ứng dụng trực tiếp sử dụng dữ liệu thử nghiệm. Ví dụ, đôi khi thay đổi tiêu đề "HOST" trong yêu cầu HTTP thành tên máy chủ nội bộ đã biết được sử dụng để thử nghiệm có thể kích hoạt lỗ hổng này.

Ngoài ra, dữ liệu thử nghiệm thanh toán cụ thể cũng nên được thử nghiệm để đảm bảo rằng không thể sử dụng nó trong môi trường trực tiếp. Ví dụ, trong một ứng dụng, có thể sử dụng dữ liệu thẻ thử nghiệm Sage Pay [9] trong một giao dịch thực tế.

# Currency Arbitrage in Deposit/Buy and Withdrawal/Refund

> Trọng tài tiền tệ trong việc gửi/mua và rút/hoàn tiền

Nếu một ứng dụng thương mại điện tử hỗ trợ các phương thức thanh toán khác nhau với các loại tiền tệ khác nhau, thì một người có thể gửi tiền bằng một loại tiền tệ và rút tiền bằng loại tiền tệ khác. Chênh lệch giá xảy ra khi phương thức gửi tiền và rút tiền khác nhau (chẳng hạn như sử dụng công ty thẻ tín dụng để gửi tiền và PayPal để rút tiền) và họ sử dụng tỷ giá hối đoái không nhất quán.

Ví dụ, hãy tưởng tượng một trang web của bên thứ ba hỗ trợ hai loại thanh toán khác nhau (hãy gọi chúng là Ngân hàng A và B) để gửi hoặc rút tiền vào hoặc ra khỏi trang web. Tỷ giá hối đoái USD sang EUR với hoa hồng là 3/2 (cho 3 đô la cho 2 euro) khi sử dụng Ngân hàng A và tỷ giá hối đoái EUR sang USD là 3/4 khi sử dụng Ngân hàng B (cho 3 euro cho 4 đô la). Bằng cách gửi 8 Euro vào trang web bằng Ngân hàng A, 12 đô la sẽ được gửi (tỷ giá hối đoái = 3/2). Bây giờ, bằng cách rút 12 đô la này khỏi trang web và gửi chúng vào Ngân hàng B, 9 euro sẽ được gửi cho người dùng (tỷ giá hối đoái = 3/4). Điều này cung cấp thêm một euro cho người dùng chỉ gửi 8 euro vào trang web ban đầu.

Một vấn đề phức tạp hơn có thể xảy ra khi một ứng dụng tài chính hỗ trợ chuyển tiền bằng nhiều loại tiền tệ khác nhau, vì có thể khai thác chênh lệch giá nhiều loại tiền tệ (như chênh lệch giá tam
giác) khi phí hoa hồng không đáng kể.

Rất hiếm khi thấy lỗ hổng này trong các ứng dụng ngân hàng và giao dịch, do sử dụng mạng máy tính tốc độ cao có thể báo động để thu hẹp khoảng cách bất cứ khi nào có thể xảy ra chênh lệch giá [3]. Tuy nhiên, một ứng dụng thương mại điện tử cập nhật tỷ giá hối đoái chậm có thể là nạn nhân của kỹ thuật khai thác này.


# Kết luận

In this paper, the following attack methods and testing methodologies were discussed against e-commerce, payment, and trading applications:
- Time-of-Check-Time-of-Use (TOCTOU) and race condition issues
	- Transferring money/points or buying items simultaneously
	- Changing the order upon payment completion
	- Changing the order after payment completion
- Parameter manipulation
	- Price manipulation
	- Currency manipulation
	- Quantity manipulation
	- Shipping address and post method manipulation
	- Additional costs manipulation
	- Response manipulation
	- Repeating an input parameter multiple times
	- Omitting an input parameter or its value
	- Mass assignment, autobinding, or object injection
	- Monitor the behaviour while changing parameters to detect logical flaws
- Replay attacks
	- Replay the call-back request
	- Replay an encrypted parameter
- Rounding issues
	- Currency rounding issues
	- Generic rounding issues between different applications
- Numerical processing
	- Negative numbers
	- Decimal numbers
	- Large or small numbers
	- Overflows and underflows
	- Zero, null, or subnormal numbers
	- Exponential notation
	- Reserved words
	- Numbers in different formats
- Credit card and other payment card related issues
	- Showing a saved card number during the payment process
	- Card number enumeration via registering duplicate cards
- Dynamic prices, prices with tolerance, or referral schemes
- Discount codes, vouchers, offers, reward points, and gift cards
	- Enumeration and guessing
	- Vouchers and offers stacking
	- Earning more points or cash return than the price when buying an item
	- Using expired, invalid, or other users’ codes
	- State and basket manipulation
	- Refund abuse
	- Buy-x-get-y-free
	- Ordering out of stock or unreleased items
	- Bypassing other restrictions
	- Point transfer
- Cryptography Issues
- Downloadable and virtual goods
- Hidden and insecure backend APIs
- Using test data in production environment
- Currency arbitrage in deposit/buy and withdrawal/refund

These attack methods can also be used against other similar applications such as betting and gambling applications, or other financial services platforms.

