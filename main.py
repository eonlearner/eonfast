from fastapi import FastAPI, Depends, File, Request, UploadFile,Form, Response,HTTPException
from fastapi.staticfiles import StaticFiles
import fastapi
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import pandas as pd
from fastapi.responses import FileResponse,HTMLResponse
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session, load_only
from fastapi import Header
from pathlib import Path
from sqlalchemy import JSON
from sqlalchemy import *
from typing import Union, Optional
from fastapi.middleware.cors import CORSMiddleware
from schema import UserInfo, CourseInfo, GroupInfo, Category, LmsEvent,Classroom,Conference, VirtualTraining, EmailSchema
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from PIL import Image
import io
import sqlalchemy as db
import model
from database import SessionLocal, engine
import shutil
import time
import os
import enum
from zipfile import ZipFile
import base64
#Email Functionality
from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List
# python-dotenv 
from dotenv import load_dotenv

conn = engine.connect()

model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# To get Video /Story.html from Fastapi Storage
some_file_path = "C:/Users/Admin/Desktop/TEST_projects/All_FastAPI_Projects/fastapi/1681713237/story.html"

# save_file_path = "C:/Users/Admin/Desktop/TEST_projects/All_FastAPI_Projects/fastapi/media/${item.file}"

app = FastAPI()

# app.add_middleware(HTTPSRedirectMiddleware)

# To fetch the Video directly by specifying path/Location
CHUNK_SIZE = 1024*1024
video_path = Path("1681713237/story_content/video_5h2Acq3SLhs_22_56_1280x720.mp4")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media/", StaticFiles(directory="media/"), name="media")

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


###################################### * GET REQUEST * ####################################################

@app.get('/')
def root():
    return{"Welcome To EonLearning Application Have a Great Day! 🌻👨‍💻🌹"}

@app.get("/users")
def getUsers(db: Session = Depends(get_database_session)):
    user = db.query(model.UserInfo).all()
    return user

@app.get("/courses")
def getCourses(db: Session = Depends(get_database_session)):
    course = db.query(model.CourseInfo).all()
    return course

@app.get("/groups")
def getGroups(db: Session = Depends(get_database_session)):
    group = db.query(model.GroupInfo).all()
    return group

@app.get("/categories")
def getCategory(db: Session = Depends(get_database_session)):
    category = db.query(model.Category).all()
    return category

# @app.get("/category")
# def getCategory(db: Session = Depends(get_database_session)):
#     category = db.query(model.Category).options(load_only("name")).all()
#     return category

@app.get("/lmsevents")
def getLmsevents(db: Session = Depends(get_database_session)):
    lmsevent = db.query(model.LmsEvent).all()
    return lmsevent

@app.get("/classrooms")
def getClassroom(db: Session = Depends(get_database_session)):
    classroom = db.query(model.Classroom).all()
    return classroom

@app.get("/conferences")
def getConference(db: Session = Depends(get_database_session)):
    conference = db.query(model.Conference).all()
    return conference

@app.get("/virtuals")
def getVirtualTraining(db: Session = Depends(get_database_session)):
    virtual = db.query(model.VirtualTraining).all()
    return virtual


# @app.get("/parentcategories")
# def getParentCategory(db: Session = Depends(get_database_session)):
#     parentcategory = db.query(model.ParentCategory).all()
#     return parentcategory

###################################### * POST REQUEST * ####################################################



@app.post('/users')
async def create_user(id: str = Form(...),eid: str = Form(...), firstname: str = Form(...), lastname: str = Form(...), email: str = Form(...),dept: str = Form(...), adhr: str = Form(...), username: str = Form(...), password: str = Form(...),bio: str = Form(...), categorytype: str = Form(...), timezonetype: str = Form(...), langtype: str = Form(...), isActive: bool = Form(...),file: UploadFile= File(...), db: Session = Depends(get_database_session)):
    with open("media/"+file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = str("media/"+file.filename)
    user = model.UserInfo(id= id, eid= eid, firstname= firstname, lastname= lastname, email= email,dept= dept,adhr= adhr,file= url, username= username, password= password,bio=bio,categorytype=categorytype,timezonetype=timezonetype,langtype=langtype,isActive=isActive)
    db.add(user)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id, "eid": eid, "firstname": firstname, "lastname": lastname, "email": email,"dept": dept, "adhr": adhr, "username": username, "password": password, "bio": bio,"categorytype": categorytype, "timezonetype": timezonetype, "langtype": langtype, "isActive": isActive, "file": file.filename}
    
