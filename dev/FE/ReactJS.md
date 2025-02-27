# React Learning notes

---
## 1. React

### 1.1. Introduction

- A frontend JavaScript **framework**, a JavaScript **library** for building UI (user interfaces) created by Facebook.
- Used to build **SPA** (single-page applications) - a web app that **loads only a single web document**, and then **_updates_** the body content of that single document via JavaScript APIs such as Fetch **_when different content is to be shown_**.
- Allows us to create reusable UI components.

### 1.2. Some key concepts

- **Components**: The fundamental building blocks of a React application. A component is a **reusable** piece of code that **_encapsulates_** the **_HTML_**, **_CSS_**, and **_JavaScript_** code required to render a piece of the UI (_they can be simple UI elements like buttons or complex structures like entire pages._)
  - **Function Components**: A Javascript function that accepts **_props_** and returns a **React element** - JSX (JavaScript XML).
  - **Class Components**: A JavaScript class that extends **_React.Component_** and has a **_render_** method that returns a **React element** - JSX (JavaScript XML).
- **JSX**: A syntax extension for JavaScript that looks similar to XML/HTML. It allows us to write HTML-like elements in JavaScript and place them in the DOM without using functions like **_createElement()_** or **_appendChild()_**. (You are not required to use JSX, but JSX makes it easier to write React applications.)

  ```jsx
  // Example of JSX
  const element = <h1>Hello, world!</h1>;
  ```

- **Props**: _Short for properties_, they are used to pass data from a parent component to a child component. They are **_read-only_** and **_immutable_**.

  ```jsx
  // Example of props
  function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
  }
  const element = <Welcome name="Sara" />;
  ```

- **State**: An object that holds some information that may change over the lifetime of the component. It is **_mutable_** and **_private_** to the component that owns it. **_When the state of a component changes, the component automatically re-renders_**.

  ```jsx
  // Example of state
  class Clock extends React.Component {
    constructor(props) {
      super(props);
      this.state = { date: new Date() };
    }
    render() {
      return <h1>It is {this.state.date.toLocaleTimeString()}.</h1>;
    }
  }
  ```

- **Lifecycle Methods**: Methods that are **called automatically** by React **at specific points in the lifecycle of a component**. They are used to perform some actions when the component is created, updated, or destroyed.

  - `componentDidMount()`: Invoked immediately after a component is mounted (inserted into the tree).
  - `componentDidUpdate()`: Invoked immediately after updating occurs.
  - `componentWillUnmount()`: Invoked immediately before a component is unmounted and destroyed.

- **Hooks** (from React 16.8): functions that let you **use state and other React features without writing a class**. They allow you to use state and other React features in functional components.

  - `useState()`: A hook that allows you to add state to a functional component.
  - `useEffect()`: A hook that allows you to perform side effects in functional components.
  - `useContext()`: A hook that allows you to use the context API in functional components.
  - `useReducer()`: A hook that allows you to manage state in functional components.

- **Virtual DOM**: A lightweight copy of the actual DOM. React uses the virtual DOM to **_minimize the number of updates to the actual DOM_**. When the state of a component changes, React **updates the virtual DOM first**, then compares it with the actual DOM, and finally **updates only the parts of the actual DOM that have changed**.

- **ES6** (React uses ES6): ECMAScript 6, also known as ES6 or ECMAScript 2015, is the latest version of the ECMAScript standard. It introduces many new features to JavaScript, such as **_arrow functions_**, **_classes_**, **_let_** and **_const_** declarations, **_template literals_**, **_destructuring_**, and **_spread syntax_**.

### 1.3. How React works

**`React creates a VIRTUAL DOM in memory.`**
**`React only changes what needs to be changed!`**

- **React** creates a **virtual DOM** (in memory) that is a lightweight copy of the actual DOM and **_updates it first_**.
- **React** then **compares** the virtual DOM with the actual DOM and **_updates only the parts of the actual DOM that have changed_**.

#### React render HTML

Use **createRoot()** function and its method render() to render a React element into the DOM.

```jsx
const element = <h1>Hello, world!</h1>;
const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);
root.render(element);
```

- The createRoot Function: Creates a new **Root** object that represents a **_React root_**. It accepts a container element as an argument. Purpose: define the HTML element where a React component should be rendered.
- The render Method: Renders a React element into the DOM. It accepts a React element as an argument. Purpose: render a React element into the DOM.

### 1.4. Implementing React

#### 1.4.1. React directly in HTML

Using **_CDN links_** to include React in an HTML file.

