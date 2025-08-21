from pymongo import MongoClient
from bson import ObjectId
from src.infrastructure.config import settings
from src.core.entities.user import User
from src.core.entities.product import Product
from src.core.entities.store import Store
from bson import ObjectId
from datetime import datetime, timedelta
from src.core.entities.sale import Sale

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]
users_collection = db["users"]
products_collection = db["products"]
sales_collection = db["sales"]
refresh_collection = db["refresh_tokens"]
store_collection = db["store"]

def create_user(user: User) -> str:
    user_dict = user.dict(exclude={"id"})
    result = users_collection.insert_one(user_dict)
    return str(result.inserted_id)

def find_user_by_email(email: str) -> User | None:
    doc = users_collection.find_one({"email": email})
    if doc:
        return User(id=str(doc["_id"]), **doc)
    return None

def create_product(product: Product) -> str:
    doc = product.dict(exclude={"id"})
    result = products_collection.insert_one(doc)
    return str(result.inserted_id)

def list_products() -> list[Product]:
    docs = products_collection.find()
    return [Product(id=str(doc["_id"]), **doc) for doc in docs]

def get_product_by_id(product_id: str) -> Product | None:
    doc = products_collection.find_one({"_id": ObjectId(product_id)})
    if doc:
        return Product(id=str(doc["_id"]), **doc)
    return None

def update_product(product_id: str, data: dict) -> bool:
    result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": data}
    )
    return result.modified_count > 0

def delete_product(product_id: str) -> bool:
    result = products_collection.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0

def list_catalog_products(name: str = None, min_price: float = None, max_price: float = None) -> list[Product]:
    query = {}
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if min_price is not None:
        query["price"] = query.get("price", {})
        query["price"]["$gte"] = min_price
    if max_price is not None:
        query["price"] = query.get("price", {})
        query["price"]["$lte"] = max_price
        
    docs = products_collection.find(query)
    return [Product(id=str(doc["_id"]), **doc) for doc in docs]

def create_sale(sale: Sale) -> str:
    doc = sale.dict(exclude={"id"})
    result = sales_collection.insert_one(doc)
    return str(result.inserted_id)

def list_sales_by_user(user_id: str) -> list[Sale]:
    docs = sales_collection.find({"user_id": user_id})
    return [Sale(id=str(doc["_id"]), **doc) for doc in docs]

def save_refresh_token(token: str, email: str, expires_days=7):
    expire_at = datetime.utcnow() + timedelta(days=expires_days)
    refresh_collection.insert_one({
        "token": token,
        "user_email": email,
        "created_at": datetime.utcnow(),
        "expires_at": expire_at,
        "active": True
    })
    
def invalidate_refresh_token(token: str):
    refresh_collection\
        .update_one(
            {"token": token},
            {"$set": {"active": False}}
        )

def is_valid_refresh_token(token: str) -> str | None:
    doc = refresh_collection\
        .find_one({"token": token, "active": True})
    if doc and doc["expires_at"] > datetime.utcnow():
            return doc["user_email"]
    return None

def add_image_to_product(product_id: str, image_data: dict) -> bool:
    result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$push": {"images": image_data}}
    )
    return result.modified_count > 0

def remove_image_from_product(product_id: str, public_id: str) -> bool:
    result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$pull": {"image": {"public_id": public_id}}}
    )
    
    return result.modified_count > 0

def get_store() -> Store:
    result = store_collection.find_one()
    if (result):
        return Store(id=str(result["_id"]), **result)
    return None

def isThereAStore():
    result = store_collection.count_documents({})
    return result > 0

def register_store(store: Store) -> str:
    store_dict = store.dict(exclude={"id"})
    result = store_collection.insert_one(store_dict)
    return str(result.inserted_id)