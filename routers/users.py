from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Entity
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [ User(id=1, name="John", surname="Jony", url="https://google.com", age=25), User(id=2,name="Nigerian", surname="Nig", url="https://wikipedia.com", age=27), User(id=3,name="Jose", surname="Pepe", url="https://wikipedia.com", age=27)]


@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)


    

@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if isinstance(search_user(user.id), User):
        raise HTTPException(status_code=404, detail="User already exists")
    else:
        users_list.routerend(user)
        return user
        
        
        
USER_NOT_FOUND = "User not found"

@router.put("/user/")
async def user(user: User):
    found = False
    
    for index, saverd_user in enumerate(users_list):
        if saverd_user.id == user.id:
            users_list[index] = user
            found = True
            
    if not found:
        return {"error": USER_NOT_FOUND}
    else:
        return user

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    
    for index, user in enumerate(users_list):
        if user.id == id:
            # users_list.pop(index)
            del users_list[index]
            found = True
            break
            
    if not found:
        return {"error": USER_NOT_FOUND}
    else:
        return {"message": "User deleted"}
            
        
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": USER_NOT_FOUND}