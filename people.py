import csv
import math
import random

STUDENT_FILE_PATH = "dataLists/Students.csv"
NUM_OF_ROOMS = 212
studentList = []
NUM_OF_SENIORS = 0
NUM_OF_FRESHERS = 0

class Student():
    def __init__(self, zid, name, year, gender, roomPoints):
        self.zID = zid
        self.name = name
        self.year = year
        self.gender = gender
        self.roomPoints = roomPoints
        self.preferenceList = []
        self.assigned = False
        self.allocation = None
    
    # NOTE: This is an unsafe method, doesn't check if the person is already allocated
    def assignRoom(self, newRoom):
        self.assigned = True
        self.allocation = newRoom
    
    def clearAllocation(self):
        self.assigned = False
        self.allocation = None
    
    def __str__(self):
        return f"Student {self.name} with {self.roomPoints} points"


# To generate random data: https://www.generatedata.com/
def importStudents():
    global NUM_OF_SENIORS
    with open(STUDENT_FILE_PATH) as file:
        reader = csv.DictReader(file)
        for row in reader:
            zid = row["zID"]
            name = row["StudentName"]
            year = int(row["year"])
            roomPoints = int(row["roomPoints"])
            gender = row["gender"]

            newStudnet = Student(zid, name, year, gender, roomPoints)
            studentList.append(newStudnet)
            
            if year > 1:
                NUM_OF_SENIORS += 1
    
    
    global NUM_OF_FRESHERS
    NUM_OF_FRESHERS = NUM_OF_ROOMS - NUM_OF_SENIORS


# creates a list of example freshers, acting as example students
def createNewStudents():
    numOfReturners = len(studentList)
    numOfFreshers = NUM_OF_ROOMS - numOfReturners

    # NOTE: this will take into consideration the gender ratio of seniors
    equalizeGender = True
    def genderNumbers():
        maleCount = 0
        femaleCount = 0

        for person in studentList:
            if person.gender == "m":
                maleCount += 1
            elif person.gender == "f":
                femaleCount += 1
        
        return {"m":maleCount, "f":femaleCount}
    
    if equalizeGender == True: 
        genderCount = genderNumbers()
        freshMaleCount = (0.5*NUM_OF_ROOMS)-genderCount['m']
        freshFemaleCount = (0.5*NUM_OF_ROOMS)-genderCount['f']
    else:
        freshMaleCount = math.floor(numOfFreshers/2)
        freshFemaleCount = numOfFreshers-freshMaleCount
    
    for fresher in range(numOfFreshers):
        zid = f"z{fresher:07d}"
        while zid in [a.zID for a in studentList]:
            zid = f"z{random.randint(0,100000):07d}"
        name = f"Fresher {fresher}"
        year = 1
        roomPoints = 0
        if freshMaleCount != 0:
            gender = 'm'
            freshMaleCount -= 1
        else:
            gender = 'f'
            freshFemaleCount -= 1

        with open(STUDENT_FILE_PATH, 'a') as file:
            fieldNames = ["zID","StudentName","year","roomPoints","gender"]
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            
            writer.writerow({"zID":zid,"StudentName":name,"year":year,"roomPoints":roomPoints,"gender":gender})


        newStudnet = Student(zid, name, year, gender, roomPoints)
        studentList.append(newStudnet)

def getStudentList():
    studentListGender = {}
    for student in studentList:
        if (student.year != 1):
            studentListGender[student.zID] = student.gender
    
    return studentListGender

def findPerson(personList, zID):
    for person in personList:
        if person.zID == zID:
            return person
    
    return False

importStudents()
createNewStudents()