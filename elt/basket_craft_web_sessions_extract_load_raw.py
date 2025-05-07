"""
1. Import necessary libraries.
2. Load source MySQL and destination Postgres connection details.
3. Build connection strings and create database engines.
4. Read website_sessions for Dec 2023 from MySQL into a DataFrame.
5. Write DataFrame to website_sessions table in Postgres (raw schema).
"""

# %%
import pandas as pd
from sqlalchemy import create_engine


# %%
mysql_user = 'analyst'
mysql_password = 'go_lions'
mysql_host = 'db.isba.co'
mysql_db = 'basket_craft'

pg_user = 'postgres'
pg_password = 'isba_4715'
pg_host = 'isba-dev-02.c7g8wiquaqg7.us-east-1.rds.amazonaws.com'
pg_db = 'basket_craft'

# %%
mysql_conn_str = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
pg_conn_str= f'postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}/{pg_db}'

# %%
mysql_engine = create_engine(mysql_conn_str)
pg_engine= create_engine(pg_conn_str)

# %%
query = """
SELECT *
FROM website_sessions
WHERE created_at >= '2023-12-01'
AND created_at <'2024-01-01'
"""
df = pd.read_sql(query, mysql_engine)

# %%
df.to_sql(
'website_sessions',
pg_engine,
schema='raw',
if_exists='replace',
index=False
)

print(f'{len(df)} records loaded into raw.website_sessions.')

# %%

df