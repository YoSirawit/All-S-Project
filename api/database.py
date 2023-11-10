""" connection with database"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_connection_string = os.getenv('DB_CONNECTION')

engine = create_engine(
    db_connection_string, 
    connect_args={
        "ssl":{
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })

conn = engine.connect()

def load_userid_from_db():
    #with engine.connect() as conn:
    userid = conn.execute(text("select * from userid"))
    userid_dict = [i._asdict() for i in userid.all()]

    return userid_dict

def shopname():
    #with engine.connect() as conn:
    shopnames = conn.execute(text("select shopname from shoplist"))

    return shopnames.all()

def orders(shopnames):
    #with engine.connect() as conn:
    order = conn.execute(text("SELECT * FROM orders WHERE shopname = \"{0}\" ORDER BY time_want".format(shopnames)))

    return order.all()

def add_data(user_name, type_user, phone, mail, password):
    #with engine.connect() as conn:
    conn.execute(text(f"INSERT INTO userid(username, typeuser, telephone, email, user_pass) VALUES('{user_name}', {type_user}, '{phone}', '{mail}', '{password}');"))

def find_user(email, password):
    #with engine.connect() as conn:
    user = conn.execute(text(f"SELECT * FROM userid WHERE email = '{email}' AND user_pass = '{password}'"))

    return user.all()

def get_shop_id(shopnames):
    shop_id = conn.execute(text(f'SELECT * FROM shoplist WHERE shopname = "{shopnames}"'))

    return shop_id.all()

def add_menu(user_name, time_want, menu, shopname):
    #with engine.connect() as conn:
    conn.execute(text(f"INSERT INTO orders(username, time_want, menu, shopname) VALUES('{user_name}', '{time_want}', '{menu}', '{shopname}');"))

def delete_order(menu_id):
    conn.execute(text(f"DELETE FROM orders WHERE id={menu_id}"))
 