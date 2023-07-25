import shutil

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from Xpayback_assignment.models import UserDB
from Xpayback_assignment.database import get_db
from Xpayback_assignment.mongo import mongo_collection
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    print("Base model visiting")
    # id: int
    user_id: str
    full_name: str
    email: str
    password: str
    phone: str
    # profile_picture: bytes


@app.post("/register/")
def register_user(user: User = Depends(), db: Session = Depends(get_db), profile_picture: UploadFile = File(...)):
    print(User)
    # Check if email already exists in PostgreSQL
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = db.query(UserDB).filter(UserDB.user_id == user.user_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!!! Please kindly login")

    # Save user data in PostgreSQL
    db_user = UserDB(
        full_name=user.full_name, user_id=user.user_id, email=user.email, password=user.password, phone=user.phone
    )


    # Save profile picture in MongoDB
    # profile_data = {"user_id": db_user.id, "profile_picture": user.profile_picture}
    # mongo_collection.insert_one(profile_data)
    if profile_picture:
        profile_data = {"user_id": str(db_user.user_id), "profile_picture": profile_picture.file.read()}
        mongo_collection.insert_one(profile_data)
        # profile_data = {"user_id": str(db_user.id), "profile_picture": profile_picture.filename}
        # with open(f"uploads/{profile_picture.filename}", "wb") as f:
        #     shutil.copyfileobj(profile_picture.file, f)
        # mongo_collection.insert_one(profile_data)
    db.add(db_user)
    db.commit()
    return {"message": "User registered successfully"}


@app.get("/")
def api_intro(request: Request):
    return f"Welcome to User registration using FastAPI." \
           f"Kindly access Docs to know more about the api : {str(request.url)}docs"


@app.get("/user/{user_id}")
def get_user_details(user_id: str, db: Session = Depends(get_db)):
    print("Entered into get user detail")
    # Get user data from PostgreSQL
    db_user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get profile picture from MongoDB
    profile_data = mongo_collection.find_one({"user_id": user_id})

    return {
        "user_id": db_user.user_id,
        "full_name": db_user.full_name,
        "email": db_user.email,
        "phone": db_user.phone,
    }


if __name__ == "__main__":
    print("Started from here")
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)