```html
<!-- React library -->
<script src="https://unpkg.com/react@18/umd/react.development.js"></script>
<!-- React DOM library -->
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<!-- Babel, allows us to write JSX syntax and ES6 in older browsers. -->
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
```

```html
<!DOCTYPE html>
<html>
  <head>
    <script
      src="https://unpkg.com/react@18/umd/react.development.js"
      crossorigin
    ></script>
    <script
      src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"
      crossorigin
    ></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  </head>
  <body>
    <div id="mydiv"></div>

    <script type="text/babel">
      function Hello() {
        return <h1>Hello World!</h1>;
      }

      const container = document.getElementById("mydiv");
      const root = ReactDOM.createRoot(container);
      root.render(<Hello />);
    </script>
  </body>
</html>
```

_This way of using React can be OK for testing purposes, but for production you will need to set up a React environment._

#### 1.4.2. Create React App

1. Install **Node.js**.
2. Install **npx** (Node Package Runner) globally.

   ```bash
   npm install -g npx
   ```

3. Create a new React app using **Create React App** named **my-app**.

   ```bash
   npx create-react-app my-app
   ```

4. Change to the **my-app** directory and start the development server.

   ```bash
    cd my-app
    npm start
   ```

5. Open the browser and navigate to **http://localhost:3000/**.

## 1.5. ES6 Features

### 1.5.1. Arrow Functions

- Arrow functions are a more concise way to write functions in JavaScript.

  ```jsx
  // Traditional function
  function add(a, b) {
    return a + b;
  }

  // Arrow function
  const add = (a, b) => {
    a + b;
  };

  // If the function has only one statement, you can omit the curly braces and the return keyword.
  const add = (a, b) => a + b;

  // If the function has only one parameter, you can omit the parentheses.
  const square = (x) => x * x;
  const square = (x) => x * x;
  ```

### 1.5.2. Variable Declarations: var, let, and const

- **var**: The variable declared with **var** is **_function-scoped_**. It means that the variable is available within the function in which it is declared.
- **let**: The variable declared with **let** is **_block-scoped_**. It means that the variable is available within the block in which it is declared.
- **const**: The variable declared with **const** is also **_block-scoped_**. It means that the variable is available within the block in which it is declared. The value of a **const** variable cannot be changed once it is assigned.

  ```jsx
  // var
  function varExample() {
    if (true) {
      var x = 10;
    }
    console.log(x); // 10
  }

  // let
  function letExample() {
    if (true) {
      let x = 10;
    }
    console.log(x); // ReferenceError: x is not defined
  }

  // const
  const PI = 3.14;
  PI = 3.14159; // TypeError: Assignment to constant variable.
  ```

### 1.5.3. Classes

- A class is a type of function, but instead of using the keyword **_function_** to initiate it, we use the keyword **_class_**, and the properties are assigned inside a **_constructor()_** method.

  ```jsx
  class Car {
    constructor(brand) {
      this.carname = brand;
    }
  }

  mycar = new Car("Ford");
  ```

- Methods can be added to a class using the **_class method_** syntax.

  ```jsx
  class Car {
    constructor(brand) {
      this.carname = brand;
    }
    present() {
      return "I have a " + this.carname;
    }
  }

  mycar = new Car("Ford");
  mycar.present();
  ```

- Class Inheritance: The **_extends_** keyword is used in class declarations or class expressions.

  ```jsx
  class Car {
    constructor(brand) {
      this.carname = brand;
    }
    present() {
      return "I have a " + this.carname;
    }
  }

  class Model extends Car {
    constructor(brand, mod) {
      super(brand);
      this.model = mod;
    }
    show() {
      return this.present() + ", it is a " + this.model;
    }
  }

  mycar = new Model("Ford", "Mustang");
  mycar.show();
  ```

### 1.5.4. Array Methods

`There are many JavaScript array methods. Some of the most commonly used array methods are:`

- **map()**: Creates a new array with the results of calling a provided function on every element in the array.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const doubled = numbers.map((number) => number * 2);
  console.log(doubled); // [2, 4, 6, 8, 10]
  ```

- **filter()**: Creates a new array with all elements that pass the test implemented by the provided function.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const even = numbers.filter((number) => number % 2 === 0);
  console.log(even); // [2, 4]
  ```

- **reduce()**: Executes a reducer function on each element of the array, resulting in a single output value.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const sum = numbers.reduce((total, number) => total + number, 0);
  console.log(sum); // 15
  ```

- **forEach()**: Calls a function for each element in the array.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  numbers.forEach((number) => console.log(number));
  ```

