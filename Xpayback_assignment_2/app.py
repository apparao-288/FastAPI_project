
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from Xpayback_assignment.models import UserDB, ProfileDB
from Xpayback_assignment.database import get_db
from pydantic import BaseModel

new_app = FastAPI()


class User(BaseModel):
    """

    """
    # id: int
    user_id: str
    full_name: str
    email: str
    password: str
    phone: str
    # profile_picture: bytes


@new_app.post("/register/")
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
    # Save profile picture in MongoDB

    db_user = UserDB(
        full_name=user.full_name, user_id=user.user_id, email=user.email, password=user.password, phone=user.phone
    )
    db.add(db_user)
    db.commit()
    if profile_picture:
        print("Profile picture found")
        # profile_data = {"user_id": str(db_user.user_id), "profile_picture": profile_picture.file.read()}

        db_profile = ProfileDB(user_id=db_user.user_id, image_data=profile_picture.file.read())
        db.add(db_profile)
        db.commit()

    return {"message": "User registered successfully"}


@new_app.get("/")
def api_intro(request: Request):
    return f"Welcome to User registration using FastAPI." \
           f"Kindly access Docs to know more about the api : {str(request.url)}docs"


@new_app.get("/user/{user_id}")
def get_user_details(user_id: str, db: Session = Depends(get_db)):
    print("Entered into get user detail")
    # Get user data from PostgreSQL
    db_user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": db_user.user_id,
        "full_name": db_user.full_name,
        "email": db_user.email,
        "phone": db_user.phone,
    }


if __name__ == "__main__":
    print("Started from here")
    uvicorn.run("app:new_app", host="127.0.0.1", port=8086, reload=True)

