from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},)


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
@router.get("/userquery/")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already exists")
    
    user_dict= dict(user)
    del user_dict["id"]
    
    id = db_client.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    
    return User(**new_user)
        
        
        
USER_NOT_FOUND = "User not found"

@router.put("/", response_model=User)
async def user(user: User):

    try:
        user_dict = dict(user)
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": USER_NOT_FOUND}
    
    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
            
    if not found:
        return {"error": USER_NOT_FOUND}
            
        
def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        if user is None:
            return None
        return User(**user_schema(user))
    except IndexError:
        return {"error": USER_NOT_FOUND}
    
