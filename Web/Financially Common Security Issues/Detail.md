- **Time-of-Check-Time-of-Use (TOCTOU) and Race Condition Issues**:
    
    - **Definition**: A TOCTOU vulnerability occurs when an application checks a resource's state before using it, but the state changes between the check and the use, invalidating the check. This often happens in concurrent or multi-threaded environments. Race conditions arise when multiple threads access shared resources, leading to unexpected outcomes.
    - **Examples**:
        - **Transferring money or points simultaneously**: A user might be able to transfer the same amount of money twice if the application doesn't properly synchronize access to the account balance. For example, if a user has £100 and two transfer requests of £100 are sent at the same time, the application may process both requests and deduct £200 from the account.
        - **Changing the order upon payment completion**: A user might add a cheap item, begin the checkout process, and then, in another tab, add expensive items to the basket. If the application doesn't re-verify the basket before completing the payment, the user could purchase all items for the price of the cheap one.
        - **Changing the order after payment completion:** After an order is completed, it may be possible to modify the details of the order, invoice or quote, without paying an additional fee. For example, a user may be able to change the details on an insurance certificate to include more expensive items without paying more.
    - **Impact**: Can lead to unauthorized transfers, purchases, or modifications, resulting in financial loss for the application.
- **Parameter Manipulation**:
    
    - **Definition**: Exploiting vulnerabilities by modifying input parameters sent to the server in order to change the application's behavior.
    - **Examples**:
        - **Price Manipulation**: Changing the price of an item to a lower or even negative value. Some applications may ignore the manipulated price initially, but start using it after adding certain types of items to the basket.
        - **Currency Manipulation**: Changing the currency parameter to one of lower value than the requested currency during payment processing. For example, changing the currency from British Pounds to Indian Rupees on a PayPal transaction, and the website authorizing the transaction without checking the currency.
        - **Quantity Manipulation**: Modifying the number of items purchased, including using small or negative numbers. Decimal values may also affect the final price when they should not.
        - **Shipping Address and Post Method Manipulation**: Changing these to alter costs, or to avoid taxes.
        - **Additional Costs Manipulation**: Removing optional costs, like gift wrapping, at the payment stage.
        - **Response Manipulation**: Modifying server responses to bypass license checks or activate in-app purchases without payment.
        - **Repeating Input Parameters**: Sending the same parameter multiple times in a request which could cause logical issues, because different technologies may parse these values differently.
        - **Omitting Input Parameters**: Removing parameters or their values to bypass checks or cause errors.
        - **Mass Assignment/Object Injection**: Including additional parameters to change data, like shipping addresses and due dates on invoices.
        - **Monitoring Parameter Changes**: Observing how changing parameters, even multiple parameters, can expose logical flaws. For example, sending a string value to the delivery type parameter may allow a decimal value to be used for quantity.
    - **Impact**: Allows users to obtain products/services at reduced prices or for free, bypass restrictions, or gain unauthorized access.
- **Replay Attacks**:
    
    - **Definition**: Capturing and re-sending messages to the server, potentially with modifications, to gain unauthorized access or complete fraudulent transactions.
    - **Examples**:
        - **Replaying the call-back request**: Replaying a successful payment callback request to authorize a transaction without paying. For example, replacing the "transaction-id" parameter to complete a payment without spending any money.
        - **Replaying an encrypted parameter**: Reusing an encrypted parameter from a previous request, such as the price, to purchase an item cheaper than intended.
    - **Impact**: Enables users to bypass payment processes, gain unauthorized access, or manipulate data by reusing old requests.
- **Rounding Errors**:
    
    - **Definition**: Inconsistencies or inaccuracies introduced due to the finite precision of numerical variables, or because of different methods of rounding.
    - **Examples**:
        - **Currency Rounding Issues**: Exploiting differences in exchange rate rounding to make a profit when converting between currencies. For example, a user may gain a small profit by converting currencies back and forth if the conversion is not exact and the exchange rate is rounded.
        - **Generic Rounding Issues**: Inconsistencies in rounding between different parts of an application, or between different applications. For example, an application may round to 2 decimal places, while the back end database stores the full number, creating a difference in value.
    - **Impact**: Can lead to financial gain by exploiting small differences between the original and rounded values.
