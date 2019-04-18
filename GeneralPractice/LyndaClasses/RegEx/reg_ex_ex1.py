import re
pattern = r"pam"
match = re.search(pattern, "eggsspamsausagepancakes")
if match:
    print "there was a match "
    print match.group()
    print match.start()
    print match.end()
    print match.span()


str = "My name is David. Hi David!!"
pattern = r"David"
newstr = re.sub(pattern, "Keenan", str)
print newstr

str = "This method replaces all occurrences of the pattern i" \
      "s max provided. This method returns the modif"

pattern =r"replace"

newstr = re.sub(pattern," ERRORRR ", str)
print newstr


pattern2 =r"gr.y"
if re.match(pattern2, "grey"):
    print "The pattern matched "
if re.match(pattern2, "gray"):
    print "Patterm matched #2!!"

if re.match(pattern2, "blue"):
    print "Match # 3"

# match with ^ Start and $ - end
pattern3 =r"^gr.y$"

if re.match(pattern3, "grey"):
    print "Match pattern 3...!!!"
if re.match(pattern3, "gray"):
    print "Found gray"
if re.match(pattern3, "stingray"):
    print "Found a sting ray match"

print "Character Classes :"
print "+++++++++++++++++++"

pattern4 = r"[aeiou]"

if re.search(pattern4, "grey"):
    print("Matched ")
if re.search(pattern4, "qwertyuiop"):
    print "qwewrty"
if re.search(pattern4, "rhythm myths"):
    print ("No vowels match")
