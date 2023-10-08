""" connection with database"""
from sqlalchemy import create_engine, text
from flask_mysqldb import MySQL

db_connection_string = "mysql+pymysql://2v71n11d5258z7xmb138:pscale_pw_yUeNiTZTrvyiWx6hJDz10nMscbLh2Zs4p7Jq4UZDcpn@aws.connect.psdb.cloud/itrestaurant?charset=utf8mb4"

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
        shopnames = list(conn.execute(text("select shopname from shoplist")))

    return shopnames
