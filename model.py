from sqlalchemy.schema import Column
from sqlalchemy import String, Integer, Text, Enum, Boolean
from sqlalchemy_utils import EmailType, URLType
from database import Base
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import mapped_column

class UserInfo(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    eid = Column(Integer, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(EmailType)
    dept = Column(String)
    adhr = Column(String)
    file = Column(URLType)
    username = Column(String)
    password = Column(String)
    bio = Column(Text())
    categorytype = Column(String)
    timezonetype = Column(String)
    langtype = Column(String)
    isActive = Column(Boolean, default=True)
    isDeactive = Column(Boolean, default=False)
    isExcludefromEmail = Column(Boolean, default=False)

class CourseInfo(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    coursename = Column(String)
    file = Column(URLType)
    description = Column(String)
    coursecode = Column(String)
    price = Column(String)
    courselink = Column(String)
    coursevideo = Column(URLType)
    capacity = Column(String)
    startdate = Column(String)
    enddate = Column(String)
    timelimit = Column(String)
    certificate = Column(String)
    level = Column(String)
    category = Column(String)
    isActive = Column(Boolean, default=True)
    isHide = Column(Boolean, default=False)

class GroupInfo(Base):
    __tablename__ = "lmsgroup"
    
    id = Column(Integer, primary_key=True, index=True)
    groupname = Column(String)
    groupdesc = Column(String)
    groupkey = Column(String)

class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parentcategory = Column(String)
    price = Column(String)

# class Base(DeclarativeBase):
#     pass

# class LmsEvent(Base):
#     __tablename__ = "lmsevent"

#     id = mapped_column(Integer, primary_key=True)
#     ename: mapped_column(String, nullable=False)
#     eventtype: mapped_column(String)
#     recipienttype : mapped_column(String)
#     descp = mapped_column(String)
#     isActive = mapped_column(Boolean, default=True)

class LmsEvent(Base):
    __tablename__ = "lmsevent"

    id = Column(Integer, primary_key=True, index=True)
    ename = Column(String)
    eventtype = Column(String)
    recipienttype = Column(String)
    descp = Column(Text())
    isActive = Column(Boolean, default=True)
    

class Classroom(Base):
    __tablename__ = "classroom"
        
    id = Column(Integer, primary_key=True, index=True)
    instname = Column(String)
    classname = Column(String)
    date = Column(String)
    starttime = Column(String)
    venue = Column(String)
    messg = Column(String)
    duration = Column(String)

class Conference(Base):
    __tablename__ = "conference"
        
    id = Column(Integer, primary_key=True, index=True)
    instname = Column(String)
    confname = Column(String)
    date = Column(String)
    starttime = Column(String)
    meetlink = Column(String)
    messg = Column(String)
    duration = Column(String)

class VirtualTraining(Base):
    __tablename__ = "virtualtraining"
        
    id = Column(Integer, primary_key=True, index=True)
    instname = Column(String)
    virtualname = Column(String)
    date = Column(String)
    starttime = Column(String)
    meetlink = Column(String)
    messg = Column(String)
    duration = Column(String)

# ForeignKey(DeptModel, on_delete=models.CASCADE)