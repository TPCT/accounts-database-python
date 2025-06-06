import math
import re

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, FastAPI
from Core.Mongo import *
from Core.Config import limiter
from Models.Account import *
from Models.Profile import *
from Models.ItemStats import *
from Models.Xp import *
from Models.Item import *
from Models.Items import *
from Models.Category import *
from Models.AccountWorth import *
from Requests.Filter import *
from operator import itemgetter
from bson.regex import Regex


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
        return await accounts_collection.find({}, {
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
        if (account := await accounts_collection.find_one({"_id": ObjectId(id)})) is not None:
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
    async def item_stats( id: str):
        if (account := await accounts_collection.find_one({"_id": ObjectId(id)})) is not None:
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
    async def item_stats( id: str):
        if (account := await accounts_collection.find_one({"_id": ObjectId(id)})) is not None:
            return account.get('account_worth', {
                'crowns': "Not Loaded Yet",
                'coins': "Not Loaded Yet",
                'gems': "Not Loaded Yet",
                "free": "Not Loaded Yet"
            })
        raise HTTPException(status_code=404, detail="Account not found")

    @staticmethod
    @Router.get(
        "/{id}/xp",
        response_description="getting account xp data",
        response_model=List[Xp],
        response_model_by_alias=False
    )
    async def xp( id: str):
        if (account := await accounts_collection.find_one({"_id": ObjectId(id)})) is not None:
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
        response_model=Items,
        response_model_by_alias=False
    )
    async def items(id: str, filters: Filter = Depends(Filter)):
        if (account := await accounts_collection.find_one({"_id": ObjectId(id)})) is not None:
            account_filters = {
                'user_id': account['user_id']
            }
            if filters.category is not None:
                account_filters['category'] = filters.category
                if filters.sub_category:
                    account_filters['sub_category'] = filters.sub_category

            if filters.availability is not None:
                account_filters['hidden'] = not filters.availability

            if filters.currency is not None:
                account_filters['currency'] = filters.currency

            if filters.keyword is not None:
                account_filters['name'] = Regex(".*" + filters.keyword + ".*", re.IGNORECASE)

            items = items_collection.find(account_filters)
            pages = math.ceil(await items_collection.count_documents(account_filters) / 10) - 1

            sorting_filter = {}

            if filters.price_sort is not None:
                sorting_filter['price'] = -1 if filters.price_sort == "desc" else 1

            if filters.release_date_sort is not None:
                sorting_filter['release_date'] = -1 if filters.release_date_sort == "desc" else 1

            if filters.page > 1:
                items = items.skip(filters.page * 10).limit(10)

            if sorting_filter:
                items = items.sort(sorting_filter)

            return Items(items=await items.to_list(10), pages=pages)
        raise HTTPException(status_code=404, detail="Account not found")

    @staticmethod
    @Router.get(
        "/items/categories",
        response_description="getting account items categories",
        response_model=List[Category],
        response_model_by_alias=False
    )
    async def categories():
        categories = await categories_collection.find({}).to_list(10000)
        output = []
        for category in categories:
            del category['_id']
            category['sub_categories'] = [sub_category['name'] for sub_category in await sub_categories_collection.find({"category": category['name']}).to_list(10000)]
            output.append(category)
        return output