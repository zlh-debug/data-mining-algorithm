import copy

class GenRules(object):
    def __init__(self,minconf,map,L,C):
        self.minconf=minconf
        self.map=map #字符串数字和物品的对应关系
        self.L=L[0:-1] #所有频繁项集
        self.flag=None #标记算过的规则，去重
        self.count=0 #记录生成强关联规则的数目
        self.C=C #k-候选集

    #字符串减法
    #param a 被减数
    #param b 减数
    def __sub(a,b):
        aa=copy.deepcopy(a).split(",")
        bb=copy.deepcopy(b).split(",")
        for i in range(len(bb)):
            aa.remove(bb[i])
        return ",".join(aa)

    #将格式化数字字符串转化成具体事物
    def __toTrans(self,str):
        s=""
        for i in range(len(str)):
            if str[i]!=",":
                s+=self.map[str[i]]
            else:
                s+=","
        return s

    #生成强关联规则的函数
    def generate (self):
        for i in range(len(self.L)-1,1,-1):
            for j in range(len(self.L[i])):
                self.flag=[]
                GenRules.__genrules(self,self.L[i][j],self.L[i][j],i,i)

    #递归查找强关联规则函数
    #param k 频繁项集
    #param m 根据此生成(m-1)-项集
    #param Nk k是几项集
    #param Nm m是几项集
    def __genrules(self,k,m,Nk,Nm):
        X=GenRules.__createSubset(self,m)
        for i in range(len(X)):
            t = ",".join(X[i])
            conf=self.C[Nk][k]/self.C[Nm-1][t]
            if conf>=self.minconf:
                self.count+=1
                print("%-3s => %-3s\tConfidence=%.0f%%"%(GenRules.__toTrans(self,t),GenRules.__toTrans(self,GenRules.__sub(k,t)),conf*100))
            else: continue
            if Nm>2:
                GenRules.__genrules(self,k,t,Nk,Nm-1)
        return

    #生成所有包含m-1项的m-项集的子集
    #param m m-项集
    def __createSubset (self,m):
        ans=[]
        temp=m.split(",")
        for i in range(len(temp)):
            t = copy.deepcopy(temp)
            t.pop(i)
            if t not in self.flag:
                ans.append(t)
                self.flag.append(t)
        return ans
