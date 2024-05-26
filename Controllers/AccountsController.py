from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from Core.Mongo import collection
from Models.Account import *
from Models.Profile import *
from Models.ItemStats import *
from Models.Xp import *
from Models.Item import *
from Models.Category import *
from Models.AccountWorth import *
from Requests.Filter import *
from operator import itemgetter


class AccountsController:
    Router: APIRouter = APIRouter(prefix="/accounts")

    @staticmethod
    @Router.get(
        "",
        name="accounts.index",
        response_description="accounts listing",
        response_model=List[Account],
        response_model_by_alias=False
    )
    async def index():
        return await collection.find({}, {
            '_id': 1,
            'account_profile_image': 1,
            'title': 1,
            'buy_now': 1,
            'account_gender': 1
        }).to_list(1000)

    @staticmethod
    @Router.get(
        "/{id}/profile",
        response_description="getting account profile data",
        response_model=Profile,
        response_model_by_alias=False
    )
    async def profile(id: str):
        if (account := await collection.find_one({"_id": ObjectId(id)})) is not None:
            account = account['profile']['result']
            account['username'] = account['username'][:-len(account['username'])//2] + "*" * (len(account['username']) // 2)
            account['views'] = account['hits']
            return account
        raise HTTPException(status_code=404, detail="Account not found")

    @staticmethod
    @Router.get(
        "/{id}/item_stats",
        response_description="getting account item stats data",
        response_model=ItemStats,
        response_model_by_alias=False
    )
    async def item_stats(id: str):
        if (account := await collection.find_one({"_id": ObjectId(id)})) is not None:
            item_stats = account['item_stats']['result']
            output = {}
            for item_stat in item_stats:
                output[item_stat.replace('owned_', '')] = item_stats[item_stat]
            return output
        raise HTTPException(status_code=404, detail="Account not found")

    @staticmethod
    @Router.get(
        "/{id}/account_worth",
        response_description="getting account worth",
        response_model=AccountWorth,
        response_model_by_alias=False
    )
    async def item_stats(id: str):
        if (account := await collection.find_one({"_id": ObjectId(id)})) is not None:
            return account['account_worth']
        raise HTTPException(status_code=404, detail="Account not found")

    @staticmethod
    @Router.get(
        "/{id}/xp",
        response_description="getting account xp data",
        response_model=List[Xp],
        response_model_by_alias=False
    )
    async def xp(id: str):
        if (account := await collection.find_one({"_id": ObjectId(id)})) is not None:
            xps = account['xp']['result']['lkwd']
            output = []
            for xp in xps:
                xp_data = {"name": xp}
                xp_data.update(xps[xp])
                output.append(xp_data)
            return output
        raise HTTPException(status_code=404, detail="Account not found")

    @staticmethod
    @Router.get(
        "/{id}/items",
        response_description="getting account items data",
        response_model=List[Item],
        response_model_by_alias=False
    )
    async def items(id: str, filters: Filter = Depends(Filter)):
        if (account := await collection.find_one({"_id": ObjectId(id)}, {'item_details': 1})) is not None:
            items = account['item_details']
            item_data = []

            if filters.category:
                item_data = items.get(filters.category, [])
                if filters.sub_category:
                    item_data = [item for item in item_data if item['sub_category'] == filters.sub_category]
            else:
                for category in items:
                    item_data.extend(items[category])

            if filters.price_sort:
                item_data = sorted(item_data, key=itemgetter('price'), reverse=filters.price_sort == "desc")

            if filters.release_date_sort:
                item_data = sorted(item_data, key=itemgetter('release_date'), reverse=filters.release_date_sort == "desc")

            if filters.availability is not None:
                item_data = [item for item in item_data if item['hidden'] != filters.availability]

            if filters.currency:
                item_data = [item for item in item_data if item['currency'] == filters.currency]

            if filters.keyword:
                item_data = [item for item in item_data if filters.keyword.lower() in item['name'].lower()]

            return item_data[(filters.page - 1) * 10: (filters.page * 10)]
        raise HTTPException(status_code=404, detail="Account not found")

    @staticmethod
    @Router.get(
        "/{id}/items/categories",
        response_description="getting account items categories",
        response_model=List[Category],
        response_model_by_alias=False
    )
    async def categories(id: str):
        if (account := await collection.find_one({"_id": ObjectId(id)})) is not None:
            items = account['item_details']
            categories = []
            for category in items:
                category = {
                    "name": category,
                    "sub_categories": []
                }
                for item in items[category['name']]:
                    if item['sub_category'] not in category['sub_categories']:
                        category["sub_categories"].append(item['sub_category'])
                categories.append(category)
            return categories
        raise HTTPException(status_code=404, detail="Account not found")
