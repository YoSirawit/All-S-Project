""" connection with database"""
from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://0tlrgkfn0wnz2f3m3g75:pscale_pw_Cn4g8I7djlxcVsbFz1I1qOwp9tmNlpdD1dYTldoT0xh@aws.connect.psdb.cloud/itrestaurant?charset=utf8mb4"

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
        order = conn.execute(text("SELECT menu FROM orders WHERE shopname = \"{0}\" ORDER BY  time_want".format(shopnames)))

    return order.all()

def add_data(user_name, type_user, phone, mail, password):
    with engine.connect() as conn:
        conn.execute(text(f"INSERT INTO userid(username, typeuser, telephone, email, user_pass) VALUES('{user_name}', {type_user}, '{phone}', '{mail}', '{password}');"))

def find_user(email, password):
    with engine.connect() as conn:
        user = conn.execute(text(f"SELECT username FROM userid WHERE email = '{email}' AND user_pass = '{password}'"))

    return user.all()
