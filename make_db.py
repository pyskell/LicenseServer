# MIT Licensed. Copyright (c) 2017
# coding: utf-8
# Run this script to produce the database this program uses
from sqlalchemy import CheckConstraint, Column, Integer, Table, Text, text, create_engine
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
metadata = Base.metadata

class Admin(Base):
    __tablename__ = 'Admins'

    Username = Column(Text, primary_key=True)
    Key = Column(Text, nullable=False)

class Signature(Base):
    __tablename__ = 'Signatures'
    __table_args__ = (
        CheckConstraint('UnlimitedInstalls IN ( 0 , 1 )'),
    )

    PrimaryKey = Column(Text, primary_key=True)
    InstallCount = Column(Integer, nullable=False)
    InstallLimit = Column(Integer, nullable=False)
    UnlimitedInstalls = Column(Integer, nullable=False, server_default=text("0"))

class User(Base):
    __tablename__ = 'Users'

    Signature = Column(Text, primary_key=True, nullable=False)
    UserID = Column(Text, primary_key=True, nullable=False)
    Name = Column(Text, nullable=False)
    Email = Column(Text, nullable=False)
    Company = Column(Text)
    InstallDateTime = Column(Text, nullable=False)

def run_main():
    db_file = 'license_database.sqlite3'
    if os.path.isfile(db_file):
        print("Database already exists.")
        return
    else:
        engine = create_engine('sqlite+pysqlite:///'+db_file, echo=True)
        Base.metadata.create_all(engine)

if __name__ == '__main__':
    run_main()