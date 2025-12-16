import streamlit as st
from sqlalchemy import create_engine, Table, \
Column, Integer, String, MetaData
import pandas as pd
from faker import Faker
from streamlit_autorefresh import st_autorefresh

import os

if 'DB_PASSWORD' in os.environ:
    db_password = os.environ['DB_PASSWORD']
    # 환경변수가 있으면, 앱 코드들
    st.write(db_password)
else:
    # 없으면,
    st.error('환경변수를 입력해주세요.')


engine = create_engine('sqlite:///users.db')
metadata = MetaData()

users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('address', String) )

metadata.create_all(engine)

fake = Faker()

def generate_fake_data(n=10):
    with engine.connect() as conn:
        conn.execute(users_table.delete())
    
        for _ in range(n):
            # Object Relation Mapping (ORM)
            # 파이썬 object로 db의 relation으로 mapping해주는 것
            # SQL문으로 바꿔주는 기능이 들어가있다.
            print('insert sql: ', users_table.insert().values(
                    name = fake.name(),
                    email = fake.email(),
                    address = fake.address()
                )
            )
            conn.execute(
                users_table.insert().values(
                    name = fake.name(),
                    email = fake.email(),
                    address = fake.address()
                ))
        conn.commit()

if st.button('Generate Fake Data'):
    generate_fake_data(20)
    st.success('Fake data generated!')

# @st.cache_data
def load_data():
    result = []
    with engine.connect() as conn:
        query = "SELECT * FROM users"
        # for row in conn.execute(users_table.select()):
            # print(row.id) # row.Row 객체
            # result.append(row)
        return pd.read_sql(users_table.select(), conn)

data = load_data()
# st.json(data)
st.dataframe(data)

st_autorefresh(interval=3000)