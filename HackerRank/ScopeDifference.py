class Difference:
    def __init__(self, a):
        self.__elements = a

    # Add your code here
    def computeDifference(self):
        count=0
        for i in self.__elements:
            tmp_num[0] = abs(i)
            count+=1
            
        maximumDifference = tmp_num[0]-tmp_num[2]
        
# End of Difference class

_ = raw_input()
a = [int(e) for e in raw_input().split(' ')]

d = Difference(a)
d.computeDifference()

print (d.maximumDifference)