- **Numerical Processing**:
    
    - **Definition**: Problems arising from how numerical data is handled, including negative numbers, decimals, large/small numbers, and formatting.
    - **Examples**:
        - **Negative Numbers**: Using negative numbers to reverse the application logic and gain funds or items.
        - **Decimal Numbers**: Using decimal numbers when only integers are expected, which may cause logical issues or create rounding issues.
        - **Large or Small Numbers**: Inputting numbers outside the expected range to bypass validation checks.
        - **Overflows and Underflows**: Causing integer variables to wrap around to their minimum or maximum values.
        - **Zero, Null, or Subnormal Numbers**: Using these values to bypass checks or manipulate the application logic.
        - **Exponential Notation**: Using exponential notation to bypass length restrictions or create specific values.
        - **Reserved Words**: Using reserved words such as NaN or Infinity in numerical fields.
        - **Numbers in Different Formats**: Using different formats to bypass validation mechanisms. For example, using currency symbols, grouping symbols, or hex values.
    - **Impact**: Leads to logic flaws, financial gain by exploiting unexpected behaviors when using unusual numbers.
- **Card Number-Related Issues**:
    
    - **Definition**: Vulnerabilities related to the handling of payment card numbers, despite compliance with PCI DSS standards.
    - **Examples**:
        - **Showing a Saved Card Number**: Revealing card numbers during the payment process, which could be intercepted by attackers. Unsaved card numbers may also be found in the HTTP responses.
        - **Card Number Enumeration**: Using the duplicate card registration check to guess card numbers registered on the site.
    - **Impact**: Exposure of card numbers leading to potential fraudulent transactions.
- **Dynamic Prices, Prices with Tolerance, or Referral Schemes**:
    
    - **Definition**: Testing for vulnerabilities when prices are not static and can change based on various factors.
    - **Examples**:
        - **Dynamic prices**: Manipulating prices when prices are dynamic due to factors such as currency exchange rates or referral schemes.
        - **Prices with Tolerance**: Prices that are calculated within a certain margin or threshold.
    - **Impact**: Can lead to manipulation of prices, potentially causing financial loss.
- **Discount Codes, Vouchers, Offers, Reward Points, and Gift Cards**:
    
    - **Definition**: Testing vulnerabilities related to the use of discounts, rewards, and gift cards.
    - **Examples**:
        - **Enumeration and Guessing**: Predictable discount or gift card codes.
        - **Vouchers and Offers Stacking**: Combining multiple vouchers or offers that should not be used together.
        - **Earning More Points or Cash Return than the Price When Buying an Item**: Gaining points or cash back when using points to purchase an item.
        - **Using Expired, Invalid, or Other Users’ Codes**: Using codes that have expired, are invalid, or belong to other users.
        - **State and Basket Manipulation**: Changing an order after a discount has been applied.
        - **Refund Abuse**: Earning free points by buying and refunding items.
        - **Buy-X-Get-Y-Free**: Manipulating these offers to get items for free or at a reduced price.
        - **Ordering Out of Stock or Unreleased Items**: Ordering items that are out of stock or not yet released.
        - **Bypassing Other Restrictions**: Bypassing quantity limitations or using customer-specific offers incorrectly.
        - **Point Transfer**: Abusing point transfer features, especially with race conditions.
    - **Impact**: Can lead to loss of revenue, fraudulent purchases, or manipulation of reward systems.
- **Cryptography Issues**:
    
    - **Definition**: Flaws in the implementation or use of cryptography for security purposes.
    - **Examples**:
        - **Using short or insecure secret keys**: Allowing attackers to easily brute-force the key.
        - **Length Extension Attacks**: Exploiting hash functions to append data to a message without knowing the secret key.
        - **Missing Delimiters**: Concatenating values without delimiters when creating a signature hash which allows for manipulation.
        - **Replaying encrypted parameters:** Reusing encrypted values in multiple locations, enabling the decryption of unknown values, or reusing encrypted values from previous requests.
    - **Impact**: Can lead to unauthorized access, data breaches, and manipulation of transactions.
- **Downloadable and Virtual Goods**:
    
    - **Definition**: Issues with direct object reference, where attackers can download or access virtual goods for free by guessing the URLs.
    - **Impact**: Free access to non-free content.
- **Hidden and Insecure Backend APIs**:
    
    - **Definition**: Insecure or improperly secured backend APIs used by payment systems, mobile apps or other connected systems.
    - **Impact**: These APIs may lack protection against attacks and provide access to administrative functions.
- **Using Test Data in Production Environment**:
    
    - **Definition**: Failing to remove test payment methods and dummy data in live environments.
    - **Examples**: Changing payment types to use test payment gateways or using test card data in real transactions.
    - **Impact**: Allows attackers to complete transactions without spending real money.
- **Currency Arbitrage in Deposit/Buy and Withdrawal/Refund**:
    
    - **Definition**: Exploiting differences in exchange rates between different payment methods to gain profit.
    - **Examples**: Depositing money using one method and withdrawing it using another where the exchange rates are not consistent.
    - **Impact**: Can lead to financial losses through the exploitation of exchange rate differences.
