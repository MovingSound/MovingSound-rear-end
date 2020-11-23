from numpy import *
import time
from texttable import Texttable

# 协同过滤推荐算法主要分为：
# 1、基于用户。根据相邻用户，预测当前用户没有偏好的未涉及物品，计算得到一个排序的物品列表进行推荐
# 2、基于物品。如喜欢物品A的用户都喜欢物品C，那么可以知道物品A与物品C的相似度很高，而用户C喜欢物品A，那么可以推断出用户C也可能喜欢物品C。
# 不同的数据、不同的程序猿写出的协同过滤推荐算法不同，但其核心是一致的：
#   1、收集用户的偏好
#       1)不同行为分组
#       2)不同分组进行加权计算用户的总喜好
#       3)数据去噪和归一化
#   2、找到相似用户(基于用户)或者物品(基于物品)
#   3、计算相似度并进行排序。根据相似度为用户进行推荐
# 本次实例过程：
# 1、初始化数据
#     获取movies和ratings
#     转换成数据userDict  表示某个用户的所有电影的评分集合，并对评分除以5进行归一化
#     转换成数据ItemUser  表示某部电影参与评分的所有用户集合
# 2、计算所有用户与userId的相似度
#     找出所有观看电影与userId有交集的用户
#     对这些用户循环计算与userId的相似度
#         获取A用户与userId的并集。格式为:{'电影ID',[A用户的评分,userId的评分]}，没有评分记为0
#         计算A用户与userId的余弦距离，越大越相似
# 3、根据相似度生成推荐电影列表
# 4、输出推荐列表和准确率


class CF:

    def __init__(self, movies, ratings, k=5, n=10):
        self.movies = movies
        self.ratings = ratings
        # 邻居个数
        self.k = k
        # 推荐个数
        self.n = n
        # 用户对电影的评分
        # 数据格式{'UserID：用户ID':[(MovieID：电影ID,Rating：用户对电影的评星)]}
        self.userDict = {}
        # 对某电影评分的用户
        # 数据格式：{'MovieID：电影ID',[UserID：用户ID]}
        # {'1',[1,2,3..],...}
        self.ItemUser = {}
        # 邻居的信息
        self.neighbors = []
        # 推荐列表
        self.recommandList = []
        self.cost = 0.0

    # 将ratings转换为userDict和ItemUser
    def formatRate(self):
        self.userDict = {}
        self.ItemUser = {}
        for i in self.ratings:
            # 评分最高为5 除以5 进行数据归一化
            temp = (i[1], float(i[2]) / 5)
            # 计算userDict {'1':[(1,5),(2,5)...],'2':[...]...}
            if(i[0] in self.userDict):
                self.userDict[i[0]].append(temp)
            else:
                self.userDict[i[0]] = [temp]
            # 计算ItemUser {'1',[1,2,3..],...}
            if(i[1] in self.ItemUser):
                self.ItemUser[i[1]].append(i[0])
            else:
                self.ItemUser[i[1]] = [i[0]]

    # 格式化userDict数据
    def formatuserDict(self, userId, l):
        user = {}
        for i in self.userDict[userId]:
            user[i[0]] = [i[1], 0]
        for j in self.userDict[l]:
            if(j[0] not in user):
                user[j[0]] = [0, j[1]]
            else:
                user[j[0]][1] = j[1]
        return user

# 获取数据
def readFile(filename):
    files = open(filename, "r", encoding="utf-8")
    # 如果读取不成功试一下
    # files = open(filename, "r", encoding="iso-8859-15")
    data = []
    for line in files.readlines():
        item = line.strip().split("::")
        data.append(item)
    return data

movies = readFile("/home/hadoop/Python/CF/movies.dat")
ratings = readFile("/home/hadoop/Python/CF/ratings.dat")