# Getting Started

> - [Python tutorial for beginners.](https://www.liaoxuefeng.com/wiki/1016959663602400)
> - [Python Tutorial](https://docs.python.org/zh-cn/3/tutorial/index.html)
> - [Python Language Reference - gives a more formal definition of the language.](https://docs.python.org/zh-cn/3/reference/index.html#reference-index)
> - [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
> - [Python Unittest](https://docs.python.org/zh-cn/3/library/unittest.html)
> - [Pyahocorasick - a fast and memory efficient library for exact or approximate multi-pattern string search.](https://pyahocorasick.readthedocs.io/en/latest/)
> - [bisect - Array bisection algorithm - to implement a sorted list.](https://docs.python.org/zh-cn/2/library/bisect.html)
> - [Sorted containers.](https://grantjenks.com/docs/sortedcontainers/)
> - [Python functions](https://docs.python.org/zh-cn/3/library/functions.html#enumerate)

## Setting up

> - [How to install Packages in Python?](https://packaging.python.org/en/latest/tutorials/installing-packages/#requirements-for-installing-packages)
> - [PIPY mirror - 清华镜像](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)

### Setting up mirrors in Chain

```bash
# Get the location of pip conf
pip3 config -v list

# Set up user-level mirroring
pip config set user.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Set up user-level mirroring
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Add other mirror sources
pip config set user.extra-index-url "<url1> <url2>..."
```

### Creating Virtual Environments

Python “Virtual Environments” allow Python [packages](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) to be installed in an isolated location for a particular application, rather than being installed globally.

1. Switch into your project.

```bash
cd helloworld
```

2. Create a virtual environment.

```bash
# python -m venv <venv_dir>
python -m venv .venv/helloworld
```

3. Activate the virtual env. Windows users should not use the ‘source‘ command, but should rather run the activate script directly from the command shell like so:

```bash
.venv/helloworld/Scripts/activate
> (helloworld) ~/helloworld>
```

When you activate a virtual environment in a terminal, the name of the virtual environment is often displayed in the terminal prompt to indicate that the virtual environment is currently active.
4. Install packages.

```bash
pip3 install -r requirements.txt

# Install specified version.
pip3 install <package[==version]>
```

5. execute python scripts.

```bash
python helloword.py
```

6. Exits virtual Environment.

```bash
deactivate
```

>[!warning]
>When using Visual Studio Code (VS Code) as your IDE and working with Python virtual environments, you typically need to specify the Python interpreter provided by the virtual environment for your project.
>If Visual Studio Code (VS Code) does not automatically detect the Python interpreter provided by the virtual environment, you need manually add it.
>
### Import Modules

1. The `sys.modules` dictionary stores the mapping of module names to modules. This dictionary records the mapping when we import a module first. Python looks up this dictionary when we import modules later on. This helps to improve the lookup speed. Try the code follows to show the mapping of already imported modules:

```python
import sys 
# Print the mapping of module names to modules 
for module_name, module in sys.modules.items(): 
 print(module_name, "->", module)
```

## Identifiers and keywords

- [Reserved classes of identifiers.](https://docs.python.org/3/reference/lexical_analysis.html#reserved-classes-of-identifiers)
  - [Private name mangling.](https://docs.python.org/3/reference/expressions.html#atom-identifiers)
  - [Private Variables of classes.](https://docs.python.org/3/tutorial/classes.html#private-variables)

**Reserved classes of identifiers**

Certain classes of identifiers(besides keywords) have speical meanings. These classes are identified by the partterns of leading and trailing underscore characters:

`_*`:

Not imported by `from module import *`.

`_`:

In a case pattern within a [match](https://docs.python.org/3/reference/compound_stmts.html#match) statement, `_` is a [soft keyword](https://docs.python.org/3/reference/lexical_analysis.html#soft-keywords) that denotes a [wildcard](https://docs.python.org/3/reference/compound_stmts.html#wildcard-patterns).

Separately, the interactive interpreter makes the result of the last evaluation available in the variable `_`. (It is stored in the [builtins](https://docs.python.org/3/library/builtins.html#module-builtins) module,  alongside built-in functions like `print`.)

`__*__`:

System-defined names, informally known as “dunder” names. These names are defined by the interpreter and its implementation (including the standard library). Current system names are discussed in the [Special method names](https://docs.python.org/3/reference/datamodel.html#specialnames) section and elsewhere. More will likely be defined in future versions of Python. _Any_ use of `__*__` names, in any context, that does not follow explicitly documented use, is subject to breakage without warning.

`__*`:

Class-private names. Names in this category, when used within the context of a class definition, are re-written to use a mangled form to help avoid name clashes between “private” attributes of base and derived classes. See section [Identifiers (Names)](https://docs.python.org/3/reference/expressions.html#atom-identifiers).

[Private Variables of classes.](https://docs.python.org/3/tutorial/classes.html#private-variables)

## Data Type

### Implement a TreeMap

**Requirement**

1. support floorKey/lowerKey & ceilKey/higherKey operations.
2. support floorEntry/lowerEntry & ceilEntry/higherEntry operations.
3. support headMap & tailMap opertaions.
4. support all standard dict methods.

**Ideas**

1. collections.OrderedDict + [bisect](https://docs.python.org/zh-cn/2/library/bisect.html).
2. [https://pypi.python.org/pypi/bintrees/0.4.0](https://pypi.python.org/pypi/bintrees/0.4.0 "https://pypi.python.org/pypi/bintrees/0.4.0")
3. <https://grantjenks.com/docs/sortedcontainers/>
4. <https://pyahocorasick.readthedocs.io/en/latest/>
5. <https://docs.python.org/zh-cn/3/library/re.html#re.Match>
    - [search() vs match()](https://docs.python.org/3/library/re.html#search-vs-match)
6. <https://docs.python.org/zh-cn/3/library/unittest.html>
7. <https://docs.python.org/zh-cn/3/library/stdtypes.html#dictionary-view-objects>

>[!info]
>bisect 的查询的确是 o(log(n)) 的，但插入是 o(n)，所以可以用来查询和更新，但删除，增加就会比较慢。

## Builtin Functions

### isinstance

> isinstance(object, class_or_tuple)

The function is used to check if an object is an instance of a specified class or any of its subclasses, it take two arguments: the object to check and the class or type to check against.

```python
# To verify whether a variable is either an integer or a float.
isinstance(a, (int, float))

if buffering == 0 or buffering is None:
if "b" not in mode:
```

### [range](https://docs.python.org/3/library/stdtypes.html#range)

To iterate over the indices of a sequence, you can combine [`range()`](https://docs.python.org/3/library/stdtypes.html#range "range") and [`len()`](https://docs.python.org/3/library/functions.html#len "len") as follows:

```python
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
 print(i, a[i])
# 0 Mary
# 1 had
# 2 a
# 3 little
# 4 lamb
```

In most such cases, however, it is convenient to use the [`enumerate()`](https://docs.python.org/3/library/functions.html#enumerate "enumerate") function, see [Looping Techniques](https://docs.python.org/3/tutorial/datastructures.html#tut-loopidioms).

## Extends & Implements

>- [Classes](https://docs.python.org/zh-cn/3/tutorial/classes.html)

Override Decorator for Static Typing

- [PEP-692:  Using TypedDict for more precise kwargs typing](https://docs.python.org/3/whatsnew/3.12.html#pep-692-using-typeddict-for-more-precise-kwargs-typing)
- [PEP-698: Override Decorator for Static Typing](https://docs.python.org/3/whatsnew/3.12.html#pep-698-override-decorator-for-static-typing)
In Python, interfaces are typically represented using Abstract Base Classes (ABCs) from the `abc` module. Abstract Base Classes allow you to define a blueprint for classes that inherit from them, specifying the methods that subclasses must implement. Here's how you can define an interface in Python using ABCs:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Abstract method to calculate the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self):
        """Abstract method to calculate the perimeter of the shape."""
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

# Creating instances of the classes
rectangle = Rectangle(5, 4)
circle = Circle(3)

# Calling methods defined in the interface
print("Rectangle area:", rectangle.area())  # Output: 20
print("Rectangle perimeter:", rectangle.perimeter())  # Output: 18

print("Circle area:", circle.area())  # Output: 28.274333882308138
print("Circle perimeter:", circle.perimeter())  # Output: 18.84955592153876

```

In this example:

- We define an abstract base class `Shape` with two abstract methods `area` and `perimeter`.
- The `@abstractmethod` decorator is used to mark these methods as abstract, indicating that subclasses must implement them.
- We then define concrete classes `Rectangle` and `Circle` that inherit from `Shape` and implement the required methods.
- When defining a subclass of `Shape`, we must implement all the abstract methods, otherwise, Python will raise a `TypeError` at runtime.

By using abstract base classes, you can define interfaces in Python, ensuring that subclasses adhere to a specific set of methods while allowing flexibility in their implementation.

## [Compound statements](https://docs.python.org/3/reference/compound_stmts.html#)

- [with statement](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#with)

### The with statement

The [`with`](https://docs.python.org/3/reference/compound_stmts.html#with) statement is used to wrap the execution of a block with methods defined by a context manager (see section [With Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)). This allows common [`try`](https://docs.python.org/3/reference/compound_stmts.html#try)…[`except`](https://docs.python.org/3/reference/compound_stmts.html#except)…[`finally`](https://docs.python.org/3/reference/compound_stmts.html#finally) usage patterns to be encapsulated for convenient reuse.

It ensures that certain operations are properly initialized and cleaned up, even if an exception occurs durng the execution of the block. Here's an example using the `with` statement with file handing:

```python
with open('example.txt', 'r') as file:
 content = file.read()
 print(content)
```

1. We use the `open()` function to open a file named 'example.txt' in read mode.
2. We use the `with` statement to create a content manager for file handing. This ensures that the file is properly closed after the block of code executes, regardless of whether an exception occurs or not.
3. Inside the `with` block, we read the contents of the file using the `read()` method and print them.
4. Once the block of code is executed, the file is automatically closed by the content manager, even if an exception occurs within the block.

## Decorator

>- [decorator](https://docs.python.org/zh-cn/3/glossary.html#term-decorator)
>- [function](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#function)
>- [classmethod](https://docs.python.org/zh-cn/3/library/functions.html#classmethod)
>- [function annotation](https://docs.python.org/zh-cn/3/glossary.html#term-function-annotation)

- <https://changchen.me/blog/20200621/annotation/>

### @property

In Python, the `@property` decorator is used to define properties for classes. Properties allow you to define getter, setter, and deleter methods for attributes, providing controlled access to these attributes while still maintaining a clean interface. Here's how you can use `@property`:

```python
class Circle:
    def __init__(self, radius):
        self.__radius = radius  # Prefixing with '_' to indicate it's a private attribute

    @property
    def radius(self):
        """Getter method for the 'radius' attribute."""
        return self.__radius

    @radius.setter
    def radius(self, value):
        """Setter method for the 'radius' attribute."""
        if value <= 0:
            raise ValueError("Radius must be a positive number.")
        self.__radius = value

    @radius.deleter
    def radius(self):
        """Deleter method for the 'radius' attribute."""
        del self.__radius

# Creating an instance of the Circle class
circle = Circle(5)

# Accessing the 'radius' attribute using the getter method
print(circle.radius)  # Output: 5

# Setting a new value for the 'radius' attribute using the setter method
circle.radius = 10

# Accessing the 'radius' attribute again
print(circle.radius)  # Output: 10

# Deleting the 'radius' attribute using the deleter method
del circle.radius
```

In this example:

- We define a `Circle` class with a private attribute `__radius`.
- We use `@radius.setter` to define a setter method named `radius`, which allows us to modify the `__radius` attribute. Inside the setter method, we can add validation logic if needed.
- We use `@radius.deleter` to define a deleter method named `raduis`, which allows us to detele the `_radius` attribute if necessary.
Using `@property`, you can provide controlled access to attributes of your class, ensuring that validation and other operations are performed as expected when accessing or modifying these attributes.

### @staticmethod & @classmethod

The `@staticmethod` decorator is used to define a static method within a class. Static methods do not receive an implicit first argument (usually named `self`), and they can be called on the class itself without needing an instance.

```python
class MyClass:
    @staticmethod
    def static_method():
        print("This is a static method")

# Calling the static method
MyClass.static_method()
```

This `@classmethod` decorator is used to define a class method within a class. Class methods receive a reference to the class itself as the first argument (usually named `cls`), allowing them to access or modify class-level attributes.

```python
class MyConfigClass:
    class_variable = 10

    @classmethod
    def class_method(cls):
        print("Class variable:", cls.class_variable)

# Calling the class method
MyClass.class_method()

## refer to the 'aws_xray_sdk' lib
class MyConfigClass:
 ENABLED_KEY = 'SDK_ENABLED'
    __SDK_ENABLED = None

 def __get_enabled_from_env(cls):
  return os.getenv(cls.ENABLED_KEY, 'true')

    @classmethod
    def sdk_enabled(cls):
  if cls.__SDK_ENABLED is None:
   cls.__SDK_ENABLED = cls.__get_enabled_from_env()
        return cls.__SDK_ENABLED
 
 def set_sdk_enabled(cls, value):
  cls.__SDK_ENABLED = value

# Calling the class method
config = MyConfigClass()
config.sdk_enabled()
```

**@staticmethod vs @classmethod**: You might wonder about the difference between `@staticmethod` and `@classmethod`. The main difference is that `@staticmethod` does not receive any reference to the class itself, while `@classmethod` does.

**@classmethod vs @staticmethod vs instance methods**: Instance methods receive a reference to the instance itself as the first argument (usually named `self`). They can access and modify instance attributes. `@classmethod` is used when you need access to the class itself within the method. `@staticmethod` is used when the method does not require access to either the instance or the class.

### @abstractmethod

The decorator is used to define abstract methods within abstract base classes (ABCs). Abstract methods must be implemented by subclasses, and attempting to create an instance of a class with unimplemented abstract methods will raise a `TypeError`.

```python
# the abc meaning of Abstract Base Classes (ABCs)
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def abstract_method(self):
        pass

class Subclass(Base):
    def abstract_method(self):
        print("Implemented abstract method")

# Attempting to create an instance of Base (will raise TypeError)
# base = Base()

# Creating an instance of Subclass
subclass = Subclass()
```

## Enum

In Python, enumerations(enums) can be defined using the `Enum` class from the `enum` module. Enum provide a way to create symbolic names for a set of unique values, making your code more readable and maintainable. Here's how you can define an enum in python:

```python
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


# Access them by:

## attribute access::
print(Color.RED)  # -> Color.RED
print(Color.RED.name)  # -> RED
print(Color.RED.value)  # -> 1

## value lookup:
print(Color(1))  # -> Color.RED

## name lookup:
print(Color["RED"])  # ->  Color.RED

## Enumerations can be iterated over, and know how many members they have:
print(len(Color))  # -> 3

print(list(Color))  # ->  [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

## Iterating over enum members
for color in Color:
    print(color)

## Enum members can be compared for equality (==).
print(Color.RED == Color.RED)  # -> True

# Methods can be added to enumerations, and members can have their own
# attributes -- see the documentation for details.
```

1. We define an enumeration `Color` by subclassing `Enum`.
2. Inside the class body, we define symbolic names for the values using class attributes (`RED`, `GREEN`, `BLUE`). Each member of the enum is an instance of the `Color` class.
3. We can access enum members using their names (`Color.RED`) or by accessing their `name` and `value` attributes.
4. Enums can be iterated over using a `for` loop.
5. Enum members can be compared for equality (`==`).

Enums provide a way to create a fixed set of symbolic names (constants) that can be used throughout your code, improving readability and preventing errors due to typos or incorrect values. They also provide built-in support for iteration, comparison, and more.

You can define enums with additional attributes by adding them as arguments to the enum members. Here's how you can define an enum with more attributes in Python:

```python
from enum import Enum

class Color(Enum):
    RED = (1, "FF0000")    # Tuple with value and hexadecimal color code
    GREEN = (2, "00FF00")
    BLUE = (3, "0000FF")

    def __init__(self, code, hex_code):
        self.code = code
        self.hex_code = hex_code

    def rgb_value(self):
        """Method to return the RGB value corresponding to the hex code."""
        return tuple(int(self.hex_code[i:i+2], 16) for i in (0, 2, 4))

# Accessing enum members and their attributes
print(Color.RED.code)           # Output: 1
print(Color.RED.hex_code)       # Output: 'FF0000'
print(Color.RED.rgb_value())    # Output: (255, 0, 0)
```

In this example:

- Each enum member (`RED`, `GREEN`, `BLUE`) is defined with a tuple containing additional attributes (`code` and `hex_code`).
- We define an `__init__` method to initialize these attributes when creating enum instances.
- We define a `rgb_value` method to convert the hexadecimal color code to an RGB value.
- When accessing enum members, you can access their attributes using dot notation (`Color.RED.code`, `Color.RED.hex_code`).
- You can also call methods defined within the enum members (`Color.RED.rgb_value()`).

By adding attributes and methods to enum members, you can make enums more versatile and useful for various purposes in your code.
