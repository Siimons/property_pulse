import importlib
import inspect

from asyncio import sleep
import asyncio
import aiohttp

from loguru import logger
from random import randint

class Controller:
    def __init__(self, script_name: str, user_agent: str, base_url: str):
        """
        Инициализация контроллера для парсинга.
        
        :param script_name: Имя скрипта (модуля), который будет загружен для парсинга.
        :param user_agent: Пользовательский агент, который будет использоваться в запросах.
        :param base_url: Базовый URL для взаимодействия с сервером (API).
        """
        self.script_name = script_name  # Название скрипта, который будет загружаться
        self.user_agent = user_agent  # Пользовательский агент для запросов
        self.base_url = base_url  # Базовый URL для API
        logger.info(f"Controller initialized with script: {self.script_name}, base_url: {self.base_url}")

    async def clear_data(self, parser_name: str):
        """
        Асинхронная очистка старых данных на сервере перед парсингом.
        
        :param parser_name: Название парсера, данные которого нужно очистить.
        """
        logger.debug(f"Clearing data for parser: {parser_name}")
        payload = {'parser': parser_name}
        try:
            # Асинхронный запрос на очистку данных
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/clear_data/", json=payload) as response:
                    if response.status != 200:
                        logger.error(f"Failed to clear data: {response.status}")
                    else:
                        logger.info(f"Data cleared for parser: {parser_name}")
        except Exception as e:
            logger.error(f"Error while clearing data: {e}")

    async def load_script(self):
        """
        Динамическая загрузка модуля для парсинга.
        """
        logger.debug(f"Loading script: {self.script_name}")
        try:
            parser_module = importlib.import_module(self.script_name)
            for name in dir(parser_module):
                obj = getattr(parser_module, name)
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, Parser)
                    and obj != Parser
                ):
                    logger.info(f"Parser {name} loaded successfully.")
                    return obj()
        except Exception as e:
            logger.error(f"Failed to load parser: {e}")
            return None

    async def run(self):
        """
        Запуск парсера. Очищает старые данные, а затем запускает основной процесс парсинга.
        """
        logger.info(f"Starting the controller for script: {self.script_name}")
        script = await self.load_script()
        if script:
            # Очищаем данные перед запуском
            await self.clear_data(script.name)
            try:
                # Запускаем основной процесс парсинга
                await script.main()
            except AttributeError as e:
                logger.error(f"Parser error: {e}")
                return
            logger.info(f"The script {script.name} completed successfully.")
            if script.session is not None:
                await script.session.close()

class Parser(Controller):
    def __init__(self, script_name: str, base_url: str, headers=None, proxies=None):
        """
        Инициализация парсера с базовыми параметрами (URL, заголовки, прокси).

        :param script_name: Название скрипта для загрузки
        :param base_url: URL для парсинга
        :param headers: Заголовки для HTTP-запросов
        :param proxies: Прокси для обхода блокировок
        """
        super().__init__(script_name=script_name, user_agent=headers['User-Agent'] if headers else None, base_url=base_url)
        self.headers = headers if headers else {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.proxies = proxies  # Для прокси можно добавить поддержку aiohttp прокси

    async def fetch_page(self, url, params=None, retries=3):
        """
        Асинхронное получение HTML-страницы с URL.

        :param url: URL для запроса
        :param params: Дополнительные параметры для GET-запроса
        :param retries: Количество попыток
        :return: HTML-содержимое страницы или None в случае неудачи
        """
        for attempt in range(retries):
            try:
                logger.info(f"Запрос к странице: {url}, Попытка: {attempt+1}")
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url, params=params, proxy=self.proxies) as response:
                        response.raise_for_status()  # Проверка на ошибки HTTP
                        html = await response.text()
                        return html
            except aiohttp.ClientError as e:
                logger.error(f"Ошибка запроса: {e}, попытка {attempt + 1}")
                await sleep(randint(1, 3))  # Пауза перед повторной попыткой
        return None

    async def parse_page(self, html):
        """
        Метод парсинга страницы (должен быть переопределен в конкретных парсерах).
        
        :param html: HTML-содержимое страницы
        :return: Извлеченные данные
        """
        raise NotImplementedError("Метод parse_page() должен быть переопределен в подклассах")

    async def run(self):
        """
        Запуск процесса парсинга.
        """
        logger.info(f"Запуск парсинга URL: {self.base_url}")
        html = await self.fetch_page(self.base_url)
        if html:
            return await self.parse_page(html)
        else:
            logger.error(f"Не удалось получить данные с {self.base_url}")
            return None