import pandas as pd
from sqlalchemy import create_engine

import database

# Connect and read data
engine = create_engine(database.DATABASE_URL)
query = "SELECT age, gender, height, weight, bmi, verdict FROM patients WHERE bmi IS NOT NULL AND verdict IS NOT NULL"
df = pd.read_sql(query, engine)

print(df.head())