- **find()**: Returns the first element in the array that satisfies the provided testing function.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const even = numbers.find((number) => number % 2 === 0);
  console.log(even); // 2
  ```

- **some()**: Tests whether at least one element in the array passes the test implemented by the provided function.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const even = numbers.some((number) => number % 2 === 0);
  console.log(even); // true
  ```

- **every()**: Tests whether all elements in the array pass the test implemented by the provided function.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const even = numbers.every((number) => number % 2 === 0);
  console.log(even); // false
  ```

### 1.5.5. Destructuring

- Destructuring is a JavaScript expression that makes it possible to unpack values from arrays, or properties from objects, into distinct variables.

  ```jsx
  // Array Destructuring
  const numbers = [1, 2, 3];
  const [a, b, c] = numbers;
  console.log(a); // 1
  console.log(b); // 2
  console.log(c); // 3

  // Object Destructuring
  const person = { name: "John", age: 30 };
  const { name, age } = person;
  console.log(name); // John
  console.log(age); // 30
  ```

### 1.5.6. Spread Operator (...)

- The spread operator is used to **expand** an **iterable** object into its individual elements.

  ```jsx
  const numbers = [1, 2, 3];
  const newNumbers = [...numbers, 4, 5];
  console.log(newNumbers); // [1, 2, 3, 4, 5]
  ```

- The spread operator can also be used to **copy** the properties of an object into another object.

  ```jsx
  const person = { name: "John", age: 30 };
  const newPerson = {
    ...person,
  };
  console.log(newPerson); // { name: "John", age: 30 }
  ```

### 1.5.7. Modules

- **Modules** are reusable pieces of code that can be exported from one program and imported for use in another program.
- Rely on the **_export_** and **_import_** statements.

  - Exporting a module: The **_export_** statement is used to export functions, objects, or primitive values from a module.

    - Named Exports: **_export_** keyword is used to export multiple named exports.

      ```jsx
      // Named Exports
      export const PI = 3.14;
      export function add(a, b) {
        return a + b;
      }
      ```

    - Default Exports: **_export default_** keyword is used to export a single default export. (**Only one default export per module**)

    ```jsx
    // Default Export
    const PI = 3.14;
    export default PI;
    ```

  - Import a module: The **_import_** statement is used to import functions, objects, or primitive values from a module. (**Named exports must be destructured using curly braces. Default exports are imported without curly braces.**)

    ```jsx
    // Named Exports
    import { PI, add } from "./math";

    // Default Export
    import PI from "./math";
    ```

### 1.5.8. Ternary Operator

- The **_ternary operator_** is the only JavaScript operator that takes **_three operands_**: a **_condition_** followed by a **_question mark_** (**_?_**), then an **_expression_** to execute if the condition is **_truthy_**, followed by a **_colon_** (**_:_)** and an **_expression_** to execute if the condition is **_falsy_**.

  ```jsx
  const age = 20;
  const message = age >= 18 ? "You are an adult" : "You are a minor";
  console.log(message); // You are an adult
  ```

## 1.6. React JSX

You are not required to use JSX, but JSX makes it easier to write React applications.

```jsx
// Example of JSX
const element = <h1>Hello, world!</h1>;

// Example of without JSX
const element = React.createElement("h1", null, "Hello, world!");
```

### 1.6.1. JSX Expressions

- JSX expressions are JavaScript expressions that can be used in JSX.

  ```jsx
  const name = "John";
  const element = <h1>Hello, {name}</h1>;
  const myElement = <h1>React is {5 + 5} times better with JSX</h1>;
  ```

- JSX expressions can be used in attributes.

  ```jsx
  const url = "https://www.example.com";
  const element = <a href={url}>Click here</a>;
  ```

- JSX expressions can be used in loops.

  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const list = numbers.map((number) => <li>{number}</li>);
  const element = <ul>{list}</ul>;
  ```

### 1.6.2. Insert large blocks of HTML

- To insert large blocks of HTML, you can use **_parentheses_**.

  ```jsx
  const element = (
    <div>
      <h1>Hello, world!</h1>
      <p>Welcome to React</p>
    </div>
  );
  ```

### 1.6.3. One top level element

- In JSX, you must have only one top-level element.

  ```jsx
  // This will throw an error
  const element = <h1>Hello, world!</h1> <p>Welcome to React</p>;

  // This is correct
  const element = (
    <div>
      <h1>Hello, world!</h1>
      <p>Welcome to React</p>
    </div>
  );
  ```

- You can use **_React.Fragment_** to group multiple elements without adding an extra node to the DOM.

  ```jsx
  const element = (
    <>
      <h1>Hello, world!</h1>
      <p>Welcome to React</p>
    </>
  );
  ```

### 1.6.4. Element must be closed

