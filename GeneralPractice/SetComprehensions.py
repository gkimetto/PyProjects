def main():
    
    ctemps = [3,34,5,56,23,12,34,67,78,97,2,3,44,23,34,56,56,3,34,56,67]
    ftemps1 = [(t*9/5)+32 for t in ctemps]
    ftemps2 = {(t*9/5)+32 for t in ctemps}
    print(ftemps1)
    print("Set ", ftemps2)
if __name__== "__main__":
    main()