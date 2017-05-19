# MIT Licensed. Copyright (c) 2017
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

# Setup our connection to the database
engine = create_engine('sqlite+pysqlite:///license_database.sqlite3', module=sqlite3)
Base = automap_base()
Base.prepare(engine, reflect=True)