def separate_strings(numStrings):
    lstStrings=[]
    for i in range(numStrings):
        input_string=str(raw_input())
        lstStrings.append(input_string)
        print(input_string[::2], input_string[1::2])
        
        
        
# Print 

if __name__=="__main__":
    numStrings = raw_input()
    numStrings=int(numStrings)
    separate_strings(numStrings)
