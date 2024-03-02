from datetime import datetime, date, time
import os
import pandas as pd
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DeliveryPreference(Base):
    __tablename__ = 'delivery_preference'
    account_id_hashed = Column(String, primary_key=True)
    deliverypreference = Column(String)
    datelastupdated = Column(DateTime)
    datecreated = Column(DateTime)

class DeliveryFacts(Base):
    __tablename__ = 'delivery_facts'
    id = Column(Integer, primary_key=True)
    account_id_hashed = Column(String, ForeignKey('delivery_preference.account_id_hashed'))
    month_id = Column(Integer)
    number_of_parcels = Column(Integer)
    parcels_home_1st = Column(Integer)

class ColloPackages(Base):
    __tablename__ = 'collo_packages'
    id = Column(Integer, primary_key=True)
    account_id_hashed = Column(String, ForeignKey('delivery_preference.account_id_hashed'))
    dn_barcode = Column(String)
    da_datum_voormelding = Column(Date)
    da_datum_acceptatie = Column(Date)
    da_tijd_acceptatie = Column(Time)
    sa_dag_sortering1 = Column(Date)
    sa_datum_sortering1 = Column(Date)
    sa_tijd_sortering1 = Column(Time)
    sa_datum_distributiecollectie = Column(Date)
    sa_tijd_distributiecollectie  = Column(Time)
    da_datum_herroutering_voor_up1 = Column(Date)
    da_tijd_herroutering_voor_up1 = Column(Time)
    da_datum_eindstatus = Column(Date)           
    da_tijd_eindstatus = Column(Time)            
    ma_gewicht = Column(Integer)
    ma_breedte = Column(Integer)
    ma_lengte = Column(Integer)
    ma_hoogte = Column(Integer)
    ma_volume = Column(Integer)
    PC4_gea = Column(Integer)
    da_landcode_gea = Column(String)               
    da_resultaatgroepcode = Column(String)
    da_resultaatcode = Column(String)
    da_type_adres_gea = Column(String)          
    da_waarnemingsequence = Column(String)

engine = create_engine('sqlite:///../PostNL_SQLite.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Read the CSV file
df_delivery_preference = pd.read_csv(os.path.join('..', 'PostNL_account_delivery_preference_anonymized.csv'))
date_format = "%Y-%m-%d %H:%M:%S.%f"

# Insert delivery preference data into the database
for index, row in df_delivery_preference.iterrows():
    # Check if 'datelastupdated' is a string and convert it, otherwise use None or a default value
    if isinstance(row['datelastupdated'], str):
        datelastupdated = datetime.strptime(row['datelastupdated'], date_format)
    else:
        datelastupdated = None 

    # Do the same for 'datecreated'
    if isinstance(row['datecreated'], str):
        datecreated = datetime.strptime(row['datecreated'], date_format)
    else:
        datecreated = None  # Or a default value

    # Create a new DeliveryPreference object with datetime objects
    new_delivery_preference = DeliveryPreference(
                                account_id_hashed=row['account_id_hashed'],
                                deliverypreference=row['deliverypreference'],
                                datelastupdated=datelastupdated,
                                datecreated=datecreated)
    session.add(new_delivery_preference)

df_delivery_facts = pd.read_csv(os.path.join('..', 'PostNL_account_delivery_facts_anonymized.csv'))

for index, row in df_delivery_facts.iterrows():
    new_delivery_facts = DeliveryFacts(
                            account_id_hashed=row['account_id_hashed'],
                            month_id=row['month_id'],
                            number_of_parcels=row['number_of_parcels'],
                            parcels_home_1st=row['parcels_home_1st'])
    session.add(new_delivery_facts)

df_collo_packages = pd.read_csv(os.path.join('..', 'PostNL_collo_packages_anonymized.csv'))

def convert_to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date() if date_string else None
def convert_to_time(time_string):
    if time_string != 'Nvt':
        return datetime.strptime(time_string, "%H:%M:%S").time() if time_string else None
    else:
        return None

for index, row in df_collo_packages.iterrows():
    new_collo_packages = ColloPackages(
                            account_id_hashed=row['account_id_hashed'],
                            dn_barcode=row['dn_barcode'],
                            da_datum_voormelding=convert_to_date(row['da_datum_voormelding']),
                            da_datum_acceptatie=convert_to_date(row['da_datum_acceptatie']),
                            da_tijd_acceptatie=convert_to_time(row['da_tijd_acceptatie']),
                            sa_dag_sortering1=convert_to_date(row['sa_dag_sortering1']),
                            sa_datum_sortering1=convert_to_date(row['sa_datum_sortering1']),
                            sa_tijd_sortering1=convert_to_time(row['sa_tijd_sortering1']),
                            sa_datum_distributiecollectie=convert_to_date(row['sa_datum_distributiecollectie']),
                            sa_tijd_distributiecollectie=convert_to_time(row['sa_tijd_distributiecollectie']),
                            da_datum_herroutering_voor_up1=convert_to_date(row['da_datum_herroutering_voor_up1']),
                            da_tijd_herroutering_voor_up1=convert_to_time(row['da_tijd_herroutering_voor_up1']),
                            da_datum_eindstatus=convert_to_date(row['da_datum_eindstatus']),
                            da_tijd_eindstatus=convert_to_time(row['da_tijd_eindstatus']),
                            ma_gewicht=row['ma_gewicht'],
                            ma_breedte=row['ma_breedte'],
                            ma_lengte=row['ma_lengte'],
                            ma_hoogte=row['ma_hoogte'],
                            ma_volume=row['ma_volume'],
                            PC4_gea=row['PC4_gea'],
                            da_landcode_gea=row['da_landcode_gea'],
                            da_resultaatgroepcode=row['da_resultaatgroepcode'],
                            da_resultaatcode=row['da_resultaatcode'],
                            da_type_adres_gea=row['da_type_adres_gea'],
                            da_waarnemingsequence=row['da_waarnemingsequence'])
    session.add(new_collo_packages)

session.commit()

print("Data has been inserted into the PostNL database")