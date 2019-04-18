
from string import Template 

def main():
    str = "This is a Python book {1} written by {0}".format("Advanced Python", "Joe Marini")
    print(str)
    
    # using a template you will need an import
    # from string import Template 
    templ = Template("This is a Python book ${title} written by ${author}")
    str2 = templ.substitute(title="Advanced Pythonista Book", author="Joseph Marini")
    print(str2)
if __name__=="__main__":
    main()