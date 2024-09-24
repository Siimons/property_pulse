from decouple import config
import aiomysql
from aiomysql import Pool
from typing import Any, List, Optional
from loguru import logger

class DBConfig:
    HOST = config('HOST', default='localhost')
    DATABASE = config('DATABASE', default='mydb')
    USER = config('USER', default='root')
    PASSWORD = config('PASSWORD', default='password')

    @classmethod
    def validate(cls):
        if not cls.HOST or not cls.DATABASE or not cls.USER or not cls.PASSWORD:
            raise ValueError("Все параметры базы данных (HOST, DATABASE, USER, PASSWORD) должны быть заданы.")

# Глобальная переменная для пула соединений
db_pool: Pool = None

async def init_db_pool() -> Pool:
    """
    Инициализация пула соединений к базе данных.
    """
    global db_pool
    DBConfig.validate()
    if not db_pool:
        try:
            db_pool = await aiomysql.create_pool(
                host=DBConfig.HOST,
                db=DBConfig.DATABASE,
                user=DBConfig.USER,
                password=DBConfig.PASSWORD,
                minsize=1,
                maxsize=10,
            )
            logger.info("Пул соединений успешно создан.")
        except Exception as e:
            logger.error(f"Ошибка при создании пула соединений: {e}")
            raise
    return db_pool

async def close_db_pool():
    """
    Закрытие пула соединений.
    """
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        logger.info("Пул соединений закрыт.")

async def execute_query(query: str, params: Optional[List[Any]] = None, fetch: bool = False) -> Optional[List[Any]]:
    """
    Универсальная функция для выполнения SQL-запросов.
    
    Args:
        query (str): SQL-запрос для выполнения.
        params (Optional[List[Any]]): Параметры для запроса.
        fetch (bool): Флаг, указывающий, нужно ли извлечь данные (True для SELECT).
    
    Returns:
        Optional[List[Any]]: Результаты запроса (для SELECT), иначе None.
    """
    pool = await init_db_pool()

    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, params)
                
                if fetch:
                    result = await cursor.fetchall()  # Получить все результаты
                    logger.info(f"Выполнен запрос: {query}")
                    return result

                await connection.commit()  # Подтвердить изменения для INSERT/UPDATE/DELETE
                logger.info(f"Выполнен запрос: {query} с параметрами: {params}")

    except Exception as e:
        logger.error(f"Ошибка выполнения запроса: {query}, параметры: {params}, ошибка: {e}")
        raise

    return None
