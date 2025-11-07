from sqlalchemy import create_engine, text

engine=create_engine("mysql+pymysql://root:iamrahul@127.0.0.1:3306/bardos_cafe")


def load_desserts_items():
    with engine.connect() as connection:
        desserts_items=connection.execute(text("select * from desserts")).mappings().all()
        return desserts_items
load_desserts_items()