@app.post('/courses')
async def create_course(id: int = Form(...), coursename: str = Form(...),description: str = Form(...), isActive: bool = Form(...),coursecode: str = Form(...),price: str = Form(...),courselink: str = Form(...),capacity: str = Form(...),startdate: str = Form(...),enddate: str = Form(...),timelimit: str = Form(...),certificate: str = Form(...),level: str = Form(...),category: str = Form(...),coursevideo: UploadFile= File(...), file: UploadFile= File(...), db: Session = Depends(get_database_session)):
    with open("media/"+file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = str("media/"+file.filename)
    with open("media/"+coursevideo.filename, "wb") as buffer:
        shutil.copyfileobj(coursevideo.file, buffer)
    urls = str("media/"+coursevideo.filename)
    course = model.CourseInfo(id= id, coursename= coursename, description= description,file= url,isActive= isActive, coursecode=coursecode, price=price,courselink=courselink, coursevideo=urls, capacity=capacity, startdate=startdate, enddate=enddate, timelimit=timelimit,certificate=certificate,level=level,category=category)
    db.add(course)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id, "coursename": coursename, "description": description, "file": file.filename, "isActive": isActive,"coursecode": coursecode, "price": price,"courselink": courselink,"coursevideo": coursevideo.filename,"capacity": capacity, "startdate": startdate, "enddate": enddate,"timelimit": timelimit,"certificate": certificate,"level": level,"category": category}
 
@app.post('/groups')
async def create_group(id: str = Form(...),groupname: str = Form(...),groupdesc: str = Form(...),groupkey: str = Form(...), db: Session = Depends(get_database_session)):
    group = model.GroupInfo(id= id,groupname=groupname,groupdesc=groupdesc, groupkey=groupkey )
    db.add(group)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id,"groupname": groupname, "groupdesc": groupdesc,"groupkey": groupkey}
  

@app.post('/categories')
async def create_category(id: str = Form(...),name: str = Form(...),parentcategory: str = Form(...),price: str = Form(...), db: Session = Depends(get_database_session)):
    category = model.Category(id=id, name=name, parentcategory=parentcategory, price=price)
    db.add(category)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id,"name": name, "parentcategory": parentcategory,"price": price}
    
@app.post('/lmsevents')
async def create_lmsevent(id: str = Form(...),ename: str = Form(...),eventtype: str = Form(...),recipienttype : str = Form(...),descp : str = Form(...), isActive: bool = Form(...), db: Session = Depends(get_database_session)):
    lmsevent = model.LmsEvent(id=id, ename= ename, eventtype=eventtype, recipienttype=recipienttype,descp=descp, isActive=isActive)
    db.add(lmsevent)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id,"ename": ename, "eventtype": eventtype, "recipienttype": recipienttype,"descp": descp, "isActive": isActive}

@app.post('/classrooms')
async def create_classroom(id: str = Form(...),instname: str = Form(...),classname: str = Form(...),date : str = Form(...),starttime : str = Form(...),venue : str = Form(...),messg : str = Form(...),duration : str = Form(...), db: Session = Depends(get_database_session)):
    classroom = model.Classroom(id=id, instname= instname, classname=classname, date=date, starttime=starttime, venue=venue, messg=messg, duration=duration)
    db.add(classroom)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id, "instname": instname, "classname": classname, "date": date,"starttime": starttime,"venue": venue,"messg": messg,"duration": duration}

