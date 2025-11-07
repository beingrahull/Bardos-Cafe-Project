from sqlalchemy import create_engine, text

engine=create_engine("mysql+pymysql://root:iamrahul@127.0.0.1:3306/bardos_cafe")


def load_bakery_pastries_items():
    with engine.connect() as connection:
        bakery_pastries_items=connection.execute(text("select * from bakery_pastries")).mappings().all()
        return bakery_pastries_items
load_bakery_pastries_items()
