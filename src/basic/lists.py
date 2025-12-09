a: list[str | list[str]] = ["一","二","三","四"]
print(f"1.{a[1]}")#打印
a.append("五")#在列表后面添加
print(f"2.{a}")
a.append("六")
print(f"3.{a}")

b = ["七","八"]
a.extend(b) # 在列表后面添加列表
print(f"4.{a}")

a.insert(2, ["九", "十", "十一", "十二"]) # 在指定位置添加列表
print(f"5.{a}")
print(f"6.{a[2]}")
print(f"7.{a[2][3]}") # 打印列表里的列表的元素

del a[-2]#指定索引删除
print(f"8.{a}")

dell = a.pop(-2)#返回删除的元素
print(f"9.{dell}")
print(f"9.1.{a}")

a.remove("四")#指定元素，并从左向右开始
print(f"10.{a}")

b.clear()#清空
print(f"11.{a,b}")

a[3] = "三十"#修改指定索引的元素
print(f"12.{a}")

print(f"13.{a.index("二")}")#打印该元素的索引

print(f"14.{a.count("三")}")#打印该元素的数量

print(f"15.{a[1:9]}")#打印索引范围内元素
print(f"16.{a[:3]}")#0可缩写,左闭右开区间
print(f"17.{a[-2:]}")#不包括-1则会打印-1的元素
print(f"18.{a[-3:-1]}")
print(f"19.{a[::2]}")#步切（跳着切），最后一个数子表示步切单位

del a[2]
a.sort()#排序
print(f"20.{a}")
a.reverse()#反转
print(f"21.{a}")

for i in a:#for循环
    print(i, end = ' ')
print()

for i in enumerate(a):#打印循环序号
    print(i, end = ' ')
print()