""" connection with database"""
from sqlalchemy import create_engine, text
from flask_mysqldb import MySQL

db_connection_string = "mysql+pymysql://84vq5ilryqpjtctnvf28:pscale_pw_T8kgj3hNDost8moUhm8DYWbOCZuyXZLgbyeLwJQInLL@aws.connect.psdb.cloud/itrestaurant?charset=utf8mb4"

engine = create_engine(
    db_connection_string, 
    connect_args={
        "ssl":{
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })

def load_userid_from_db():
    with engine.connect() as conn:
        userid = conn.execute(text("select * from userid"))
        userid_dict = [i._asdict() for i in userid.all()]

    return userid_dict

def shopname():
    with engine.connect() as conn:
        shopnames = conn.execute(text("select shopname from shoplist"))

    return shopnames.all()
