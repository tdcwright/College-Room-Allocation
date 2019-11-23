import os
from urllib.parse import urlparse
from peewee import *  # pylint: disable=unused-wildcard-import
import math
import datetime

# from dotenv import load_dotenv

# load_dotenv()
# TODO: add environ variables
if "HEROKU" in os.environ:
    url = urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )
else:
    db_name = os.environ["DB_NAME"]
    db_user = os.environ["DB_USER"]
    db_pword = os.environ["DB_PASSWORD"]
    db = PostgresqlDatabase(db_name, user=db_user, password=db_pword)
    # db = SqliteDatabase('test1.db')


class Base(Model):
    class Meta:
        database = db


class Floor(Base):
    floorNumber = IntegerField(primary_key=True)
    # rooms = FoorToRoom Model
    # numDivisions = IntegerField()

    @classmethod
    def createFloor(cls, floorNumber):
        try:
            newFloor = cls.create(
                floorNumber=floorNumber,
                # numDivisions=numOfDivisions
            )

            return newFloor
        except IntegrityError as e:
            print("insert error! ", e)
            raise ValueError("Floor Already Exists")

    @classmethod
    def findFloor(cls, floorNumber):
        found = cls.get_or_none(Floor.floorNumber == floorNumber)
        if found != None:
            return found
        else:
            return None

    @property
    def numOfSeniors(self):
        studentList = (
            Student.select()
            .join(Room)
            .where(Student.allocation == Room.roomNumber)
            .where(Room.floor == self.floorNumber)
            .where(Student.year > 1)
        )

        return studentList.count()

    @property
    def numOfFreshers(self):
        studentList = (
            Student.select()
            .join(Room)
            .where(Student.allocation == Room.roomNumber)
            .where(Room.floor == self.floorNumber)
            .where(Student.year == 1)
        )

        return studentList.count()

    def numOfGender(self, isSenior=False):
        maleCount = 0
        femaleCount = 0

        studentList = (
            Student.select()
            .join(Room)
            .where(Student.allocation == Room.roomNumber)
            .where(Room.floor == self.floorNumber)
        )

        for student in studentList:
            if isSenior and student.year == 1:
                continue

            if student.gender == "m":
                maleCount += 1
            if student.gender == "f":
                femaleCount += 1

        return {"m": maleCount, "f": femaleCount}


class Room(Base):
    roomNumber = IntegerField(primary_key=True)
    bathroom = BooleanField()
    rf = BooleanField()
    front = BooleanField()
    balc = BooleanField()
    SubDivisionNumber = IntegerField()
    assigned = BooleanField()
    floor = ForeignKeyField(Floor, backref="rooms")

    @classmethod
    def createRoom(cls, roomNum, bathroom, front, balc, rf, SubDivisionNumber):
        try:
            floorNum = math.floor(roomNum / 100)
            newRoom = cls.create(
                roomNumber=roomNum,
                bathroom=bathroom,
                front=front,
                balc=balc,
                rf=rf,
                SubDivisionNumber=SubDivisionNumber,
                assigned=False,
                floor=floorNum,
            )

            return newRoom
        except IntegrityError:
            raise ValueError("Room Already Exists")

    @classmethod
    def findRoom(cls, roomNumber):
        found = cls.get_or_none(Room.roomNumber == roomNumber)
        if found != None:
            return found
        else:
            return False

    # newOccupant as zid
    def assignRoom(self, newOccupant):
        self.assigned = True
        student = Student.get(Student.zID == newOccupant)
        student.assigned = True
        student.allocation = self.roomNumber
        self.save()
        student.save()

    # oldOccupant as zid
    def clearAllocation(self):
        self.assigned = False
        student = self.occupant.get()
        student.assigned = False
        student.allocation = None
        self.save()
        student.save()


class Student(Base):
    zID = CharField(primary_key=True)
    name = CharField()
    year = IntegerField()
    gender = CharField()
    roomPoints = IntegerField()
    assigned = BooleanField(null=True)
    allocation = ForeignKeyField(Room, backref="occupant", null=True)
    password = CharField()
    startTime = DateTimeField(default=datetime.datetime.strptime("2050", "%Y"))
    otherPreferences = TextField(null=True)

    @classmethod
    def createStudent(cls, zid, name, year, gender, roomPoints, password, startTime):
        try:
            newStudent = cls.create(
                zID=zid,
                name=name,
                year=year,
                gender=gender,
                roomPoints=roomPoints,
                assigned=None,
                allocation=None,
                password=password,
                startTime=startTime,
            )

            return newStudent
        except IntegrityError:
            raise ValueError("Student Already Exists")

    @classmethod
    def findStudent(cls, zid):
        found = cls.get_or_none(Student.zID == zid)
        if found != None:
            return found
        else:
            return False

class Allocation(Base):
    timeOfAllocation = DateField(default=datetime.datetime.now())
    person = ForeignKeyField(Student, backref="allocation")
    room = ForeignKeyField(Room, backref="occupant")
    otherPreferences = TextField(null=True)

def db_reset():
    db.connect()
    # db.drop_tables([Student, Floor, Room])
    db.create_tables([Student, Floor, Room], safe=True)
    db.close()