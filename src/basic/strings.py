seq = map(lambda x: str(x) + ".", range(100))
print(seq)
entire = "abcdefg rhijklmn opq rst uvw xyz      opq "

print(seq.__next__(), len(entire))#字符串的长度
print(entire.upper())#将字母转换成大写
print(entire.lower())#将字母转换成小写
print(entire.title().swapcase())#大小写转换
print(entire.capitalize())#将字符第一个字母转换成大写
print(entire.title())#将每个单词第一个字母转换成大写
print('2.', entire.upper().casefold(), sep='')#转换成小写，并处理特殊字符以实现更强大的匹配


print(entire.strip(' '), 'get', sep='')#去空格
print(entire.replace("opq","OPQ",1))#字符串新旧替换
print(entire.replace("opq","OPQ",2))#字符串新旧替换
print(entire.split(" ",4))#以子串作为分隔符，将原字符串按指定次数进行拆分（默认为一）
print(entire.rsplit(" ",4))#从右向左，以子串作为分隔符，将原字符串按指定次数进行拆分（默认为一）
print(" * ".join(entire,))#将字符串作为分隔符，把可迭代元素连接成一个字符串
print(entire.partition("rh"))#以子串为分隔符将字符串分割成三部分
print(entire.rpartition("rh"))#分割字符串成三份（从右边开始）
print(entire.center(78,"_"))#居中，并使用在指定字符填充空白部分
print(entire.ljust(50,"/"))#左对齐，并使用在指定字符填充空白部分
print(entire.rjust(67,"-"))#右对齐，并使用在指定字符填充空白部分
print(entire.zfill(67))#使字符串长度达到指定宽度，并用0填充空白
print(entire.expandtabs())
print(entire.encode())


print(entire.startswith("c",2,44))#判断是否以某个字符为开头
print(entire.endswith("z",3,23))#判断是否以某个字符为结尾
print(entire.isalnum())#判断是否是只包含数字和字母
print(entire.isalpha())#判断是否只包含字母
print(entire.isdigit())#判断是否只包含数字
print(entire.islower())#判断是否小写
print(entire.isupper())#判断是否大写
print(entire.isnumeric())#判断是否只包含数字字符（包括全角数字）
print(entire.isdecimal())#判断是否只包含十进制数字字符
print(entire.isascii())#判断是否只包含ASCII字符
print(entire.isidentifier())#判断是否是一个合法的PYTHON标识符
print(entire.isprintable())#判断是否可以打印
print(entire.isspace())#判断是否只包含空格
print(entire.istitle())#判断是否每个单词首字母都大写（标题格式）


print(entire.count("r",0,11))#返回范围内子串出现次数
print(entire.find("en",1,23))#返回范围内子串第一次出现时的索引，不存在返回-1
print(entire.find("r",1,23))
print(entire.index("r",2,10))#返回范围内子串第一次出现时的索引，不存在则报错
print(entire.rfind("r",1,33))#返回范围内子串最后一次出现时的索引，不存在返回-1
print(entire.rfind("ww",1,33))
print(entire.rindex("w",1,33))#返回范围内子串最后一次出现时的索引，不存在则报错

import string
print(string.__all__)
