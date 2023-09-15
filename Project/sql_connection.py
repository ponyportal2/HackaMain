from sqlalchemy import create_engine

engine = create_engine("sqlite:///metanit.db", echo=True)
print(engine)
conn = engine.connect()