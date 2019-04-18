# Enter your code here. Read input from STDIN. Print output to STDOUT

def createPhonebook(num_entries):
    address_book={}
    for i in range(num_entries):
        name_and_phone=(raw_input())
        name,phone_no=name_and_phone.split(" ")
        address_book[name]=phone_no

    return address_book

def getphoneNumber(name, address_book):
    nameList = address_book.keys()
    if name in nameList:
        print("%s %s")%(name, address_book[name])
    else:
        print("Not found")

if __name__=="__main__":
    num_entries=int(raw_input())
    address_book=createPhonebook(num_entries)
    while(1):
        name=raw_input()
        getphoneNumber(name, address_book)