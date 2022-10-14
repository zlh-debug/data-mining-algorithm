from Rule_generate import GenRules
from Apriori import Apriori

data=[["A","B","C","D"],["B","C","E"],["A","B","C","E"],["B","D","E"],["A","B","C","D"]]
minsup_count=2
minconf=0.6

Apr=Apriori(data,minsup_count)
Apr.apriori()
Gen=GenRules(minconf,Apr.Map,Apr.L,Apr.C)
Gen.generate()
print("共生成%d个强关联规则"%(Gen.count))
