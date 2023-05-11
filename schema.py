from fastapi import File
from pydantic import BaseModel,FileUrl, EmailStr
from typing import Optional, List
    

# TO support creation and update APIs
class UserInfo(BaseModel):
    eid: int
    firstname: str
    lastname: str
    email: str
    dept: str
    adhr: str
    file: List[bytes]
    username: str
    password: str
    bio: str
    categorytype: str
    timezonetype: str
    langtype: str
    isActive: bool = True
    isDeactive: bool = False
    isExcludefromEmail: bool = False

class CourseInfo(BaseModel):
    id: int
    coursename: str
    file: List[bytes]
    description: str
    coursecode: str
    price: str
    courselink: str
    coursevideo: List[bytes]
    capacity: str
    startdate: str
    enddate: str
    timelimit: str
    certificate: str
    level: str
    category: str
    isActive: bool = True
    isHide: bool = False

class GroupInfo(BaseModel):
    id: int
    groupname: str
    groupdesc: str
    groupkey: str

class Category(BaseModel):
    id: int
    name: str
    parentcategory: str
    price: str

        
class LmsEvent(BaseModel):
    id: int
    ename: str
    eventtype: str
    recipienttype : str
    descp : str
    isActive: bool = True

class Classroom(BaseModel):
    id: int
    instname: str
    classname: str
    date: str
    starttime: str
    venue: str
    messg: str
    duration: str

class Conference(BaseModel):
    id: int
    instname: str
    confname: str
    date: str
    starttime: str
    meetlink: str
    messg: str
    duration: str

class VirtualTraining(BaseModel):
    id: int
    instname: str
    virtualname: str
    date: str
    starttime: str
    meetlink: str
    messg: str
    duration: str

    class Config:
        orm_mode = True
        
class EmailSchema(BaseModel):
   email: List[EmailStr]

