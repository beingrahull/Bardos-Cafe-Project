from sqlalchemy import create_engine, text

engine=create_engine("mysql+pymysql://root:iamrahul@127.0.0.1:3306/bardos_cafe")


def load_savory_bites_items():
    with engine.connect() as connection:
        savory_bites_items=connection.execute(text("select * from savory_bites")).mappings().all()
        return savory_bites_items
load_savory_bites_items()
