from fastapi import HTTPException, APIRouter

from .exceptions import (
    ListingNotFoundException, 
    InvalidListingDataException, 
    InternalServerErrorException,
    is_valid_listing
)

from .schemas import (
    ListingCreate,
    ListingUpdate
)

router = APIRouter()

@router.post("/api/listing/")
async def create_listing(listing: ListingCreate):
    try:
        if not is_valid_listing(listing):
            raise InvalidListingDataException()
        # new_listing = await save_listing_to_db(listing)
        # return new_listing
    except InvalidListingDataException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(f"Ошибка при создании объявления: {str(e)}")