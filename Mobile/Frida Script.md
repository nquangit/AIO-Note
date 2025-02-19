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
	    // List all function/variable from lib
	    let objects = Module.enumerateExports("libfrida0xa.so");
        for (let object of objects) {
            console.log(object.name + ": " + object.address);
        }

		// Hook by address
		// Calling native function from Java
        let get_flag_addr =
            Module.getBaseAddress("libfrida0xa.so").add(0x1dd60); // Get base address of function
        // Native Pointer`
        let getFlagPointer = ptr(get_flag_addr);
        // Native function get_flag(int, int) takes two integer arguments with void return type
        // NativeFunction(ptr, returnType, argsType)
        let get_flag = new NativeFunction(getFlagPointer, "void", [
            "int",
            "int",
        ]);
        get_flag(1, 2);


        // Hook native function by name
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

### Write instruction

> x86

```js
console.log("start Frida");
setTimeout(function () {
    Java.perform(function () {
        // Calling native function from Java
        let addr = Module.getBaseAddress("libfrida0xb.so").add(0x0000); // Get base address of function
        console.log(addr);

		// Edit permission on Memory with size 0x1000
        Memory.protect(addr, 0x1000, "rwx");
        let mem_writer = new X86Writer(addr);
        try {
            // Insert instructions
            mem_writer.putNop();
            mem_writer.putNop();
            mem_writer.putNop();
            mem_writer.putNop();
            mem_writer.putNop();
            mem_writer.putNop();
            // Flush the changes to memory
            mem_writer.flush();
        } finally {
            // Dispose of the X86Writer to free up resources
            mem_writer.dispose();
        }
    });
}, 1000);

```

> arm64

```js
console.log("start Frida");
setTimeout(function () {
    Java.perform(function () {
        // Calling native function from Java
        let addr = Module.getBaseAddress("libfrida0xb.so").add(0x15248); // Get base address of function
        console.log(addr);
        // The target to jmp to
        let target = Module.getBaseAddress("libfrida0xb.so").add(0x1524c);

		// Edit permission on Memory with size 0x1000
        Memory.protect(addr, 0x1000, "rwx");
        let mem_writer = new Arm64Writer(addr);
        try {
            // Insert instructions
            mem_writer.putBImm(target)
            // Flush the changes to memory
            mem_writer.flush();
        } finally {
            // Dispose of the X86Writer to free up resources
            mem_writer.dispose();
        }
    });
}, 1000);
```