@app.post('/conferences')
async def create_conference(id: str = Form(...),instname: str = Form(...),confname: str = Form(...),date : str = Form(...),starttime : str = Form(...),meetlink : str = Form(...),messg : str = Form(...),duration : str = Form(...), db: Session = Depends(get_database_session)):
    conference = model.Conference(id=id, instname= instname, confname=confname, date=date, starttime=starttime, meetlink=meetlink, messg=messg, duration=duration)
    db.add(conference)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id, "instname": instname, "confname": confname, "date": date,"starttime": starttime,"meetlink": meetlink,"messg": messg,"duration": duration}

@app.post('/virtuals')
async def create_virtual(id: str = Form(...),instname: str = Form(...),virtualname: str = Form(...),date : str = Form(...),starttime : str = Form(...),meetlink : str = Form(...),messg : str = Form(...),duration : str = Form(...), db: Session = Depends(get_database_session)):
    virtual = model.VirtualTraining(id=id, instname= instname, virtualname=virtualname, date=date, starttime=starttime, meetlink=meetlink, messg=messg, duration=duration)
    db.add(virtual)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"id": id, "instname": instname, "virtualname": virtualname, "date": date,"starttime": starttime,"meetlink": meetlink,"messg": messg,"duration": duration}






###################################### * GET SCORM COURSE REQUEST * ####################################################


@app.get("/scorm/story.html", response_class=FileResponse)
async def scorm():
    return some_file_path

