from sqlalchemy import create_engine, text

engine=create_engine("mysql+pymysql://root:iamrahul@127.0.0.1:3306/bardos_cafe")


def load_breakfast_brunch_items():
    with engine.connect() as connection:
        breakfast_brunch_items=connection.execute(text("select * from breakfast_brunch")).mappings().all()
        return breakfast_brunch_items
load_breakfast_brunch_items()
