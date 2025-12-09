a = {
    '军军军':'zhiai',
    '女开':89,
    '谁':["shit",26,"唯一"],
    '爱与诚':["come","and","get","your","love"],
    "斯基":"你好！"
}#字典
print(a)

print(a.fromkeys([1],"love"))

a["军军军"] = ["有点上进心吧","别想女人了","一切都是值得的"]#修改
print(a)

a["殊死一搏"] = ["爱与诚"]#添加（若所添加的key已经存在，则是对原来的key进行修改
print(a)

print(a.pop("女开"))#删除且保留
del a["谁"]#删除
print(a)

print(a.values())#打印所有value
print(a.keys())#打印所有key

print(a.items())#把字典转换成列表
for i in a.items():#循环key—walue
    print(i)
for j,k in a.items():#分别循环key和value
    print(j,k)

for n in a:
    print(n)#循环打印key
    print(n,a[n])#分别循环key和value

a["三叶的歌"] = {"钢琴":"舞蹈","吉他":"圆舞曲"}#嵌套字典
print(a['三叶的歌']["吉他"])#打印字典里的字典