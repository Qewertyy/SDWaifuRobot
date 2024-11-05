from typing import Optional

from pony import orm
from datetime import datetime

from config import Config
from bot import LOGGER

db = orm.Database()


class User(db.Entity):
    __table__ = "users"
    id = orm.PrimaryKey(int, size=64)
    name = orm.Required(str)
    username = orm.Optional(str, nullable=True)
    banned = orm.Optional(bool, default=False)
    created_at = orm.Required(datetime, default=datetime.now())


class Message(db.Entity):
    __table__ = "messages"
    chat_id = orm.Required(int, size=64)
    role = orm.Required(str)
    content = orm.Required(str)


if not any((Config.DB_HOST, Config.DB_USER, Config.DB_PASSWORD, Config.DB_NAME)):
    LOGGER.warning("External Database not configured. Using SQLite instead.")
    db.bind(provider="sqlite", filename="sql.db", create_db=True)

else:
    db.bind(
        provider="postgres",
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        sslmode="require",
    )
    LOGGER.info("Postgres Database configured.")

db.generate_mapping(create_tables=True)

async def add_user(id: int, name: str, username: Optional[str]):
    with orm.db_session:
        if not User.exists(id=id):
            try:
                User(id=id, name=name, username=username)
            except (orm.IntegrityError, orm.TransactionIntegrityError):
                return False
            return True
        return False

def user_exists(user_id: int):
    with orm.db_session:
        return User.exists(id=user_id)

async def set_user_input(user_id: int,  message: str):
    with orm.db_session:
        Message(chat_id=user_id, content=message, role="user")
        db.commit()


async def set_model_response(user_id: int, message: str):
    with orm.db_session:
        Message(chat_id=user_id, content=message, role="assistant")
        db.commit()

async def ban_user(user_id: int):
    with orm.db_session:
        user = User.get(id=user_id)
        if user:
            user.banned = True
            db.commit()


async def get_messages(user_id: int) -> list[Message]:
    with orm.db_session:
        return list(
            reversed(
                list(
                    Message.select(lambda h: h.chat_id == user_id)
                    .order_by(orm.desc(Message.id))
                    .limit(10)
                )
            )
        )


async def clear_history(user_id: int):
    with orm.db_session:
        orm.select(h for h in Message if h.chat_id == user_id).delete(bulk=True)