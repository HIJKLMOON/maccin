a = [1,2,3,4]
print(sum(a)) # sum 返回总值

a = [7,6,4,78,72,52,62]
a.sort(key=lambda x: (x + 3) % 5)
print((a)) # sorted 打印升序的列表

a = -6
print(abs(a)) # abs 绝对值

numbers = (1,2,3,4)
squared = list(map(lambda x: x**2, numbers)) # map 应用函数
print(squared)

a = 3.1415926
print(round(a,5)) # round 四舍五入

a = ["jack","curry","joden"]
b = ["rose","3ps","goat"]
print(dict(zip(a, b))) # zip 迭代配对

a = list(range(11))
print(sum(filter(lambda x:x % 2 == 0, a))) # filter 过滤

a = [1,2,3,4,5,6,0]
print(all(a), any(a)) # all 合取 any 析取

class young:x,y = 29, 11
a = young()
print(getattr(a,"x")) # getattr 获取属性

a.__setattr__("x", 20)
print(a.x, a.y)

a.__delattr__("x")
print(hasattr(a, "x"))

q = 728972
print(repr(q)) # repr 获取对象的原始表示

run = "4/2"
print(eval(run)) # eval 计算字符串的表达式

old = print("Hello world!") # print 输出
exec("old") # exec 执行多条语句
print(ord("a"))
print(chr(98))


Pi = 3.1415926
print(globals()["Pi"])#globals 返回全局变量

class jlja:y = 11
print(issubclass(young, jlja))

a = 123
print(dir(a))