- In JSX, you must close all elements.

  ```jsx
  // This will throw an error
  const element = <input type="text">;

  // This is correct
  const element = <input type="text" />;
  ```

### 1.6.5. Attributes in JSX

- In JSX, you can use **_attributes_** to add **_HTML attributes_** to elements.

  ```jsx
  const element = <img src="image.jpg" alt="My Image" />;
  ```

- **class** attribute is replaced with **_className_** in JSX.

  ```jsx
  const element = <div className="container">Hello, world!</div>;
  ```

### 1.6.6. Style attribute in JSX

- In JSX, you can use the **_style_** attribute to add **_inline styles_** to elements.

  ```jsx
  const myStyle = {
    color: "red",
    fontSize: "20px",
  };
  const element = <h1 style={myStyle}>Hello, world!</h1>;
  ```

## 1.7. React Components

We have 2 types of components in React:

- **Function Components**: A JavaScript function that accepts **_props_** and returns a **React element**.
- **Class Components**: A JavaScript class that extends **_React.Component_** and has a **_render_** method that returns a **React element**.

### 1.7.1. Create first React component

- **Function Component**:

  ```jsx
  function Welcome(props) {
    return <h1>Hello, world</h1>;
  }

  const element = <Welcome />;
  ```

- **Class Component**:

  ```jsx
  class Welcome extends React.Component {
    render() {
      return <h1>Hello, world</h1>;
    }
  }

  const element = <Welcome />;
  ```

### 1.7.2. Rendering a Component

- To render a React component into the DOM, you can use the **_ReactDOM.render()_** method.

  ```jsx
  const element = <Welcome />;
  ReactDOM.createRoot(document.getElementById("root"));
  root.render(element); // Or root.render(<Welcome />);
  ```

### 1.7.3. Props

- **Props** are used to pass data from a parent component to a child component.

  ```jsx
  // props in Function Component
  function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
  }

  const element = <Welcome name="John" />;

  // props in Class Component
  class Welcome extends React.Component {
    render() {
      return <h1>Hello, {this.props.name}</h1>;
    }
  }

  const element = <Welcome name="John" />;
  ```

### 1.7.4. Components in components

- You can use components inside other components.

  ```jsx
  function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
  }

  function App() {
    return (
      <div>
        <Welcome name="John" />
        <Welcome name="Sara" />
        <Welcome name="Mike" />
      </div>
    );
  }

  const element = <App />;
  ```

### 1.7.5. Component in a file

- You can create a component in a separate file and import it into another file.

  ```jsx
  // Welcome.js
  function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
  }

  export default Welcome;
  ```

  ```jsx
  // App.js
  import Welcome from "./Welcome";

  function App() {
    return (
      <div>
        <Welcome name="John" />
        <Welcome name="Sara" />
        <Welcome name="Mike" />
      </div>
    );
  }

  export default App;
  ```

  ```jsx
  // index.js
  import App from "./App";

  const element = <App />;
  ReactDOM.createRoot(document.getElementById("root"));
  root.render(element);
  ```

### 1.7.6. React Class

##### Note:

- Before React 16.8, class components were the only way to create stateful components in React.
- With the introduction of **_Hooks_** in React 16.8, you can now use state and other React features in functional components.
- The differences are so minor that you will probably never need to use a Class component in React.
- Feel free to skip this section, and use Function Components instead.

#### 1.7.6.1. Class Component

- A class component is a JavaScript class that extends **_React.Component_**. The component's name must start with an upper case letter.

  ```jsx
  class Welcome extends React.Component {
    render() {
      return <h1>Hello, world</h1>;
    }
  }

  const element = <Welcome />;
  ```

#### 1.7.6.2. Constructor

- The **_constructor_** method is a special method for creating and initializing an object created with a class.

  ```jsx
  class Welcome extends React.Component {
    constructor(props) {
      super(props);
      this.state = { name: "John" };
    }
    render() {
      return <h1>Hello, {this.state.name}</h1>;
    }
  }

  const element = <Welcome />;
  ```

#### 1.7.6.3. Props

- You can access **_props_** in a class component using **_this.props_**.

  ```jsx
  class Welcome extends React.Component {
    render() {
      return <h1>Hello, {this.props.name}</h1>;
    }
  }

  const element = <Welcome name="John" />;
  ```

#### 1.7.6.4. State

- **State** is an object that holds some information that may change over the lifetime of the component.

  ```jsx
  class Welcome extends React.Component {
    constructor(props) {
      super(props);
      this.state = { name: "John" };
    }
    render() {
      return <h1>Hello, {this.state.name}</h1>;
    }
  }

  const element = <Welcome />;
  ```

