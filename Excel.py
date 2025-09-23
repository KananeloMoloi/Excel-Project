import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc

print(pyodbc.drivers())

DATABASE_URL = "mssql+pyodbc://BABYBOY/ExcelProject?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

Base = declarative_base()
engine = create_engine(DATABASE_URL, fast_executemany=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

#  Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class Records(Base):
    __tablename__ = "Records"
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    Year = Column(Integer, nullable=False)
    Month = Column(Integer, nullable=False)
    Amount = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload-excel/{user_id}")
async def upload_excel(user_id: int, file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Please upload Excel (.xls or .xlsx) file")

    df = pd.read_excel(file.file)
    # Clean column headers: strip spaces and lowercase
    df.columns = [c.strip().lower() for c in df.columns]

    required_cols = {"year", "month", "amount"}
    if not required_cols.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail="Excel must have columns: Year, Month, Amount")

    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            record = Records(
                user_id=user_id,
                Year=int(row["year"]),
                Month=int(row["month"]),
                Amount=float(row["amount"])
            )
            session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

    return {"status": "success", "message": f"{len(df)} records added for user {user_id}"}

@app.get("/get-records/{user_id}")
def get_records(user_id: int):
    session = SessionLocal()
    try:
        records = session.query(Records).filter(Records.user_id == user_id).all()
        return [{"year": r.Year, "month": r.Month, "amount": r.Amount} for r in records]
    finally:
        session.close()
