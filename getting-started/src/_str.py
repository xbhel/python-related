""" Use unicode to encode characters in Python."""

char_to_number = ord("A")
cn_char_to_number = ord("中")
number_to_char = chr(char_to_number)


"""
bytes 字符串字面量
在一个字符串字面量前面使用 b 前缀表示这是一个 bytes 串，其中每个字符只占一个 byte.
而字符串字面量中的值可能占多个 byte，这一点要和字符串字面量区分开来.
"""
bytes_str = b"bytes"

# encode and decode
encode_to_bytes = "str".encode("ascii")
decode_to_str = encode_to_bytes.decode("ascii")

"""
如果 bytes 中包含无法解码的字节，decode 会报错，
当 bytes 中只有一小部分无效的字节，可以使用 `errors=ignore` 去忽略错误的字节。
"""
encode_to_bytes.decode("utf-8", errors="ignore")

## format 

### by %
##### %d: int | %s: str | %f: float | %x: hex |
str_format_with_single_var = "Hello, %s" % ("world")
str_format_with_multi_var = "Hello, %s | %2d-%02d | %2f | %x" % ("world", 10, 10, 3.1415926, 0xffff)

### by format()
format_str_by_format_method = "Hello, {0}, {1:.1f}".format("world", 3.1415926)

### f string
#### 最后一种格式化字符串的方法是使用以f开头的字符串，称之为f-string，它和普通字符串不同之处在于，字符串如果包含{xxx}，
#### 就会以对应的变量替换
r = 2.5
s = 3.14 * r ** 2
format_str_f_prefix = f'The area of a circle with radius {r} is {s:.2f}'