### 1.7.7. React Props

- **Props** are used to pass data from a parent component to a child component.
- React Props are read-only! You will get an error if you try to change their value.

  ```jsx
  // Function Component
  function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
  }

  const element = <Welcome name="John" />;

  // Class Component
  class Welcome extends React.Component {
    render() {
      return <h1>Hello, {this.props.name}</h1>;
    }
  }

  const element = <Welcome name="John" />;
  ```

- We can pass variables, functions, or objects as props.

  ```jsx
  // Passing variables
  const name = "John";
  const element = <Welcome name={name} />;

  // Passing functions
  function handleClick() {
    alert("Button clicked");
  }
  const element = <button onClick={handleClick}>Click me</button>;

  // Passing objects
  const person = { name: "John", age: 30 };
  const element = <Welcome person={person} />;
  ```

### 1.7.8. React Events

- **Events** are actions that occur when a user interacts with a web page.

  ```jsx
  function handleClick() {
    alert("Button clicked");
  }

  const element = <button onClick={handleClick}>Click me</button>;
  ```

- **Event handlers** are functions that are executed when an event occurs.

### 1.7.9. React Forms

- **Forms** are used to collect user input in a web page.

  ```jsx
  function MyForm() {
    return (
      <form>
        <label>
          Enter your name:
          <input type="text" />
        </label>
      </form>
    );
  }
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<MyForm />);
  ```

- Handling Forms:
  | HTML | React |
  |---|---|
  | Form data is usually handled by the DOM | - Form data is usually handled by the components<br>- The data is stored in the component state |

  - Control changes by adding event handlers in the onChange attribute.
  - Use the useState Hook to keep track of each inputs value and provide a "single source of truth" for the entire application.

  ```jsx
  function MyForm() {
    const [name, setName] = React.useState("");
    const handleChange = (event) => {
      setName(event.target.value);
    };
    return (
      <form>
        <label>
          Enter your name:
          <input type="text" value={name} onChange={handleChange} />
        </label>
        <p>Your name is: {name}</p>
      </form>
    );
  }
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<MyForm />);
  ```

- Submitting Forms:

  - Use the onSubmit attribute to specify a function that will be called when the form is submitted.
  - Use the preventDefault() method to prevent the default action of the form.

  ```jsx
  function MyForm() {
    const [name, setName] = React.useState("");
    const handleSubmit = (event) => {
      event.preventDefault();
      alert("Form submitted");
    };
    const handleChange = (event) => {
      setName(event.target.value);
    };
    return (
      <form onSubmit={handleSubmit}>
        <label>
          Enter your name:
          <input type="text" value={name} onChange={handleChange} />
        </label>
        <button type="submit">Submit</button>
      </form>
    );
  }
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<MyForm />);
  ```

- Multiple input fields:

  - Use the **_name_** attribute to specify the name of the input field.
  - Use the **_value_** attribute to specify the value of the input field.
  - Use the **_onChange_** attribute to specify a function that will be called when the input field changes.

  ```jsx
  import { useState } from "react";
  import ReactDOM from "react-dom/client";

  function MyForm() {
    const [inputs, setInputs] = useState({});

    const handleChange = (event) => {
      const name = event.target.name;
      const value = event.target.value;
      setInputs((values) => ({ ...values, [name]: value }));
    };

    const handleSubmit = (event) => {
      event.preventDefault();
      alert(inputs);
    };

    return (
      <form onSubmit={handleSubmit}>
        <label>
          Enter your name:
          <input
            type="text"
            name="username"
            value={inputs.username || ""}
            onChange={handleChange}
          />
        </label>
        <label>
          Enter your age:
          <input
            type="number"
            name="age"
            value={inputs.age || ""}
            onChange={handleChange}
          />
        </label>
        <input type="submit" />
      </form>
    );
  }

  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<MyForm />);
  ```

- Textarea:

  - Use the **_textarea_** element to create a multi-line text input field.
  - Use the **_value_** attribute to specify the value of the textarea.
  - Use the **_onChange_** attribute to specify a function that will be called when the textarea changes.

  ```jsx
  function MyForm() {
    const [message, setMessage] = React.useState("");
    const handleChange = (event) => {
      setMessage(event.target.value);
    };
    return (
      <form>
        <label>
          Enter your message:
          <textarea value={message} onChange={handleChange} />
        </label>
        <p>Your message is: {message}</p>
      </form>
    );
  }
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<MyForm />);
  ```

