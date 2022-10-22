import copy

class Close(object):
    def __init__(self,data,minsup_count):
        self.Map={}
        self.FCC=[{}]
        self.FC=[{}]
        self.S=[]
        self.data=data
        self.L={} #k-频繁项集
        self.C={} #k-候选频繁项集
        self.minsup_count=minsup_count

    #将交易数据库的数据格式化
    #param data 未处理的交易数据库
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

    #根据k-频繁闭合项集生成(k+1)-候选频繁闭合项集
    #param FC k-频繁闭合项集
    def __Gen_Generator(self,FC):
        ans={"generate":[],"closure":[],"support":[]}
        temp=[]
        Tf = FC["generate"]
        for i in range(len(Tf)):
            for j in range(i+1,len(Tf)):
                t=self.__checkToMerge(Tf[i],Tf[j])
                if(t==1):
                    c=copy.deepcopy(Tf[j])
                    c.append(Tf[i][len(Tf[i])-1])
                if(t==2):
                    c=copy.deepcopy(Tf[i])
                    c.append(Tf[j][len(Tf[j])-1])
                if(t!=0):
                    if(self.__has_infrequent_subset(c)): c=None
                    else: temp.append(c)
        #print(temp)
        for i in temp:
            Sp=self.__Subset(Tf,i)
            flag=True
            for j in Sp:
                if i==FC["closure"][j]:
                    continue
                if self.__isSubset(i,FC["closure"][j]):
                    flag=False
                    break
            if flag:
                ans["generate"].append(i)
                ans["closure"].append(None)
                ans["support"].append(0)
        #print(ans)
        return ans;

    #根据定理：如果一个项集是非频繁项集，那么它的超集也是非频繁项集。判断c是否需要加到C[k]中去
    #param c 待判断的项集
    def __has_infrequent_subset(self,c):
        #"1,2,3"  "2,3,4"
        for i in self.S:
            if self.__isSubset(i,c):
                return True
        return False

    #定义集合a和b的交集
    #param a 集合a
    #param b 集合b
    def __intersection(self,a,b):
        ans=[]
        for i in a:
            if i in b: ans.append(i)
        return ans

    #计算闭合项集
    #param C 候选频繁闭合项集
    #param T 格式化的交易数据库
    def __Gen_Closure(self,C,T):
        ans={"generate":[],"closure":[],"support":[]}
        for i in T:
            Go=self.__Subset(C["generate"],i)
            for p in Go:
                if C["closure"][p]==None:
                    C["closure"][p]=i;
                else:
                    C["closure"][p]=self.__intersection(C["closure"][p],i)
                C["support"][p]+=1;
        for i in range(len(C["closure"])):
            if C["closure"][i]!=None:
                ans["generate"].append(C["generate"][i])
                ans["closure"].append(C["closure"][i])
                ans["support"].append(C["support"][i])
        return ans

    #判断a是否是b的子集
    #param a 集合a
    #param b 集合b
    def __isSubset(self,a,b):
        for i in a:
            if i not in b:
                return False
        return True

    #找出交易数据库中一条交易的子集
    #param generate 候选频繁闭合项目集的产生式
    #param t 交易数据库中的一条交易记录
    def __Subset(self,generate,t):
        ans=[]
        for i in range(len(generate)):
            if self.__isSubset(generate[i],t):
                ans.append(i)
        return ans

    #判断两个(k-1)-频繁项集是否可以合并k-候选集
    #param La a项集
    #param Lb b项集
    def __checkToMerge(self,La,Lb):
        l1 = len(La)
        l2 = len(Lb)
        if(l1!=l2): return 0
        for i in range(l1-1):
            if(La[i]!=Lb[i]): return 0
        if(La[l1-1]>Lb[l1-1]): return 1
        else: return 2

    #生成所有包含m-1项的m-项集的子集
    #param m m-项集
    def __createSubset (self,m):
        ans=[]
        temp=m.split(",")
        for i in range(len(temp)):
            t = copy.deepcopy(temp)
            t.pop(i)
            ans.append(t)
        return ans

    #推到所有k-项集和候选集
    def __deriving(self):
        for i in range(1,len(self.FC)):
            for j in range(len(self.FC[i]["generate"])):
                self.FC[i]["closure"][j].sort()
                l=len(self.FC[i]["closure"][j])
                if l not in self.L.keys(): self.L[l]=[]
                t=",".join(self.FC[i]["closure"][j])
                if t not in self.L[l]: self.L[l].append(t)
                if l not in self.C.keys(): self.C[l]={}
                self.C[l][t]=self.FC[i]["support"][j]
        for i in range(len(self.L),1,-1):
            if i-1 not in self.L.keys(): self.L[i-1]=[]
            if i-1 not in self.C.keys(): self.C[i-1]={}
            for j in self.L[i]:
                Sub=self.__createSubset(j)
                for k in Sub:
                    t=",".join(k)
                    if t not in self.L[i-1]: self.L[i-1].append(t)
                    if t not in self.C[i-1].keys():
                        self.C[i-1][t]=self.C[i][j]
        return

    #close算法主函数
    def close(self):
        T=self.__convert(self.data)
        self.FCC.append({})
        self.FCC[1]['generate']=[]
        self.FCC[1]["closure"]=[]
        self.FCC[1]["support"]=[]
        for i in self.Map.keys():
            self.FCC[1]["generate"].append([i])
            self.FCC[1]["closure"].append(None)
            self.FCC[1]["support"].append(0)
        k=1
        while len(self.FCC[k]["generate"])!=0:
            self.FC.append({"generate":[],"closure":[],"support":[]})
            self.FCC[k]=self.__Gen_Closure(self.FCC[k],T)
            for i in range(len(self.FCC[k]["support"])):
                if self.FCC[k]["support"][i]>=self.minsup_count:
                    self.FC[k]["generate"].append(self.FCC[k]["generate"][i])
                    self.FC[k]["closure"].append(self.FCC[k]["closure"][i])
                    self.FC[k]["support"].append(self.FCC[k]["support"][i])
                else:
                    self.S.append(self.FCC[k]["generate"][i])
            self.FCC.append({})
            self.FCC[k+1]=self.__Gen_Generator(self.FC[k])
            k+=1
        self.__deriving()
        self.L[0]=[]
        return;
