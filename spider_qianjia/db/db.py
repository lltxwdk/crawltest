import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, ForeignKey,Float
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class HouseInfo(Base):
    __tablename__ = 'house'
    id = Column(Integer, primary_key=True)
    coverImageUrl = Column(String(128))
    salePrice = Column(Float)
    unitPrice = Column(Float)
    title = Column(String(256))
    houseType = Column(String(128))
    area = Column(String(32))
    direction = Column(String(128))
    decoration = Column(String(128))
    houseTypeCode = Column(Integer)
    community = Column(String(256))
    floorLayer = Column(String(32))
    status = Column(String(16))
    region = Column(String(256))
    district = Column(String(256))
    topFloor = Column(Integer)
    builtYears = Column(String(16))
    propertyAge = Column(String(16))

#db操作
class DataBase:
    def __init__(self,host,port,user,password,databases,charset,maxoverflow):
        self.db_host = host
        self.db_port = port
        self.db_user = user
        self.db_pass = password
        self.db_db = databases
        self.db_charset = charset
        self.db_maxoverflow = maxoverflow

    def connectDB(self):
        conn_str = "mysql+pymysql://{user}:{pwd}@{host}:{port}/{db_name}?charset={charset}"
        connect_info = conn_str.format(user=self.db_user,pwd=self.db_pass,host=self.db_host,
                            port=self.db_port,db_name=self.db_db,charset=self.db_charset)
        
        maxoverflow = self.db_maxoverflow
        engine = create_engine(connect_info, max_overflow=maxoverflow)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def selectInfo(self,houseType):
        #ret = session.query(HouseInfo).all()
        qurry = self.session.query(HouseInfo)
        ret = qurry.filter(HouseInfo.houseTypeCode==houseType).all()
        return ret

    def deleteInfo(self,houseType):
        
        self.session.query(HouseInfo).filter(HouseInfo.houseTypeCode==houseType).delete()
        self.session.commit()

    def insert(self,id,coverImageUrl,salePrice,title,unitPrice,houseType,area,direction,decoration,houseTypeCode,community,floorLayer,status,region,district,topFloor,builtYears,propertyAge):
        houseId = int(id)
        sPrice = float(salePrice)
        uPrice = float(unitPrice)
        hTypeCode = int(houseTypeCode)
        tFloor = int(topFloor)
        house_info = HouseInfo(id=houseId,coverImageUrl = coverImageUrl,salePrice=sPrice,
                            unitPrice = uPrice,title= title,houseType=houseType,
                            area= area, direction= direction,
                            decoration=decoration,houseTypeCode=hTypeCode,community = community,
                            floorLayer=floorLayer,status=status,region=region,
                            district=district,topFloor=tFloor,builtYears=builtYears,
                            propertyAge=propertyAge)
        self.session.add(house_info)
        self.session.commit()


