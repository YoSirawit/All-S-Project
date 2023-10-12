from sqlalchemy import create_engine, text

db_connection_string = ""

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
