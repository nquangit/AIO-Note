# Note:

- Java.choose: Use if you want to use the current running instance of the class
- Java.use: Use like a normal imported class

## Java.choose template

```js
console.log("Frida started");
setTimeout(function () {
    Java.perform(function () {
        Java.choose("<package_name>.<class_name>", {
            onMatch: function (instance) {
                console.log("Found instance: " + instance);
                // Call the method from this instance
                instance.<method_name>(args);
            },
            onComplete: function () {
                console.log("Search completed");
            }
        });
    });
}, 1000);
```

## Java.use template

```js
console.log("Frida started");
setTimeout(function () {
    Java.perform(function () {
        let MainActivity = Java.use("com.ad2001.frida0x1.MainActivity");
        // Reimplement the method
        MainActivity.<method_name>.implementation = function () {
            return 0;
        };
        
        // Reimplement constructor method
        let Checker = Java.use("com.ad2001.frida0x7.Checker");
        Checker.$init.implementation = function (params) {
            this.$init(999, 999);
        }
        
		// Calling a static method
		MainActivity.<static_method>();

		// Overload a method
		hook.<method_name>.overload("int", "int").implementation = function (a, b) {
                this.<method_name>(4, 12); // this.method(args)
        };

		// Load a class and create a new instance
		let class_object = Java.use("<package_name>.<class_name>");
		let class_instance = Check.$new();
		// Calling method
		class_instance.<method_name>(args);
    });
}, 0);
```


## Native hook

```js
console.log("Frida started");
setTimeout(function () {
    Java.perform(function () {
        // Because the frida0x8 is a native lib compiled by C, so we need to find the strcmp function in libc.so
        let strcmp_addr = Module.findExportByName("libc.so", "strcmp");

        console.log("Found strcmp address: " + strcmp_addr);

        Interceptor.attach(strcmp_addr, {
            onEnter: function (args) {
                let firstArg = Memory.readCString(args[0]);
                let secondArg = Memory.readCString(args[1]);
                // Submit the input with value: frida0x8 to get the flag
                if (firstArg == "frida0x8") {
                    console.log("strcmp firstArg: " + firstArg);
                    console.log("strcmp secondArg: " + secondArg);
                }
            },
            onLeave: function (retval) {
                // Replace the return value
                retval.replace(0x539); // return 1337;
            },
        });
    });
}, 1000);
```

