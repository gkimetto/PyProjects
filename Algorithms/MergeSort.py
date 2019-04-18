"""Author: Gilbert Kimetto
   Purpose: Demonstrate the merge and sort 
            Divide and conquer algorithm break dataset into pieces and
            merge them. 
"""

def mergeSort(dataset):
    if len(dataset) > 1:
        mid = len(dataset)//2
        leftarr = dataset[:mid]
        rightarr = dataset[mid:]
        # TODO :: Recursively break down the arrays
        mergeSort(leftarr)
        mergeSort(rightarr)
        
        # TODO:: Now do the merging
        i=0 # Index into the left array
        j=0 # index into the right array
        k=0 # Index into the new merged array
        
        while i < len(leftarr) and j < len(rightarr):
            if leftarr[i] < rightarr[i]:
                dataset[k]=leftarr[i]
                i+=1
            else:
                dataset[k] =rightarr[j]
                j+=1
                k += 1
        # TODO : If the left array has values add them
        while i < len(leftarr):
            dataset[k] = leftarr[i]
            i += 1
            k += 1
        # If the right array has values add them
        while j < len(rightarr):
            dataset[k] = rightarr[j]
            j += 1
            k += 1
    return (dataset)
             
def main():
    dataset= [5,2,4,3,12,23,34,55,66,7,8,33,77,99,2,4,66,33,32]
    print(dataset)
    print(sorted(dataset))
    dataset1=mergeSort(dataset)
    print(dataset1)

if __name__=="__main__":
    main()