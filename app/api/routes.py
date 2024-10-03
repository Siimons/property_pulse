from fastapi import HTTPException, APIRouter
from loguru import logger

from app.storage.queries import ListingService

from .exceptions import (
    InvalidListingDataException, 
    InternalServerErrorException,
    is_valid_listing
)

from .schemas import (
    ListingCreate
) 

router = APIRouter()

listing_service = ListingService()

@router.post("/api/listing/")
async def create_listing(listing: ListingCreate):
    try:
        if not is_valid_listing(listing):
            logger.warning(f"Invalid listing data: {listing}")
            raise InvalidListingDataException()

        await listing_service.save_listing_to_db(listing)
        
        logger.info("Listing successfully created.")
        return {"message": "Listing created successfully"}

    except InvalidListingDataException as e:
        logger.error(f"Listing validation failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid listing data.")
    
    except Exception as e:
        logger.error(f"Internal server error while creating listing: {e}")
        raise InternalServerErrorException(f"Ошибка при создании объявления: {str(e)}")