@app.get("/media/")
async def media():
    imgpath = "C:/Users/Admin/Desktop/TEST_projects/All_FastAPI_Projects/fastapi/media/"
    with open(imgpath, 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image

    # out = []
    # for filename in os.listdir("media/"):
    #     out.append({
    #         "name": filename.split(".")[0],
    #         "path": "/media/" + filename
    #     })
    # return out
    # return save_file_path

###################################### * GET IMAGE REQUEST * ####################################################


@app.get("/images")
def images():
    base64image = []
    for filename in os.listdir("media/"):
        base64image.append({
            "name": filename.split(".")[0],
            "path": "media/" + filename
        })
    with open("media/", 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image

@app.post('/media/')
async def upload(file: UploadFile = File(...)):
    try:
        print("media/"+file.filename)
        contents = file.file.read()

        with open("media/"+file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file}"}

# @app.get("/photos", response_model=CourseInfo)
# async def get_all_photos():
#     conn = DATABASE_URL
#     conn.execute("Select file From course ORDER BY id DESC")
#     rows = conn.fetchall()

#     formatted_photos = []
#     for row in rows:
#         formatted_photos.append(
#             CourseInfo(
#             id=row[0], coursename=row[1], file=row[2], description=row[3], coursecode=row[4], price=row[5], courselink=row[6], coursevideo=row[7], capacity=row[8], startdate=row[9], enddate=row[10], timelimit=row[11] ,certificate=row[12] ,level=row[13] , category=row[14], isActive=row[15],isHide=row[16],eid=row[17]
#             )
#         )

#     conn.close()
#     return formatted_photos


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), uname: str = Form(...)):

    #Create unique folder for uploading Scorm zip
    mode = 0o666
    parent_dir = "C:/Users/Admin/Desktop/TEST_projects/All_FastAPI_Projects/fastapi"
    file_dir = str(int(time.time()))
    path = os.path.join(parent_dir, file_dir)
    os.mkdir(path, mode)

    #MOve uploaded file to created unique folder
    with open(file_dir + "/" + file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Extract zip file in that unique folder
    with ZipFile(file_dir + "/" + file.filename, 'r') as zObject:
        zObject.extractall(
            path=file_dir + "/")

#     # YOu got all relevance data for iframe and database entry
    return {"filename": file.filename, "name": uname, "url": parent_dir+"/"+file_dir+"/story.html"}

# @app.post('/users/excel/')
# async def create_excel(id: str = Form(...), eid: str = Form(...), firstname: str = Form(...),lastname: str = Form(...),email: str = Form(...),dept: str = Form(...),adhr: str = Form(...),username)
#     let workbook = xlsx.readFile('users.xlsx')
#     let worksheet = workbook.Sheets[workbook.SheetNames[0]]
#     let range = xlsx.utils.decode_range(worksheet["!ref"])

#     for (let row = range.s.r; row<= range.e.r; row++) {
#     let data = []

#     for (let col = range.s.c; col<= range.e.c; col++) {
#         let cell = worksheet[xlsx.utils.encode_cell({r:row, c:col})]
#         data.push(cell.v)
#     }
#     console.log(data)

#     let sql = "INSERT INTO 'user'('eid','firstname','lastname','email','dept','adhr','username','password','bio','file','categorytype','timezonetype','langtype','isActive','isDeactive','isExcludefromEmail') VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

#     db.query(sql,data,(err,results,fields) => {
#         if(err){
#         return console.error(err.message)
#         }
#         console.log('User ID:' + results.insertId)
#     }) 
#     }

#     db.end()
################################## * UPDATE REQUEST * ###############################################

# @app.put('/users/{id}', response_model=UserInfo)
# async def update_user(id: str = Field(...),eid: str = Form(...), firstname: str = Form(...), lastname: str = Form(...), email: str = Form(...),dept: str = Form(...), adhr: str = Form(...), username: str = Form(...), password: str = Form(...),bio: str = Form(...), categorytype: str = Form(...), timezonetype: str = Form(...), langtype: str = Form(...), isActive: bool = Form(...),file: UploadFile= File(...), db: Session = Depends(get_database_session)):
#     user = db.query(UserInfo).get(id)
#     query = user.update().where(user == id).value(
#         eid = eid,
#         firstname = firstname,
#         lastname = lastname,
#         email = email,
#         dept = dept,
#         adhr = adhr,
#         username = username,
#         password = password,
#         bio = bio,
#         file = file,
#         categorytype = categorytype,
#         timezonetype = timezonetype,
#         langtype = langtype,
#         isActive = isActive,
#     )
#     user_id = await db.execute(query)
#     query = user.select().where(user.id == user_id)
#     row = await db.fetch_one(query)
#     return {**row}

# class DocumentUpdateForm():
#     def __init__(
#             self,
#             eid: str = fastapi.Form(...),
#             firstname: str = fastapi.Form(...),
#             lastname: str = fastapi.Form(...),
#             email: str = fastapi.Form(...),
#             dept: str = fastapi.Form(...),
#             adhr: str = fastapi.Form(...),
#             username: str = fastapi.Form(...),
#             password: str = fastapi.Form(...),
#             bio: str = fastapi.Form(...),
#             file: Optional[fastapi.UploadFile] = fastapi.File(None),
#             categorytype: str = fastapi.Form(...),
#             timezonetype: str = fastapi.Form(...),
#             langtype: str = fastapi.Form(...),

#     ) -> None:
#         self.eid = eid
#         self.firstname = firstname
#         self.lastname = lastname
#         self.email = email
#         self.dept = dept
#         self.adhr = adhr
#         self.username = username
#         self.password = password
#         self.bio = bio
#         self.file = file
#         self.categorytype = categorytype
#         self.timezonetype = timezonetype
#         self.langtype = langtype


# @app.put('/users/{id}')
# def update_document(
#     id: str,
#     form_in: DocumentUpdateForm = fastapi.Depends(),
# ) -> None:
#     return {id, form_in}

# @app.post("/users/{id}")
# async def update_data(id: str, user: UserInfo):
#     conn.execute(user.insert().values(
#         id=user.id,
#         eid=user.eid,
#         firstname=user.firstname,
#         lastname=user.lastname,
#         email=user.email,
#         dept=user.dept,
#         adhr=user.adhr,
#         username=user.username,
#         password=user.password,
#         bio=user.bio,
#         file=user.file,
#         categorytype=user.categorytype,
#         timezonetype=user.timezonetype,
#         langtype=user.langtype
#     ))
#     return conn.execute(user.select()).fetchall()


# @app.patch("/users/{id}")
# async def update_user(request: Request, id: str,eid: str = Form(...), firstname: str = Form(...), lastname: str = Form(...), email: str = Form(...),dept: str = Form(...), adhr: str = Form(...), username: str = Form(...), password: str = Form(...),bio: str = Form(...), categorytype: str = Form(...), timezonetype: str = Form(...), langtype: str = Form(...), isActive: bool = Form(...),file: UploadFile= File(...), db: Session = Depends(get_database_session)):
#     requestBody = await request.json()
#     with open("media/"+file.filename, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     url = str("media/"+file.filename)
#     user = db.query(model.UserInfo).get(id,eid,firstname,lastname,email,dept,adhr, username, password, bio,isActive,file=url )
#     user.eid = requestBody['eid']
#     user.firstname = requestBody['firstname']
#     user.lastname = requestBody['lastname']
#     user.email = requestBody['email']
#     user.dept = requestBody['dept']
#     user.adhr = requestBody['adhr']
#     user.file = requestBody["file"]
#     user.username = requestBody['username']
#     user.password = requestBody['password']
#     user.bio = requestBody['bio']
#     user.isActive = requestBody['isActive']
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     response = RedirectResponse('/', status_code=303)
#     return {"id": id, "eid": eid, "firstname": firstname, "lastname": lastname, "email": email,"dept": dept, "adhr": adhr, "username": username, "password": password, "bio": bio,"categorytype": categorytype, "timezonetype": timezonetype, "langtype": langtype, "isActive": isActive, "file": file.filename}

# class UserInfoIn(BaseModel):
#     eid: str = Field(...)
#     firstname: str = Field(...)
#     lastname: str = Field(...)
#     email: str = Field(...)
#     dept: str = Field(...)
#     adhr: str = Field(...)
#     username: str = Field(...)
#     password: str = Field(...)
#     bio: str = Field(...)
#     file: bytes = File(...)
#     categorytype: str = Field(...)
#     timezonetype: str = Field(...)
#     langtype: str = Field(...)
#     isActive: bool = Field(...)


# @app.put("/users/{id}", response_model=UserInfo)
# async def update(id: int,  r: UserInfoIn = Depends(get_database_session)):
#     user = db.query(UserInfo).get(id)
#     query = user.update().where(user == id).value(
#         eid = r.eid,
#         firstname = r.firstname,
#         lastname = r.lastname,
#         email = r.email,
#         dept = r.dept,
#         adhr = r.adhr,
#         username = r.username,
#         password = r.password,
#         bio = r.bio,
#         file = bytes[r.file],
#         categorytype = r.categorytype,
#         timezonetype = r.timezonetype,
#         langtype = r.langtype,
#         isActive = r.isActive,
#     )
#     user_id = await db.execute(query)
#     query = user.select().where(user.id == user_id)
#     row = await db.fetch_one(query)
#     return {**row}

@app.post("/users/{id}")
def update_user(id: int,eid: str, firstname: str, lastname: str, email: str,dept: str, adhr: str, username: str, password: str,bio: str, categorytype: str, timezonetype: str, langtype: str, isActive: bool,file: UploadFile = File(...)):

    db = Session(bind=engine, expire_on_commit=False)
    with open("media/"+file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = str("media/"+file.filename)
    file=url
    # get the todo item with the given id
    user = db.query(model.UserInfo).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if user:
        user.eid = eid
        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.dept = dept
        user.adhr = adhr
        user.username = username
        user.password = password
        user.bio = bio
        user.file = file
        user.categorytype = categorytype
        user.timezonetype = timezonetype
        user.langtype = langtype
        user.isActive = isActive
        db.commit()

    # closing the session
    db.close()

    # check if user with given id exists. If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(status_code=404, detail=f"iser item with id {id} not found")

    return user
# @app.patch("/courses/{id}")
# async def update_course(request: Request, id: str,coursename: str = Form(...), description: str = Form(...), coursecode: str = Form(...), price: str = Form(...),courselink: str = Form(...), capacity: str = Form(...), startdate: str = Form(...),enddate: str = Form(...), timelimit: str = Form(...), certificate: str = Form(...), level: str = Form(...), category: bool = Form(...), isActive: bool = Form(...), coursevideo: UploadFile= File(...), file: UploadFile= File(...), db: Session = Depends(get_database_session)):
#     requestBody = await request.json()
#     with open("media/"+file.filename, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     url = str("media/"+file.filename)
#     with open("media/"+coursevideo.filename, "wb") as buffer:
#         shutil.copyfileobj(coursevideo.file, buffer)
#     urls = str("media/"+coursevideo.filename)

#     course = db.query(model.CourseInfo).get(id,coursename,description,coursecode,price,courselink, capacity, startdate, enddate,timelimit,certificate,level,category,isActive,coursevideo=urls,file=url )
#     course.coursename = requestBody['coursename']
#     course.description = requestBody['description']
#     course.coursecode = requestBody['coursecode']
#     course.file = requestBody['file']
#     course.price = requestBody['price']
#     course.courselink = requestBody['courselink']
#     course.coursevideo = requestBody['coursevideo']
#     course.capacity = requestBody["capacity"]
#     course.startdate = requestBody['startdate']
#     course.enddate = requestBody['enddate']
#     course.timelimit = requestBody['timelimit']
#     course.certificate = requestBody['certificate']
#     course.level = requestBody['level']
#     course.category = requestBody['category']
#     course.isActive = requestBody['isActive']
#     db.add(course)
#     db.commit()
#     db.refresh(course)
#     response = RedirectResponse('/', status_code=303)
#     return {"id": id, "coursename": coursename, "description": description, "coursecode": coursecode, "price": price,"courselink": courselink, "capacity": capacity, "startdate": startdate, "enddate": enddate, "timelimit": timelimit,"certificate": certificate, "level": level, "category": category, "isActive": isActive,"coursevideo": coursevideo.filename, "file": file.filename}
    

# @app.patch("/groups/{id}")
# async def update_group(request: Request, id: str,groupname: str = Form(...), groupdesc: str = Form(...), groupkey: str = Form(...), db: Session = Depends(get_database_session)):
#     requestBody = await request.json()
#     group = db.query(model.GroupInfo).get(id,groupname,groupdesc,groupkey)
#     group.groupname = requestBody['groupname']
#     group.groupdesc = requestBody['groupdesc']
#     group.groupkey = requestBody['groupkey']
#     db.add(group)
#     db.commit()
#     db.refresh(group)
#     response = RedirectResponse('/', status_code=303)
#     return {"id": id, "groupname": groupname, "groupdesc": groupdesc, "groupkey": groupkey}

# @app.patch("/categories/{id}")
# async def update_category(request: Request, id: str,name: str = Form(...), parentcategory: str = Form(...), price: str = Form(...), db: Session = Depends(get_database_session)):
#     requestBody = await request.json()
#     category = db.query(model.Category).get(id,name,parentcategory,price)
#     category.name = requestBody['name']
#     category.parentcategory = requestBody['parentcategory']
#     category.price = requestBody['price']
#     db.add(category)
#     db.commit()
#     db.refresh(category)
#     response = RedirectResponse('/', status_code=303)
#     return {"id": id, "name": name, "parentcategory": parentcategory, "price": price}
   
# @app.put("/users/{id}")
# async def update_user(id: int, user: UserInfo,db: Session = Depends(get_database_session)):

#     user_model = db.query(model.UserInfo).filter(model.UserInfo.id == id).first()

#     if user_model is None:
#         raise HTTPException(
#             status_code=404,
#             details=f"ID {id} : Does not exists"
#         )
    
#     user_model.eid = user.eid
#     user_model.firstname = user.firstname
#     user_model.lastname = user.lastname
#     user_model.email = user.email
#     user_model.dept = user.dept
#     user_model.adhr = user.adhr
#     user_model.file = user.file
#     user_model.username = user.username
#     user_model.password = user.password
#     user_model.bio = user.bio
#     user_model.isActive = user.isActive
#     user_model.categorytype = user.categorytype
#     user_model.timezonetype = user.timezonetype
#     user_model.langtype = user.langtype
    
#     db.add(user_model)
#     db.commit()

#     return user




# @app.patch("/users/{user_id}", response_model=UserInfo)
# async def update_item(item_id: str, user: UserInfo):
#     stored_user_data = users[user_id]
#     stored_user_model = UserInfo(**stored_user_data)
#     update_data = user.dict(exclude_unset=True)
#     updated_user = stored_user_model.copy(update=update_data)
#     users[item_id] = jsonable_encoder(updated_user)
#     return updated_user

# @app.put('/users')
# def update_user(user: UserInfo):
#     id = user.id
#     eid = user.eid
#     firstname = user.firstname
#     lastname = user.lastname
#     email = user.email
#     dept = user.dept
#     adhr = user.adhr
#     username = user.username
#     password = user.password
#     bio = user.bio
#     file = user.file
#     categorytype = user.categorytype
#     timezonetype = user.timezonetype
#     langtype = user.langtype
#     isActive = user.isActive
#     user_db[id] = user.dict()
#     return {'message': f'Successfully updated user: {id, eid, firstname, lastname, email, dept, adhr,username, password, bio,categorytype, timezonetype, langtype, file, isActive}'}

# @app.patch('/users')
# def update_user_partial(user: UserInfo):
#     username = user.username
#     user_db[username].update(user.dict(exclude_unset=True))
#     return {'message': f'Successfully updated user: {username}'}


# # @app.patch("/users/${userId}", response_model=UserInfo)
# # def update_user(userId: int, user: UserInfo, db: Session = Depends(get_database_session)):
# #         db_user = db.get(UserInfo, userId)
# #         if not db_user:
# #             raise HTTPException(status_code=404, detail="Hero not found")
# #         user_data = user.dict(exclude_unset=True)
# #         for key, value in user_data.items():
# #             setattr(db_user, key, value)
# #         db.add(db_user)
# #         db.commit()
# #         db.refresh(db_user)
# #         return db_user

################################## * DELETE REQUEST * ##################################################



@app.delete("/users/{id}")
async def delete_user(id: int, db: Session = Depends(get_database_session)):
    user = db.query(model.UserInfo).get(id)
    db.delete(user)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"User Deleted Successfully"}

@app.delete("/courses/{id}")
async def delete_course(id: int, db: Session = Depends(get_database_session)):
    course = db.query(model.CourseInfo).get(id)
    db.delete(course)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"Course Deleted Successfully"}

