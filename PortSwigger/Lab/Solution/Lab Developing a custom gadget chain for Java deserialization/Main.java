import data.productcatalog.ProductTemplate;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Base64;
import java.io.IOException;
// Scanner
import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the SQL query: ");
        String query = scanner.nextLine();
        ProductTemplate productTemplate = new ProductTemplate(query);
        
        // Serialize the object and encode it to Base64
        try {
            // Convert the object to a byte array (serialization)
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
            objectOutputStream.writeObject(productTemplate);
            objectOutputStream.flush();
            
            // Get the byte array from the output stream
            byte[] serializedBytes = byteArrayOutputStream.toByteArray();
            
            // Convert the byte array to a Base64 string
            String base64String = Base64.getEncoder().encodeToString(serializedBytes);
            
            // Print the Base64-encoded serialized object
            System.out.println("Base64 Serialized ProductTemplate: " + base64String);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
