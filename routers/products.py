from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                   tags={"products"}, 
                   responses={404: {"description": "Not found"}})

products_list = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Mouse", "price": 20},
    {"id": 3, "name": "Keyboard", "price": 50},
]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]