import pandas as pd
from sqlalchemy import create_engine,Column,Integer,Float,String,MetaData,Table,ForeignKey
from sqlalchemy.orm import declarative_base,sessionmaker,relationship
from fastapi import FastAPI,UploadFile,File,HTTPException


Database_url = "SQL Server:///./ExcelProject"
Base = declarative_base
   
engine = create_engine(Database_url, connect_args={"check_same_thread": False})

Sesssionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Users(Base):
    
    __tablename__ = "Users"
    
    user_id = Column(Integer ,primary_key=True, autoincrement=True)
    name = Column(String , nullable= False)
    
class Records(Base):
    
    __tablename__ = "Records"
    
    record_id = Column(Integer, primary_key =True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"),nullable=False)
    Year = Column(Integer,nullable=False)
    Month = Column(Integer, nullable=False)
    Amount = Column(Float,nullable=False)
 
Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.post("/upload-excel/{user_id}")
async def upload_excel(user_id: int,file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx", ".xls"):
        raise HTTPException(status_code=400, detail="please upload Required formart is Excel(.xls or .xslx)")
    
    
    df=  pd.read_excel(file)
    
    required_colms = {"year","month","amount"}
    if not required_colms.issubset(df.columns.str.lower()):
      raise HTTPException(status_code=400, detail="Excel must have colums {Year, month and Amount} in it")
    session = Sesssionlocal()
    
    try:
       for _, row in df.iterrows():
           records = Records(
               user_id=user_id,
               year = int(row["year"]),
               month = int(row["month"]),
               amount = float(row['amount'])
           )  
           session.Add(records)
           
           session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        session.close()
        
    
    return {"status": "success", "message":f"{len(df)} records added for user {user_id}" }
        