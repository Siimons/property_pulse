from typing import Dict, Any, List 
from loguru import logger

from .database import DatabaseExecutor

class ListingService(DatabaseExecutor):
    """
    Класс для работы с объявлениями. Наследуется от DatabaseExecutor для получения доступа к методам работы с базой данных.
    """

    async def save_listing_to_db(self, listing: Dict[str, Any]) -> None:
        """
        Сохранение объявления в базе данных.
        
        Args:
            listing (Dict[str, Any]): Объявление для сохранения.
        """
        query = """
        INSERT INTO listings (title, description, price, deal_type, rooms, area, location, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (
            listing['title'],
            listing.get('description'),
            listing['price'],
            listing['deal_type'],
            listing.get('rooms'),
            listing.get('area'),
            listing.get('location')
        )
        
        try:
            await self.execute_query(query, params)
            logger.info("Объявление успешно сохранено в базе данных.")
        except Exception as e:
            logger.error(f"Ошибка при сохранении объявления: {e}")
            raise

    async def get_all_listings(self) -> List[Dict[str, Any]]:
        """
        Получение всех объявлений из базы данных.
        
        Returns:
            List[Dict[str, Any]]: Список объявлений.
        """
        query = "SELECT * FROM listings"
        
        try:
            result = await self.execute_query(query, fetch=True)
            logger.info("Объявления успешно получены из базы данных.")
            return result
        except Exception as e:
            logger.error(f"Ошибка при получении объявлений: {e}")
            raise