- Select:

  - Use the **_select_** element to create a drop-down list.
  - Use the **_value_** attribute to specify the value of the select element.
  - Use the **_onChange_** attribute to specify a function that will be called when the select element changes.

  ```jsx
  function MyForm() {
    const [fruit, setFruit] = React.useState("apple");
    const handleChange = (event) => {
      setFruit(event.target.value);
    };
    return (
      <form>
        <label>
          Select your favorite fruit:
          <select value={fruit} onChange={handleChange}>
            <option value="apple">Apple</option>
            <option value="banana">Banana</option>
            <option value="orange">Orange</option>
          </select>
        </label>
        <p>Your favorite fruit is: {fruit}</p>
      </form>
    );
  }
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<MyForm />);
  ```

## 1.8. React Router

- _Create React App doesn't include page routing._
- **React Router** is a collection of navigational components that compose declaratively with your application.

  ```bash
  npm i -D react-router-dom
  ```

### 1.8.1. Folder Structure

- **src**: Contains the source code of the application.
- **src/components**: Contains the components of the application.
- **src/pages**: Contains the pages of the application.
- **src/App.js**: The main component of the application.

`src\pages\:`

- `Home.js`: The Home page of the application.
- `Layout.js`: The layout component of the application.
- `Blog.js`: The Blog page of the application.
- `Contact.js`: The Contact page of the application.
- `NoPage.js`: The 404 page of the application.

#### 1.8.2. Basic Usage

```jsx
// index.js
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import Home from "./pages/Home";
import Blogs from "./pages/Blogs";
import Contact from "./pages/Contact";
import NoPage from "./pages/NoPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="blogs" element={<Blogs />} />
          <Route path="contact" element={<Contact />} />
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
```

Explain:

- **BrowserRouter**: A router that uses the HTML5 history API to keep your UI in sync with the URL.
- **Routes**: A collection of routes that render their children when their path matches the current URL. An application can have multiple `<Routes>`.
- **Route**: A route that renders its children when its path matches the current URL. `<Route>s` can be nested.
  - The `index` attribute is used to specify the default route (`/`).
  - Setting path to `*` will match all paths that are not matched by other routes.

#### 1.8.3 Pages / Components

```jsx
// Layout.js
import { Outlet, Link } from "react-router-dom";

const Layout = () => {
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/blogs">Blogs</Link>
          </li>
          <li>
            <Link to="/contact">Contact</Link>
          </li>
        </ul>
      </nav>

      <Outlet />
    </>
  );
};

export default Layout;
```

```jsx
// Home.js
const Home = () => {
  return <h1>Home Page</h1>;
};

export default Home;
```

```jsx
// Blogs.js
const Blogs = () => {
  return <h1>Blogs Page</h1>;
};

export default Blogs;
```

```jsx
// Contact.js
const Contact = () => {
  return <h1>Contact Page</h1>;
};

export default Contact;
```

```jsx
// NoPage.js
const NoPage = () => {
  return <h1>404 Page</h1>;
};

export default NoPage;
```

Explain:

- The Layout component has `<Outlet>` and `<Link>` elements.
- The `<Outlet>` renders the current route selected.
- `<Link>` is used to set the URL and keep track of browsing history.
- Anytime we link to an internal path, we will use `<Link>` instead of `<a href="">`.
- The "layout route" is a shared component that inserts common content on all pages, such as a navigation menu.

## 1.9. React Hooks

- Allow function components to use state and other React features without writing a class.

### 1.9.1. What is a Hook?

- **Hooks** are functions that let you use state and other React features in functional components.
- **Hooks** are a new addition in React 16.8.
- **Hooks** don't work inside classes.

#### Hook rules

- **Only call Hooks at the top level**: Don't call Hooks inside loops, conditions, or nested functions.
- **Only call Hooks from React functions**: Call Hooks from React function components and not just any regular JavaScript function or class.
- **Hooks cannot be conditional**: Don't call Hooks conditionally.

### 1.9.2. useState()

To use state in a functional component, you can use the **_useState()_** Hook.

```jsx
import { useState } from "react";
```

- **useState()** is a Hook that allows you to add state to a functional component.

  ```jsx
  import { useState } from "react";

  function Counter() {
    const [count, setCount] = useState(0);
    return (
      <div>
        <p>You clicked {count} times</p>
        <button onClick={() => setCount(count + 1)}>Click me</button>
      </div>
    );
  }
  ```

#### Initializing State

**useState()** accepts an argument that represents the initial state value.

```jsx
import { useState } from "react";

function FavoriteColor() {
  const [color, setColor] = useState("");
}
```

#### Reading State

```jsx
import { useState } from "react";
import ReactDOM from "react-dom/client";

function FavoriteColor() {
  const [color, setColor] = useState("red");

  return <h1>My favorite color is {color}!</h1>;
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<FavoriteColor />);
```

