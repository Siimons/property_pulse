from typing import Any, List, Optional
from decouple import config
import aiomysql
from aiomysql import Pool
from loguru import logger

class DBConfig:
    """
    Класс конфигурации для базы данных.
    """
    HOST = config('HOST', default='localhost')
    DATABASE = config('DATABASE', default='mydb')
    USER = config('USER', default='root')
    PASSWORD = config('PASSWORD', default='password')

    @classmethod
    def validate(cls):
        """
        Проверяем конфигурацию.
        """
        if not cls.HOST or not cls.DATABASE or not cls.USER or not cls.PASSWORD:
            raise ValueError("Все параметры базы данных (HOST, DATABASE, USER, PASSWORD) должны быть заданы.")


class DatabaseExecutor(DBConfig):
    """
    Базовый класс для работы с базой данных.
    """
    db_pool: Pool = None

    async def init_db_pool(self) -> Pool:
        """
        Инициализация пула соединений.
        """
        if not self.db_pool:
            try:
                self.db_pool = await aiomysql.create_pool(
                    host=self.HOST,
                    db=self.DATABASE,
                    user=self.USER,
                    password=self.PASSWORD,
                    minsize=1,
                    maxsize=10,
                )
                logger.info("Пул соединений успешно создан.")
            except Exception as e:
                logger.error(f"Ошибка при создании пула соединений: {e}")
                raise
        return self.db_pool

    async def close_db_pool(self):
        """
        Закрытие пула соединений.
        """
        if self.db_pool:
            self.db_pool.close()
            await self.db_pool.wait_closed()
            logger.info("Пул соединений закрыт.")

    async def execute_query(self, query: str, params: Optional[List[Any]] = None, fetch: bool = False) -> Optional[List[Any]]:
        """
        Выполнение SQL-запроса.
        
        Args:
            query (str): SQL-запрос для выполнения.
            params (Optional[List[Any]]): Параметры для запроса.
            fetch (bool): Если True, выполняется SELECT и возвращаются данные.
        
        Returns:
            Optional[List[Any]]: Результаты запроса для SELECT, иначе None.
        """
        pool = await self.init_db_pool()

        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, params)
                    
                    if fetch:
                        result = await cursor.fetchall()
                        logger.info(f"Выполнен запрос: {query}")
                        return result

                    await connection.commit()
                    logger.info(f"Выполнен запрос: {query} с параметрами: {params}")

        except Exception as e:
            logger.error(f"Ошибка выполнения запроса: {query}, параметры: {params}, ошибка: {e}")
            raise

        return None
