# PYC Documentation

## Datatypes

PYC offers three main data types: `int`, `float`, and `string`. Arrays and multidimensional arrays of all datatypes are supported. Converting between datatypes is possible via casting.

## Declaration of Variables and Arrays

Variables in C must be declared before they can be used. The syntax for declaring a variable is:

```c
data_type variable_name;
```

Here, `data_type` represents the type of data that the variable will store. `variable_name` is the name of the variable.

Arrays can also be declared in a similar way, using the following syntax:

```c
data_type array_name[size];
```

Here, `data_type` is the type of data that the array will store, `array_name` is the name of the array, and `size` is the number of elements in the array.

```c
int main() {
    int a = 5;
    float b = 3.14;
    string c = "abcde";
    int arr[5] = {1, 2, 3, 4, 5};
    return 0;
}
```

## Input and Output

To read input from the user, you can use the `scan()` function. The `print()` function can be used to display output to the user. Note that `scan()` returns a string, which must be casted to other datatypes. Similarly, `print()` takes in a string as an argument, so the argument must be casted to a string.

```c
int main() {
    print("Enter your age: ");
    int age = (int) scan();
    print("Your age is " + (string) age);
    return 0;
}
```

## Control Structures

PYC provides a number of control structures, such as `if-else`, `while`, `do-while`, and `for`, that allow you to control the flow of your program based on certain conditions.

### if-else

The `if-else` statement executes different blocks of code based on the result of a conditional expression. The `if` block is executed `if` the expression is true, while the else block (if present) is executed if the expression is false. You can use `else if` statements to test multiple conditions in sequence.

```c
int main() {
    int a = 5;
    if (a > 10) {
        print("a is greater than 10\n");
    } else if (a < 10) {
        print("a is less than 10\n");
    } else {
        print("a is equal to 10\n");
    }
    return 0;
}
```

### while

The `while` loop is used to execute a block of code repeatedly while a certain condition is true.

```c
int main() {
    int i = 1;
    while (i <= 5) {
        print((string) i + "\n");
        i += 1;
    }
    return 0;
}
```

### for

The `for` loop is a control flow statement that iterates a specific number of times. It consists of an initialization expression, a conditional expression, and an increment/decrement expression. The initialization expression is executed once at the beginning of the loop, the conditional expression is evaluated at the beginning of each iteration, and the increment/decrement expression is executed at the end of each iteration. If the conditional expression is true, the loop continues to execute; otherwise, the loop terminates.

```c
int main() {
    for (int i = 1; i <= 5; i += 1) {
        print((string) i + "\n");
    }
    return 0;
}
```

## Functions

Functions are a way to organize your code into reusable blocks. A function consists of a set of statements that perform a specific task. The basic syntax for defining a function is:

```c
return_type function_name(parameters) {
    // function body
}
```

Here, `return_type` is the type of value that the function will return, `function_name` is the name of the function, and `parameters` are the input values that the function will use.

```c
int sum(int a, int b) {
    return a + b;
}

int main() {
    int x = 5;
    int y = 10;
    int result = sum(x, y);
    print("The sum of " + (string) x + " and " + (string) y + " is " + (string) result + "\n");
    return 0;
}
```