#### Updating State

To update our state, we use our state updater function. This function will update the state and re-render the component.
**We should never directly update state. Ex: color = "red" is not allowed.**

```jsx
import { useState } from "react";
import ReactDOM from "react-dom/client";

function FavoriteColor() {
  const [color, setColor] = useState("red");

  return (
    <>
      <h1>My favorite color is {color}!</h1>
      <button type="button" onClick={() => setColor("blue")}>
        Blue
      </button>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<FavoriteColor />);
```

#### What Can State Hold

**useState()** can hold any type of data, such as strings, numbers, arrays, and objects.

```jsx
const [name, setName] = useState("John");
const [age, setAge] = useState(30);
const [colors, setColors] = useState(["red", "green", "blue"]);
const [person, setPerson] = useState({ name: "John", age: 30 });
```

#### Updating State Based on Previous State

When updating state based on the previous state, you can pass a function to **_setState()_**.

```jsx
const [count, setCount] = useState(0);

const increment = () => {
  setCount((prevCount) => prevCount + 1);
};
```

#### Updating State Based on Previous State (Object)

When updating state based on the previous state (object), you can pass a function to **_setState()_**.

```jsx
const [person, setPerson] = useState({ name: "John", age: 30 });

const updatePerson = () => {
  setPerson((prevPerson) => {
    return { ...prevPerson, age: prevPerson.age + 1 };
  });
};
```

### 1.9.3. useEffect()

- The **_useEffect()_** Hook is used to perform side effects in a functional component.
- Some examples of side effects are: fetching data, directly updating the DOM, and timers.

- `useEffect` accepts two arguments. The second argument is optional.

  ```jsx
  useEffect(() => {
    // Side effect
  }, [dependencies]);

  // Or
  useEffect(<function>, [dependencies])
  ```

Example:

```jsx
// Use setTimeout() to count 1 second after initial render:
import { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";

function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setTimeout(() => {
      setCount((count) => count + 1);
    }, 1000);
  });

  return <h1>I've rendered {count} times!</h1>;
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Timer />);
```

- useEffect runs on every render by default.
- To run useEffect only once, pass an empty array as the second argument.

  ```jsx
  useEffect(() => {
    // Side effect
  }, []);
  ```

- To run useEffect only when a specific value changes, pass that value in the array.

  ```jsx
  import { useState, useEffect } from "react";
  import ReactDOM from "react-dom/client";

  function Counter() {
    const [count, setCount] = useState(0);
    const [calculation, setCalculation] = useState(0);

    useEffect(() => {
      setCalculation(() => count * 2);
    }, [count]); // <- add the count variable here and if the count variable updates, the effect will run again:

    return (
      <>
        <p>Count: {count}</p>
        <button onClick={() => setCount((c) => c + 1)}>+</button>
        <p>Calculation: {calculation}</p>
      </>
    );
  }

  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<Counter />);
  ```

#### Cleanup

- **_useEffect()_** can return a function that will be called when the component is unmounted or before the effect runs again.

  ```jsx
  useEffect(() => {
    // Side effect
    return () => {
      // Cleanup
    };
  }, []);
  ```

  ```jsx
  useEffect(() => {
    // Note: To clear the timer, we had to name it.
    const interval = setInterval(() => {
      // Side effect
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, []);
  ```

### 1.9.4. useContext()

- The **_useContext()_** is a way to manage state globally.
- The **_useContext()_** Hook is used to access the value of a context.

#### Create a Context

- Create a context using the **_createContext()_** function.

  ```jsx
  import { useState, createContext } from "react";
  import ReactDOM from "react-dom/client";

  const UserContext = createContext();
  ```

#### Provide a Context

- Use the **_Provider_** component to provide the context value to its children.

  ```jsx
  const App = () => {
    const [user, setUser] = useState("John");

    return (
      <UserContext.Provider value={user}>
        <h1>{`Hello ${user}!`}</h1>
        <Component2 user={user} />
      </UserContext.Provider>
    );
  };
  ```

  Now, all components in this tree will have access to the user Context.

#### Use a Context

- Use the **_useContext()_** Hook to access the value of a context.

  ```jsx
  import { useState, createContext, useContext } from "react";

  const Component2 = () => {
    const user = useContext(UserContext);

    return <h2>{`Hello ${user}!`}</h2>;
  };
  ```

#### Full Example

