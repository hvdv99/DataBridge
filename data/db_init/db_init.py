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

def create_full_database():
    engine = create_engine('sqlite:///../PostNL_Full_SQLite.sqlite')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Read the CSV files
    df_delivery_preference = pd.read_csv(os.path.join('..', 'PostNL_account_delivery_preference_anonymized.csv'))
    df_delivery_facts = pd.read_csv(os.path.join('..', 'PostNL_account_delivery_facts_anonymized.csv'))
    df_collo_packages = pd.read_csv(os.path.join('..', 'PostNL_collo_packages_anonymized.csv'))

    # Insert data into the database
    for index, row in df_delivery_preference.iterrows():
        datelastupdated = datetime.strptime(row['datelastupdated'], "%Y-%m-%d %H:%M:%S.%f") if isinstance(row['datelastupdated'], str) else None
        datecreated = datetime.strptime(row['datecreated'], "%Y-%m-%d %H:%M:%S.%f") if isinstance(row['datecreated'], str) else None
        new_delivery_preference = DeliveryPreference(
                                    account_id_hashed=row['account_id_hashed'],
                                    deliverypreference=row['deliverypreference'],
                                    datelastupdated=datelastupdated,
                                    datecreated=datecreated)
        session.add(new_delivery_preference)

    for index, row in df_delivery_facts.iterrows():
        new_delivery_facts = DeliveryFacts(
                                account_id_hashed=row['account_id_hashed'],
                                month_id=row['month_id'],
                                number_of_parcels=row['number_of_parcels'],
                                parcels_home_1st=row['parcels_home_1st'])
        session.add(new_delivery_facts)

    for index, row in df_collo_packages.iterrows():
        new_collo_packages = ColloPackages(
                                account_id_hashed=row['account_id_hashed'],
                                dn_barcode=row['dn_barcode'],
                                da_datum_voormelding=row['da_datum_voormelding'],
                                da_datum_acceptatie=row['da_datum_acceptatie'],
                                da_tijd_acceptatie=row['da_tijd_acceptatie'],
                                sa_dag_sortering1=row['sa_dag_sortering1'],
                                sa_datum_sortering1=row['sa_datum_sortering1'],
                                sa_tijd_sortering1=row['sa_tijd_sortering1'],
                                sa_datum_distributiecollectie=row['sa_datum_distributiecollectie'],
                                sa_tijd_distributiecollectie=row['sa_tijd_distributiecollectie'],
                                da_datum_herroutering_voor_up1=row['da_datum_herroutering_voor_up1'],
                                da_tijd_herroutering_voor_up1=row['da_tijd_herroutering_voor_up1'],
                                da_datum_eindstatus=row['da_datum_eindstatus'],
                                da_tijd_eindstatus=row['da_tijd_eindstatus'],
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
    print("Data has been inserted into the PostNL Full database")

def create_sample_database():
    engine = create_engine('sqlite:///../PostNL_Sample_SQLite.sqlite')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Read the CSV files
    df_delivery_preference = pd.read_csv(os.path.join('..', 'PostNL_account_delivery_preference_anonymized.csv'))
    df_delivery_facts = pd.read_csv(os.path.join('..', 'PostNL_account_delivery_facts_anonymized.csv'))
    df_collo_packages = pd.read_csv(os.path.join('..', 'PostNL_collo_packages_anonymized.csv'))

    # Insert a subset of data into the sample database - it's half now, but that can be changed if we want
    num_records_to_insert = min(len(df_delivery_preference), len(df_delivery_facts), len(df_collo_packages)) // 2

    for index, row in df_delivery_preference.iloc[:num_records_to_insert].iterrows():
        datelastupdated = datetime.strptime(row['datelastupdated'], "%Y-%m-%d %H:%M:%S.%f") if isinstance(row['datelastupdated'], str) else None
        datecreated = datetime.strptime(row['datecreated'], "%Y-%m-%d %H:%M:%S.%f") if isinstance(row['datecreated'], str) else None
        new_delivery_preference = DeliveryPreference(
                                    account_id_hashed=row['account_id_hashed'],
                                    deliverypreference=row['deliverypreference'],
                                    datelastupdated=datelastupdated,
                                    datecreated=datecreated)
        session.add(new_delivery_preference)

    for index, row in df_delivery_facts.iloc[:num_records_to_insert].iterrows():
        new_delivery_facts = DeliveryFacts(
                                account_id_hashed=row['account_id_hashed'],
                                month_id=row['month_id'],
                                number_of_parcels=row['number_of_parcels'],
                                parcels_home_1st=row['parcels_home_1st'])
        session.add(new_delivery_facts)

    for index, row in df_collo_packages.iloc[:num_records_to_insert].iterrows():
        new_collo_packages = ColloPackages(
                                account_id_hashed=row['account_id_hashed'],
                                dn_barcode=row['dn_barcode'],
                                da_datum_voormelding=row['da_datum_voormelding'],
                                da_datum_acceptatie=row['da_datum_acceptatie'],
                                da_tijd_acceptatie=row['da_tijd_acceptatie'],
                                sa_dag_sortering1=row['sa_dag_sortering1'],
                                sa_datum_sortering1=row['sa_datum_sortering1'],
                                sa_tijd_sortering1=row['sa_tijd_sortering1'],
                                sa_datum_distributiecollectie=row['sa_datum_distributiecollectie'],
                                sa_tijd_distributiecollectie=row['sa_tijd_distributiecollectie'],
                                da_datum_herroutering_voor_up1=row['da_datum_herroutering_voor_up1'],
                                da_tijd_herroutering_voor_up1=row['da_tijd_herroutering_voor_up1'],
                                da_datum_eindstatus=row['da_datum_eindstatus'],
                                da_tijd_eindstatus=row['da_tijd_eindstatus'],
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
    print("Data has been inserted into the PostNL Sample database")