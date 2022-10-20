from Rule_generate import GenRules
from Apriori import Apriori

data=[["A","B","E"],["B","D"],["B","C"],["A","B","D"],["A","C"],["B","C"],["A","C"],["A","B","C","E"],["A","B","C"]]
minsup_count=2
minconf=0.6

Apr=Apriori(data,minsup_count)
Apr.apriori()
#print(Apr.transL())
print(Apr.transC()[1:-1])
Gen=GenRules(minconf,Apr.Map,Apr.L,Apr.C)
Gen.generate()
print("共生成%d个强关联规则"%(Gen.count))
