# main.py (OAuth2 Server)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt

from libs.Connection import Psql
from libs.Config import Config
from libs.Password import Password


app = FastAPI()

db_host, db_port, db_name, db_user, db_password = Config('postgresql0').get()
conn, cur = Psql(db_host, db_port, db_name, db_user, db_password).connect()


# Secret key to sign JWT token
SECRET_KEY = "3AC0FFA2-F6C1-44BE-9046-94C85EE816F3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock user data (you would replace this with your actual user data logic)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password": "secret",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
    }
}

# Token related functions
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Token validation function
def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload

# Token endpoint
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)

    query_user = "select * from users where username='" + form_data.username + "'"
    cur.execute(query_user)
    db_data = cur.fetchone()

    hash_userpass = Password(form_data.password).sha512()
    print(hash_userpass)
    print(db_data[1])
    if hash_userpass != db_data[1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_data[0]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Example endpoint that requires authentication
@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
