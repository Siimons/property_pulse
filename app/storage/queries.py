from typing import Dict, Any

from .database import execute_query

async def save_listing_to_db(listing: Dict[str, Any]) -> None:
    """
    Сохранение объявления в базе данных.
    
    Args:
        listing (Dict[str, Any]): Объявление, которое нужно сохранить.
                                   Ожидается, что будет передан словарь с ключами,
                                   соответствующими полям таблицы listings.
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
        await execute_query(query, params)
        logger.info("Объявление успешно сохранено в базе данных.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении объявления: {e}")
        raise
