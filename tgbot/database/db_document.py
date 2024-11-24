# - *- coding: utf- 8 - *-
import sqlite3

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format_where, update_format
from tgbot.utils.const_functions import ded, get_unix, gen_id


# Модель таблицы
class DocumentModel(BaseModel):
    increment: int  # Инкремент
    document_id: int  # Айди документа
    document_name: str  # Название документа
    document_info: str  # Инфо документа
    document_unix: int  # Время создания документа


# Работа с юзером
class Documentx:
    storage_name = "storage_documents"

    # Добавление записи
    @staticmethod
    def add(
        document_name: str,
        document_info: str,
    ):
        document_id = gen_id()
        document_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Documentx.storage_name} (
                        document_id,
                        document_name,
                        document_info,
                        document_unix
                    ) VALUES (?, ?, ?, ?)
                """),
                [
                    document_id,
                    document_name,
                    document_info,
                    document_unix,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> DocumentModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Documentx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = DocumentModel(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[DocumentModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Documentx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [DocumentModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[DocumentModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Documentx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [DocumentModel(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(document_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Documentx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(document_id)

            con.execute(sql + "WHERE document_id = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Documentx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Documentx.storage_name}"

            con.execute(sql)
