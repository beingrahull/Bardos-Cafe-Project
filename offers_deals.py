import sys
sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine, text

engine=create_engine("mysql+pymysql://root:iamrahul@127.0.0.1:3306/bardos_cafe")


def load_offers_deals_items():
    with engine.connect() as connection:
        offers_deals=connection.execute(text("select * from offers_deals")).mappings().all()
        return offers_deals
load_offers_deals_items()

