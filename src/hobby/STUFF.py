from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
subs_1 = 'wonderful'
subs_2 = 'beautiful'
print(f'我叫{subs_1 + subs_2:-^20}，我是一个好人')
subs = 111_111_117.13_12
subs_s = f'{subs:=<+#20,.2f}'
print(type(subs_s), subs_s, sep='\n')


def subs_1(a, b, *, c):
    print(a, b, c)
    return


(subs_1(1, 3, c=3))


def subs_2(subs_array=[]):
    if subs_array == []:
        subs_array = []
    subs_array.append('a')
    print(subs_array)
    return


subs_2()
subs_2()
subs_2()


def subs_3(name, *love: int) -> int:
    subs_len = sum(love)
    print(type(love))
    return subs_len


print(subs_3('a', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

s = [1, 4, 23, 12, 42, 32, 17]
s.sort(key=lambda x: x % 10)
print(s)

subs_a = ['a', 'w', 'vs', 's']
subs_b = range(10)
subs_c = subs_a.__iter__()
print(help(subs_a.__iter__()))


def subs(s):
    return s < 5


subs_a = filter(None, [1, 23, 43, 12, 5, 2])
print(subs_a.__next__())
print(subs_a.__next__())
print(subs_a.__next__())
print(subs_a.__next__())


def subs(x, y):
    return x * 2


subs_a = map(subs, [1, 3], [23, 5])
for i in subs_a:
    print(i)

data = (
    ('姓名', '年龄', '城市'),
    ('张三', 28, '北京'),
    ('李四', 22, '上海')
)
with open('mytest.csv', mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

data = [
    {'姓名': '闫', '年龄': 27, '城市': '漠上'}
]
csv_writer = pd.DataFrame(data)
csv_writer.to_csv('mytest.csv', mode='a', header=False,
                  index=False, encoding='utf-8')

subs = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], ndmin=2)
subs = subs.reshape(9, 1)
print(subs, subs.shape, subs.ndim, subs.dtype, sep='*')

strData = 'life can be good, life can be bad, life is mostly cheerful, life is sometimes sad.'
strList = strData.split()
oneList = [1] * len(strList)
strDF = pd.DataFrame({'Words': strList, 'Count': oneList})
strDF = strDF.groupby(['Words']).count().reset_index()
print(strDF)

ffigure = plt.figure(figsize=(10, 5))
fp = ffigure.add_subplot(4, 3, 1)
plt.show()

dataA = [15, 22, 31, 46, 55]
dataB = [3, 5, 12, 51, 23]
dataC = [67, 23, 25, 65, 62]
df = pd.DataFrame({'A': dataA, 'B': dataB, 'C': dataC})
ax = df.plot(kind='line', figsize=(10, 5), title='Bar Chart Example')
ax.set_xlabel('Index')
ax.set_ylabel('Values')
plt.show()

npData = np.random.randn(10)
npDatacs = npData.cumsum()
print(npData, npDatacs)


def randrange(n, min, max):
    randArr = np.random.rand(n)
    return min + (max - min) * randArr


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 50
style = [(0, 10, 'r', 'o', 'low'), (10, 20, 'g', '*', 'high')]
for start, end, color, marker, label in style:
    xs = randrange(n, start, end)
    ys = randrange(n, start, end)
    zs = randrange(n, start, end)
    ax.scatter(xs, ys, zs, c=color, marker=marker, label=label)
ax.set_xlabel('Xlabel')
ax.set_ylabel('Ylabel')
ax.set_zlabel('Zlabel')
plt.show()

iris_data = load_iris()
x_train, x_test, y_train, y_test = train_test_split(
    iris_data['data'], iris_data['target'], test_size=0.2, random_state=2)
iris_df = pd.DataFrame(data=x_train, columns=iris_data.feature_names)
pd.plotting.scatter_matrix(iris_df, c=y_train, figsize=(
    15, 15), marker='o', hist_kwds={'bins': 20}, s=60, alpha=.8)

test = '字符串'
str1 = test.encode('utf-8')
print(str1, type(str1))
str2 = str1.decode('utf-8')
print(str2, type(str2))
