from fastapi import FastAPI, HTTPException, Depends, status, Form, Request, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uvicorn
import os



app = FastAPI()

# Подключение к базе данных
current_directory = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_directory, "test.db")
DATABASE_URL = f"sqlite:///{db_path}"  
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей SQLAlchemy
Base = declarative_base()

# Определение модели Delivery
class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    status = Column(String)

# Создание таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создание сессии SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Моковая функция для имитации обработки оплаты
def simulate_payment(order_id: int):
    payment_status = "paid" if order_id % 2 == 0 else "pending"
    return {"order_id": order_id, "status": payment_status}

# Функция для создания доставки и записи в БД
def create_delivery_and_record(db, order_id: int):
    payment_result = simulate_payment(order_id)
    delivery_status = "processed" if payment_result["status"] == "paid" else "not processed"

    # Создание объекта Delivery и добавление в БД
    db_delivery = Delivery(order_id=order_id, status=delivery_status)
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)

    return {"message": f"Processing delivery for order {order_id}", "delivery_id": db_delivery.id}

def get_access_token_from_header(request: Request):
    return request.headers["Authorization"]

# POST-запрос для создания доставки
@app.post("/delivery/{order_id}")
def create_delivery(order_id: int):
    db = SessionLocal()
    result = create_delivery_and_record(db, order_id)
    db.close()
    return result

# GET-запрос для чтения данных о доставке из БД
@app.get("/delivery/{order_id}")
def read_delivery(order_id: int):
    db = SessionLocal()
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    db.close()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return {"order_id": delivery.order_id, "status": delivery.status}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)