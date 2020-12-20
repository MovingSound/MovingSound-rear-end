from numpy import *
import time
from texttable import Texttable
import numpy as np

class CF:

    def __init__(self, musics, ratings, k=3, n=10):
        self.musics = musics
        self.ratings = ratings
        # 邻居个数
        self.k = k
        # 推荐个数
        self.n = n
        # 用户对音乐的评分
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

    #歌曲相似矩阵
    def musicSimilarity(self):
        musicsim =zeros((383,383))
        musicsim_ = zeros((383, 383))
        for v in self.userDict.values():
            for i in range(0,len(v)):
                for j in range(i+1,len(v)):
                    if v[i][1] != 0 and v[j][1] != 0:
                        x=int(v[i][0])-1
                        y=int(v[j][0])-1
                        musicsim[x][y] += 1
                        musicsim_[x][y] += 1 / (1 + 0.8 * math.fabs(int(v[i][2]) - int(v[j][2])))
        musicsim = np.triu(musicsim)
        musicsim += musicsim.T - np.diag(musicsim.diagonal())
        musicsim_ = np.triu(musicsim_)
        musicsim_ += musicsim_.T - np.diag(musicsim_.diagonal())
        return musicsim,musicsim_

    '''#
    def ItemSimilarity(self,train):
        # calculate co-rated users between items
        C = dict()
        N = dict()
        for u, items in train.items():
            for i in self.userDict:
                N[i] += 1
        for j in self.userDict:
            if i == j:
                continue
        C[i][j] += 1 / math.log(1 + len(items) * 1.0)
        # calculate finial similarity matrix W
        W = dict()
        for i, related_items in C.items():
            for j, cij in related_items.items():
                W[u][v] = cij / math.sqrt(N[i] * N[j])
        return W'''

    #计算各首歌曲被喜欢的次数
    def musicLike(self,musicsim):
        musicLikeNum = []
        for i in range(0,musicsim.shape[1]):
            num = 0
            for j in range(0,musicsim.shape[1]):
                num += musicsim[i][j]
            musicLikeNum.append(num)
        return musicLikeNum

    #基于物品的推荐
    def recommendByMusic(self,musicId):
        musicId = int(musicId)
        musicsim,musicsim_ = self.musicSimilarity()
        musicLikeNum = self.musicLike(musicsim)
        max = -1
        maxsim = 0.
        for i in range(0,len(musicLikeNum)):
            if math.sqrt(musicLikeNum[i]*musicLikeNum[musicId-1]) != 0:
                sim = musicsim_[musicId-1][i]/math.sqrt(musicLikeNum[i]*musicLikeNum[musicId-1])
            if sim > maxsim:
                maxsim = sim
                max = i+1
        return max

    # 基于用户的推荐
    # 根据对电影的评分计算用户之间的相似度
    def recommendByUser(self, userId):
        self.formatRate()
        # 推荐个数 等于 本身评分电影个数，用户计算准确率
        self.n = len(self.userDict[userId])
        self.getNearestNeighbor(userId)
        self.getrecommandList(userId)
        self.getPrecision(userId)

    # 获取推荐列表
    def getrecommandList(self, userId):
        self.recommandList = []
        # 建立推荐字典
        recommandDict = {}
        for neighbor in self.neighbors:
            musics = self.userDict[neighbor[1]]
            for music in musics:
                if(music[0] in recommandDict):
                    recommandDict[music[0]] += neighbor[0]
                else:
                    recommandDict[music[0]] = neighbor[0]

        # 建立推荐列表
        for key in recommandDict:
            self.recommandList.append([recommandDict[key], key])
        self.recommandList.sort(reverse=True)
        self.recommandList = self.recommandList[:self.n]

    # 将ratings转换为userDict和ItemUser
    def formatRate(self):
        self.userDict = {}
        self.ItemUser = {}
        for i in self.ratings:
            # 评分最高为5 除以5 进行数据归一化
            temp = (i[1], float(i[2]) / 5 , i[3])
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

    # 找到某用户的相邻用户
    def getNearestNeighbor(self, userId):
        neighbors = []
        self.neighbors = []
        # 获取userId评分的音乐都有那些用户也评过分
        for i in self.userDict[userId]:
            for j in self.ItemUser[i[0]]:
                if(j != userId and j not in neighbors):
                    neighbors.append(j)
        # 计算这些用户与userId的相似度并排序
        for i in neighbors:
            dist = self.getCost(userId, i)
            self.neighbors.append([dist, i])
        # 排序默认是升序，reverse=True表示降序
        self.neighbors.sort(reverse=True)
        self.neighbors = self.neighbors[:self.k]

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

    # 计算余弦距离
    def getCost(self, userId, l):
        # 获取用户userId和l评分音乐的并集
        # {'音乐ID'：[userId的评分，l的评分]} 没有评分为0
        user = self.formatuserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if(z == 0.0):
            return 0
        return z / sqrt(x * y)

    # 推荐的准确率
    def getPrecision(self, userId):
        user = [i[0] for i in self.userDict[userId]]
        recommand = [i[1] for i in self.recommandList]
        count = 0.0
        if(len(user) >= len(recommand)):
            for i in recommand:
                if(i in user):
                    count += 1.0
            self.cost = count / len(recommand)
        else:
            for i in user:
                if(i in recommand):
                    count += 1.0
            self.cost = count / len(user)

    # 显示推荐列表
    def showTable(self):
        neighbors_id = [i[1] for i in self.neighbors]
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t", "t", "t","t"])
        table.set_cols_align(["l", "l","l", "l"])
        rows = []
        rows.append([u"music ID", u"Name", u"musictype", u"from userID"])
        for item in self.recommandList:
            fromID = []
            for i in self.musics:
                if i[0] == item[1]:
                    music = i
                    break
            for i in self.ItemUser[item[1]]:
                if i in neighbors_id and i not in fromID:
                    fromID.append(i)
            music.append(fromID)
            rows.append(music)
        table.add_rows(rows)
        print(table.draw())


# 获取数据
def readmusicFile(filename):
    files = open(filename, "r", encoding="utf-8")
    data = []
    for line in files.readlines():
        item = line.strip().split("\t")
        data.append(item)
    return data

def readFile(filename):
    files = open(filename, "r", encoding="ISO-8859-1")
    data = []
    for line in files.readlines():
        item = line.strip().split("::")
        if int(item[1])>383:
            item[1]=str(int(int(item[1])/10))
        if int(item[1])>383:
            item[1]=str(int(item[1])-50)
        #print(item)
        data.append(item)
    print(data)
    return data

# -------------------------开始-------------------------------
start = time.clock()
musics = readmusicFile("E:/python/软工实践/团队编程/musicdata/musics.txt")
ratings = readFile("E:/python/软工实践/团队编程/musicdata/ratings.txt")
demo = CF(musics, ratings, k=10)
demo.recommendByUser("1")
print(demo.userDict['1'])
musics = []
for k in demo.userDict['1']:
    if k[1] > 0:
        music = demo.recommendByMusic(k[0])
        if music not in musics:
            print(k[0], music)
            musics.append(music)
print("基于歌曲的相似度推荐：")
print('为用户1推荐歌曲:',musics)
print("基于用户的推荐列表为：")
demo.showTable()
print("处理的数据为%d条" % (len(demo.ratings)))
print("准确率： %.2f %%" % (demo.cost * 100))
end = time.clock()
print("耗费时间： %f s" % (end - start))