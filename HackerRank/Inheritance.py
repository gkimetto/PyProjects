class Person:
    def __init__(self, firstName, lastName, idNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.idNumber = idNumber
    def printPerson(self):
        print("Name:", self.lastName + ",", self.firstName)
        print("ID:", self.idNumber)

class Student(Person):

    #   Class Constructor
    #   
    #   Parameters:
    #   firstName - A string denoting the Person's first name.
    #   lastName - A string denoting the Person's last name.
    #   id - An integer denoting the Person's ID number.
    #   scores - An array of integers denoting the Person's test scores.
    #
    # Write your constructor here
    def __init__(self, firstName, lastName,idNumber, scores ):
        self.firstName=firstName
        self.lastName=lastName
        self.idNumber=idNumber
        self.scores=scores

    #   Function Name: calculate
    #   Return: A character denoting the grade.
    #
    # Write your function here
 
    def calculate(self):
        # A char calculate() method that calculates a Student object's average 
        # and returns the grade character representative of their calculated average

        sum_scores=sum(self.scores)
        sz_score=len(self.scores)
        average_score=sum_scores/sz_score
        print(sz_score)
        print(sum_scores)
        print(average_score)

        if average_score >= 90 and average_score <=100:
            grade='O'
        elif average_score >=80 and average_score <90:
            grade ='E'
        elif average_score >=70 and average_score <80:
            grade ='A'
        elif average_score >=55 and average_score <70:
            grade = 'P'
        elif average_score >=40 and average_score < 55:
            grade = 'D'
        elif average_score < 40:
            grade ='T'
        else:
            print('Error:...')
        return grade

line = raw_input().split()
firstName = line[0]
lastName = line[1]
idNum = line[2]
numScores = int(raw_input()) # not needed for Python
scores = map(int, raw_input().split())
s = Student(firstName, lastName, idNum, scores)
s.printPerson()
print("Grade:", s.calculate())