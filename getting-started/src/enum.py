from enum import Enum, auto


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = auto() # auto generate a value


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


class ColorWithMoreAttributes(Enum):
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
print(ColorWithMoreAttributes.RED.code)           # -> 1
print(ColorWithMoreAttributes.RED.hex_code)       # -> 'FF0000'
print(ColorWithMoreAttributes.RED.rgb_value())    # -> (255, 0, 0)
