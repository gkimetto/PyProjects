"""Author: Gilbert Kimetto
   Purpose: 
           Implement the bubble sort 
   Performance : O(n)^2  - Quadratic -very inefficient    
                 Usually a for loop in a for loop is O(n)^2 
                 Does not scale for large data sets    
           """

def bubbleSort(dataset):
    print("Current state : ", dataset)
    for i in range(len(dataset) -1, 0, -1):
        for j in range(i):
            if dataset[i] < dataset[i-1]:
                temp = dataset[j]
                dataset[j] = dataset[j+1]
                dataset[j+1] = temp
    print("End state : ", dataset)
          
def main():
    list1 = [4545,6,20,8, 34,56,32,45,67,632,23]
    bubbleSort(list1)
    print("Result: ", list1)
if __name__=="__main__":
    main()