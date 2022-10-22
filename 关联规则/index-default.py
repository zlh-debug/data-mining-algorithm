from Rule_generate import GenRules
from Apriori import Apriori
from Close import Close
import time

data=[['A','B','E'],['B','D'],['B','C'],['A','B','D'],['A','C'],['B','C'],['A','C'],['A','B','C','E'],['A','B','C'],['D','E'],['B','D','E'],['A','B','C','E']];
minsup_count=2

t1=time.time()
Cls = Close(data,minsup_count)
Cls.close()
t2=time.time()

t3=time.time()
Apr=Apriori(data,minsup_count)
Apr.apriori()
t4=time.time()

Gen1=GenRules(0.6,Apr.Map,Apr.L,Apr.C)
Gen1.generate()
print("共生成%d个强关联规则"%(Gen1.count))
print("Apriori耗时%.5fms"%(t2-t1))

Gen2=GenRules(0.6,Cls.Map,Cls.L,Cls.C)
Gen2.generate()
print("共生成%d个强关联规则"%(Gen2.count))
print("Close耗时%.5fms"%(t4-t3))
