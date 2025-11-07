from sqlalchemy import create_engine, text

engine=create_engine("mysql+pymysql://root:iamrahul@127.0.0.1:3306/bardos_cafe")


def load_coffee_items():
    with engine.connect() as connection:
        coffee_items=connection.execute(text("select * from coffee")).mappings().all()
        return coffee_items
load_coffee_items()
