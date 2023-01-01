from . import engine, models
from sqlalchemy.orm import Session


def add_user(telegram_id:str):
    if not check_user(telegram_id):
        with Session(engine) as session:
            session.add(models.User(telegram_id=telegram_id))
            session.commit()
        
def check_user(telegram_id:str):
    with Session(engine) as session:
        data = session.query(models.User).filter(models.User.telegram_id==telegram_id).first()
        return True if data else False
    

def get_users() -> list[str]:
    with Session(engine) as session:
        data = session.query(models.User)
        return [el.telegram_id for el in data]