@app.delete("/groups/{id}")
async def delete_group(id: int, db: Session = Depends(get_database_session)):
    group = db.query(model.GroupInfo).get(id)
    db.delete(group)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"Group Deleted Successfully"}

@app.delete("/categories/{id}")
async def delete_category(id: int, db: Session = Depends(get_database_session)):
    category = db.query(model.Category).get(id)
    db.delete(category)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"Category Deleted Successfully"}

@app.delete("/lmsevents/{id}")
async def delete_lmsevent(id: int, db: Session = Depends(get_database_session)):
    lmsevent = db.query(model.LmsEvent).get(id)
    db.delete(lmsevent)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"Event Deleted Successfully"}

@app.delete("/classrooms/{id}")
async def delete_classroom(id: int, db: Session = Depends(get_database_session)):
    classroom = db.query(model.Classroom).get(id)
    db.delete(classroom)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"Classroom Deleted Successfully"}

@app.delete("/conferences/{id}")
async def delete_conference(id: int, db: Session = Depends(get_database_session)):
    conference = db.query(model.Conference).get(id)
    db.delete(conference)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"Conference Deleted Successfully"}

@app.delete("/virtuals/{id}")
async def delete_virtual(id: int, db: Session = Depends(get_database_session)):
    virtual = db.query(model.VirtualTraining).get(id)
    db.delete(virtual)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return {"Virtual Training Deleted Successfully"}