```jsx
import { useState, createContext, useContext } from "react";
import ReactDOM from "react-dom/client";

const UserContext = createContext();

function Component1() {
  const [user, setUser] = useState("Jesse Hall");

  return (
    <UserContext.Provider value={user}>
      <h1>{`Hello ${user}!`}</h1>
      <Component2 />
    </UserContext.Provider>
  );
}

function Component2() {
  return (
    <>
      <h1>Component 2</h1>
      <Component3 />
    </>
  );
}

function Component3() {
  return (
    <>
      <h1>Component 3</h1>
      <Component4 />
    </>
  );
}

function Component4() {
  return (
    <>
      <h1>Component 4</h1>
      <Component5 />
    </>
  );
}

function Component5() {
  const user = useContext(UserContext);

  return (
    <>
      <h1>Component 5</h1>
      <h2>{`Hello ${user} again!`}</h2>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Component1 />);
```

### 1.9.5. useRef()

- The **_useRef()_** Hook is used to create a mutable reference that persists for the lifetime of the component.
- It can be used to access a DOM element directly.

#### Does Not Cause Re-renders

- **_useRef()_** does not cause re-renders when the value changes.

  ```jsx
  // Use useRef to track application renders.
  import { useState, useEffect, useRef } from "react";
  import ReactDOM from "react-dom/client";

  function App() {
    const [inputValue, setInputValue] = useState("");
    const count = useRef(0);

    useEffect(() => {
      count.current = count.current + 1;
    });

    return (
      <>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
        <h1>Render Count: {count.current}</h1>
      </>
    );
  }

  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<App />);
  ```

- `useRef()` only returns one item. It returns an Object called `current`.
- It's like doing this: `const count = {current: 0}`. We can access the count by using `count.current`.

#### Accessing DOM Elements

- **_useRef()_** can be used to access DOM elements directly.

  ```jsx
  import { useRef } from "react";

  function App() {
    const inputRef = useRef();

    const handleClick = () => {
      inputRef.current.focus();
    };

    return (
      <>
        <input type="text" ref={inputRef} />
        <button onClick={handleClick}>Focus</button>
      </>
    );
  }
  ```

#### Tracking state changes

```jsx
// Use useRef to keep track of previous state values:
import { useState, useEffect, useRef } from "react";
import ReactDOM from "react-dom/client";

function App() {
  const [inputValue, setInputValue] = useState("");
  const previousInputValue = useRef("");

  useEffect(() => {
    previousInputValue.current = inputValue;
  }, [inputValue]);

  return (
    <>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <h2>Current Value: {inputValue}</h2>
      <h2>Previous Value: {previousInputValue.current}</h2>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
```

### 1.9.6. useReducer()

- The **_useReducer()_** Hook is used to manage complex state logic in a component.
- It is similar to **_useState()_**, but it accepts a reducer function with the current state and an action.

#### Syntax

```jsx
// useReducer(<reducer>, <initialState>)
const [state, dispatch] = useReducer(reducer, initialState);
```

- The reducer function contains your custom state logic and the initialState can be a simple value but generally will contain an object.
- The useReducer Hook returns the current state and a dispatch method.

#### Usage

```jsx
import { useReducer } from "react";
import ReactDOM from "react-dom/client";

const initialTodos = [
  {
    id: 1,
    title: "Todo 1",
    complete: false,
  },
  {
    id: 2,
    title: "Todo 2",
    complete: false,
  },
];

const reducer = (state, action) => {
  switch (action.type) {
    case "COMPLETE":
      return state.map((todo) => {
        if (todo.id === action.id) {
          return { ...todo, complete: !todo.complete };
        } else {
          return todo;
        }
      });
    default:
      return state;
  }
};

function Todos() {
  const [todos, dispatch] = useReducer(reducer, initialTodos);

  const handleComplete = (todo) => {
    dispatch({ type: "COMPLETE", id: todo.id });
  };

  return (
    <>
      {todos.map((todo) => (
        <div key={todo.id}>
          <label>
            <input
              type="checkbox"
              checked={todo.complete}
              onChange={() => handleComplete(todo)}
            />
            {todo.title}
          </label>
        </div>
      ))}
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Todos />);
```

- This is just the logic to keep track of the todo complete status.
- All of the logic to add, delete, and complete a todo could be contained within a single useReducer Hook by adding more actions.

### 1.9.7. useCallback()

- The **_useCallback()_** Hook is used to memoize functions.
- It returns a memoized version of the callback function that only changes if one of the dependencies has changed.

#### Note: Not done yet

### 1.9.8. useMemo()

- The **_useMemo()_** Hook is used to memoize values.
- It returns a memoized value that only changes when one of the dependencies has changed.
- It is similar to **_useCallback()_**, but it is used for memoizing values instead of functions.

#### Note: Not done yet
