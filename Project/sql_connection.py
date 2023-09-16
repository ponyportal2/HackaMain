from sqlalchemy import create_engine
import sqlite3

engine = create_engine("sqlite:///metanit.db", echo=True)
print(engine)
conn = engine.connect()