""" connection with database"""
from sqlalchemy import create_engine, text
from flask_mysqldb import MySQL

db_connection_string = "ตรงนี้ครับ"

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

def orders(shopnames):
    with engine.connect() as conn:
        order = conn.execute(text("SELECT menu FROM orders WHERE shopname = \"{0}\"".format(shopnames)))

    return order.all()

def add_data(user_name, type_user, phone):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO userid(username, typeuser, telephone) VALUES('{0}', {1}, '{2}');".format(user_name, type_user, phone)))
