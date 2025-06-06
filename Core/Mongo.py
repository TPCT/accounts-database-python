from motor.motor_asyncio import AsyncIOMotorClient
from Core.Config import *
from typing_extensions import Annotated
from pydantic import BeforeValidator


client = AsyncIOMotorClient(MONGO_DB)
database = client.account_selling
accounts_collection = database.accounts
categories_collection = database.categories
sub_categories_collection = database.sub_categories
items_collection = database.items


PyObjectId = Annotated[str, BeforeValidator(str)]


if __name__ == '__main__':
    import asyncio
    import pprint
    from bson import ObjectId

    async def main():
        account_data = await collection.find_one({'_id': ObjectId('664ff17b6004ad838318286b')}, {'item_details': 1})
        pprint.pprint(account_data.item_details)

    asyncio.run(main())