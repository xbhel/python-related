# int
int_number = 10;
int_number_binary = 0b01;
int_number_octal = 0o71;
int_number_hex = 0xff00;
int_underline_split_format = 0xffff_ffff;

# float
float_number = 1.23;
float_scientific_notation_positive = 1.23e10;
float_scientific_notation_negative = 1.23e-10;

# 整数和浮点数在计算机内部存储的方式是不同的，整数运算永远是精确的（包括除法）
print(f"int / int => an exactly result => 10 / 3 = {10 / 3}")
print(f"float / float => an rounded result => 10.0 / 3.0 = {10.0 / 3.0}")

# string
string_quote = "This is a string";
string_single_quote = 'This is a string';
string_nested_quote = "'This' is a string";
string_multi_line = r"""
This is first \n line.
This is second \n line.
"""
string_escape_delimiter = 'I\'m \"OK\"!\\t';

"""
-r prefix: -r == row
When you use the r prefix before a string literal in Python (e.g., r'\\\t\\'), 
it creates a raw string. In a raw string, backslashes (\) are treated as literal 
characters rather than escape characters.
"""
string_no_escape = r'I\'m \"OK\"!'; # I\'m \"OK\"!

# boolean
bool_true = True;
bool_false = False;
bool_and_operator = True and True; # True
bool_or_operator = True or False; # True
bool_not_operator = not True; # -> !True = False
bool_with_expression = 1 > 2;

# Null
null_expression = None;

# bytes 字符串字面量
# 在一个字符串字面量前面使用 b 前缀表示这是一个 bytes 串，其中每个字符只占一个 byte.
# 而字符串字面量中的值可能占多个 byte，这一点要和字符串字面量区分开来.
bytes_str = b'bytes'