########################  EMAIL FUNCTIONALITY  ###################################

conf = ConnectionConfig(
    MAIL_USERNAME = "aniket24aug22@gmail.com",
    MAIL_PASSWORD = "gblenofxhmfrwgvy",
    MAIL_FROM = "aniket24aug22@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


@app.post("/send_mail")
async def send_mail(email: EmailSchema):
 
    template = """
        <html>
        <body>
         
 
<p>Hi !!!
        <br>Thanks for using EonLearning LMS, keep using it..!!!</p>
        <p>If you’re new to EonLearningLMS, you might need a little help starting out. To get things moving, let’s walk you through your first steps and point you to a few useful resources along the way.

<br>1. Sign in to your EonLearningLMS account as Administrator.
<br>2. Point to Help. From there you can:

<br>Search our Knowledge base articles.
<br>Restart the guided Tour to view EonLearningLMS in 3 different roles.
<br>Browse a vast collection of videos. What you see is a series of introductory videos. We recommend that you watch them in the following order:
<br>EonLearningLMS: Roles explained in EonLearningLMS
<br>EonLearningLMS: Creating a course in EonLearningLMS
<br>EonLearningLMS: How to add tests
<br>EonLearningLMS: How to add assignments
<br>EonLearningLMS: How to add files
<br>EonLearningLMS: How to create Instructor-led Training
<br>Email our customer support team from the Contact support option for any further clarification.
<br>Admin_Dashboard.png

<br>3. Make sure you’re logged in as Administrator.
<br>4. Go to Home >Account & Settings. On the Basic settings tab, type a name and description, and upload your company logo to your EonLearningLMS site.
<br>5. On the Domain tab, type a domain name for your EonLearningLMS site.
<br>6. On the Subscription tab, make sure that you are subscribed to the correct plan. Leave the other tabs for later.
<br>7. Go to Home > Categories > Add category. On this page, you can create a category for classifying a series of courses that share the same topic. For example, if that topic is Customer Service, then this can be the name of your new category.
<br>8. Return to Home and click Add user to start adding users to your EonLearningLMS platform. If your platform is for training your employees, then those are your EonLearningLMS users. If you also plan on training your customers then set up your user base to include customers that purchase your courses.

<br>Note: To assign your users to a course, you first have to create a course.
<br>9. Go to Home > Courses > Add course to start creating your first course. Type a Course Name and Description, and pick a Category for your new course. Click Save and select users to assign the course to Learners. If no users have been added yet, leave that for later. The next step is to add the content.
<br>10. Point to your name on the top bar. From the drop-down menu, change your role from Administrator to Instructor. Click the name of your new course. On your course page, click Add. Choose from the list of content types and start adding some content.
<br>11. Change your role to Learner. Click the name of your new course to view the added content and test it from a user’s viewpoint.

<br>Note: When you are assigned to the course as Instructor and complete it while you are switched to your learner role, you won't be able to see your data in reports. In reports you can find only data from users that are logged in and assigned to courses as learners.
<br>12. Change back to Instructor to make the necessary adjustments and, if needed, add more content to your course.
<br>13. As Administrator, add some users to your portal and assign the new course to them.

<br>Are you ready to dig deeper? Then, take a look at these videos:

<br>EonLearningLMS: How to customize your account
<br>EonLearningLMS: How to import and export data
<br>EonLearningLMS: How to set up notifications
<br>EonLearningLMS: How to use branches
<br>EonLearningLMS: How to use groups
<br>EonLearningLMS: How to view reports
<br>EonLearningLMS: How to customize user types
<br>EonLearningLMS: How to work with automations
<br>EonLearningLMS: How to clone courses & units
<br>EonLearningLMS: How to add conferences
<br>EonLearningLMS: How to set up gamification
<br>EonLearningLMS: How to sell your courses online</p>
 
        </body>
        </html>
        """
 
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=template,
        subtype="html"
        )
 
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)
 
     
 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})