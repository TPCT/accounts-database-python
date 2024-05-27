from pymongo import MongoClient

from pymongo import MongoClient
client = MongoClient("mongodb+srv://topgtopg:2IGyXuU4lWhgPRfI@cluster0.ukm3j.mongodb.net/?retryWrites=true&w=majority")
collection = client['account_selling']
account_selling = collection['account_selling']
accounts = collection['accounts']
categories = collection['categories']
sub_categories = collection['sub_categories']
items = collection['items']

for account in account_selling.find():
    if not (db_account := accounts.find_one({'user_id': account['user_id']})):
        db_account = accounts.insert_one({
            'user_id': account['user_id'],
            'gender': account['account_gender'],
            'title': account['title'],
            'profile_image': account['account_profile_image'],
            'buy_now': account['buy_now'],

            'item_stats': account['item_stats'],
            'profile': account['profile'],
            'xp': account['xp'],
            'account_worth': account['account_worth']
        })

    for category in account['item_details']:
        if not categories.find_one({'name': category}):
            categories.insert_one({
                'name': category
            })

        for item in account['item_details'][category]:
            if not sub_categories.find_one({'name': item['sub_category'], 'category': category}):
                sub_categories.insert_one({
                    'name': item['sub_category'],
                    'category': item['category']
                })

            if not items.find_one({'id': item['id'], 'user_id': account['user_id']}):
                items.insert_one({
                    'id': item['id'],
                    'user_id': account['user_id'],
                    'price': item['price'],
                    'name': item['name'],
                    'category': item['category'],
                    'thumbnail_url': item['thumbnail_url'],
                    'currency': item['currency'],
                    'mock_id': item['mock_id'],
                    'hidden': item['hidden'],
                    'brand_id': item['brand_id'],
                    'buildable': item['buildable'],
                    'bundle_name': item['bundle_name'],
                    'new': item['new'],
                    'release_date': item['release_date'],
                    'sub_category': item['sub_category'],
                    'giftable': item['giftable'],
                    'purchasable': item['purchasable'],
                })

