from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ERMS_Falcon_API.models import Base

engine=create_engine("sqlite:///ERMS_Falcon_API/app.db",echo=False)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()
