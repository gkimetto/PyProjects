class Difference:
    def __init__(self, a):
        self.__elements = a

    # Add your code here
    def computeDifference(self):
        diff_num=[]
        if len(self.__elements)==1 :
            print(self.__elements)
            pass
        else:
            for i in self.__elements:
                nxt_count=1
                while(nxt_count<len(self.__elements)):
                    nxt_num=abs(self.__elements[nxt_count])
                    print(nxt_num)
                    diff=abs(i-nxt_num)
                    diff_num.append(diff)
                    nxt_count+=1
            
        self.maximumDifference = max(diff_num)
        
# End of Difference class

_ = raw_input()
a = [int(e) for e in raw_input().split(' ')]

d = Difference(a)
d.computeDifference()

print (d.maximumDifference)