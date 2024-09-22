from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from .schemеs import ListingCreate

"""Исключения для HTTP-ответов"""

class ListingNotFoundException(HTTPException):
    def __init__(self, listing_id: int):
        detail = f"Объявление с ID {listing_id} не найдено."
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)

class ListingAlreadyExistsException(HTTPException):
    def __init__(self, listing_id: int):
        detail = f"Объявление с ID {listing_id} уже существует."
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class InvalidListingHTTPException(HTTPException):
    def __init__(self):
        detail = "Неверные данные для создания или обновления объявления."
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class InternalServerErrorException(HTTPException):
    def __init__(self, message: str = "Произошла внутренняя ошибка сервера"):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=message)


"""Исключения для проверки валидации"""

class InvalidListingDataException(Exception):
    """
    Базовое исключение для неверных данных объявления.
    """
    def __init__(self, message="Данные объявления некорректны"):
        self.message = message
        super().__init__(self.message)

class MissingRequiredFieldException(InvalidListingDataException):
    """
    Исключение для случая, когда отсутствуют обязательные поля.
    """
    def __init__(self, field_name: str):
        super().__init__(f"Обязательное поле '{field_name}' отсутствует.")

class InvalidPriceException(InvalidListingDataException):
    """
    Исключение для случая, когда цена некорректна.
    """
    def __init__(self):
        super().__init__("Цена должна быть положительным числом.")

class InvalidDealTypeException(InvalidListingDataException):
    """
    Исключение для некорректного типа сделки.
    """
    def __init__(self):
        super().__init__("Тип сделки должен быть 'sale' или 'rent'.")

class InvalidRoomsException(InvalidListingDataException):
    """
    Исключение для некорректного количества комнат.
    """
    def __init__(self):
        super().__init__("Количество комнат должно быть положительным целым числом.")

class InvalidAreaException(InvalidListingDataException):
    """
    Исключение для некорректной площади.
    """
    def __init__(self):
        super().__init__("Площадь должна быть положительным числом.")



def is_valid_listing(listing: ListingCreate) -> None:
    """
    Проверяет валидность данных объявления и выбрасывает исключения, если данные некорректны.
    """
    if not listing.title:
        raise MissingRequiredFieldException('title')
    
    if not listing.description:
        raise MissingRequiredFieldException('description')

    if listing.price <= 0:
        raise InvalidPriceException()

    if listing.deal_type not in ["sale", "rent"]:
        raise InvalidDealTypeException()

    if listing.rooms <= 0:
        raise InvalidRoomsException()

    if listing.area <= 0:
        raise InvalidAreaException()
