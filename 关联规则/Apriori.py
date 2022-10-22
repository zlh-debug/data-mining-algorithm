class Apriori(object):
    def __init__(self,data,minsup_count):
        self.Map = {} #对应关系
        self.C=[{}] #k-候选集
        self.L=[[]] #k-频繁项集
        self.S=[] #确定为不是频繁项集的项
        self.Data=data #事务数据库
        self.minsup_count=minsup_count #最小支持数
    
    #apriori发现频繁项集
    def apriori (self):
        T=Apriori.__convert(self,self.Data) #格式化的事务数据库
        #计算C[1]和L[1]
        self.C.append({}); self.L.append([]);
        for i in range(len(T)):
            for j in range(len(T[i])):
                if T[i][j] in self.C[1].keys():
                    self.C[1][T[i][j]] += 1
                else :
                    self.C[1][T[i][j]] = 1
        for i in self.C[1].keys():
            if self.C[1][i]>=self.minsup_count: self.L[1].append(i)
            else: self.S.append(i)
        k=2
        while len(self.L[k-1])!=0:
            self.C.append({}); self.L.append([]);
            self.C[k]=Apriori.__apriori_gen(self, self.L[k-1], k)
            for i in range(len(T)):
                for j in self.C[k].keys():
                    if Apriori.__isSubset(j,T[i]): 
                        self.C[k][j]+=1
            for i in self.C[k].keys():
                if self.C[k][i]>=self.minsup_count: self.L[k].append(i)
                else: self.S.append(i)
            k+=1
        return;
    
    #将事务数据库的数据格式化
    #param data 未处理的事务数据库
    def __convert (self,data):
        index=0
        buff=[]
        T=[]
        for i in range(len(data)):
            T.append([])
            for j in range(len(data[i])):
                t = buff.count(data[i][j])
                if t==0:
                    buff.append(data[i][j])
                    self.Map["%d"%index]=data[i][j]
                    T[i].append("%d"%index)
                    index+=1
                else:
                    T[i].append("%d"%buff.index(data[i][j]))
        return T;

    #由L[k-1]频繁项集生成C[k]候选集
    #param L[k-1] (k-1)-频繁项集
    def __apriori_gen (self, data, k):
        for i in range(len(data)):
            for j in range(i+1,len(data)):
                t = Apriori.__checkToMerge(data[i],data[j])
                if(t==1):
                    c=data[j]+","+data[i][len(data[i])-1]
                if(t==2):
                    c=data[i]+","+data[j][len(data[j])-1]
                #print(c)
                if(t!=0):
                    if(Apriori.__has_infrequent_subset(self,c)): c=None
                    else: self.C[k][c]=0
        return self.C[k];

    #根据定理：如果一个项集是非频繁项集，那么它的超集也是非频繁项集。判断c是否需要加到C[k]中去
    #param c 待判断的项集
    def __has_infrequent_subset (self,c):
        #"1,2,3"  "2,3,4"
        for i in range(len(self.S)):
            if Apriori.__isSubset(self.S[i],c):
                return True
        return False

    #判断两个(k-1)-频繁项集是否可以合并k-候选集
    #param La a项集
    #param Lb b项集
    def __checkToMerge(La,Lb):
        l1 = len(La)
        l2 = len(Lb)
        if(l1!=l2): return 0
        for i in range(l1-1):
            if(La[i]!=Lb[i]): return 0
        if(La[l1-1]>Lb[l1-1]): return 1
        else: return 2
        
    #判断a是否在b中出现过
    #param a string
    #param b list
    def __isSubset(a,b):
        a = a.split(",")
        for i in range(len(a)):
            if(a[i] not in b): return False
        return True

    #将list中数字格式转化成具体事物
    #param str string
    def __toThing (self,str):
        s=""
        for i in range(len(str)):
            if str[i] in self.Map.keys():
                s+=self.Map[str[i]]
            else:
                s+=str[i]
        return s

    #将dict中数字转化
    #param dc dict
    def __toThingDc (self,dc):
        dict={}
        for k,v in dc.items():
            dict[Apriori.__toThing(self,k)]=v
        return dict

    #转化频繁项集
    def transL (self):
        return list(map(lambda x:list(map(lambda y:Apriori.__toThing(self,y),x)),self.L))

    #转化候选集
    def transC (self):
        return list(map(lambda x:Apriori.__toThingDc(self,x),self.C))

    #转化非频繁项集
    def transS (self):
        return list(map(lambda x:Apriori.__toThing(self,x),self.S))
