from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import time
import based58
import requests
import uuid
import jnsq
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

# MongoDB configuration
from pymongo import MongoClient
client = MongoClient("mongodb+srv://topgtopg:2IGyXuU4lWhgPRfI@cluster0.ukm3j.mongodb.net/?retryWrites=true&w=majority")
db = client['account_selling']

accounts_collection_v2 = db['accounts']
categories_collection_v2 = db['categories']
sub_categories_collection_v2 = db['sub_categories']
items_collection_v2 = db['items']

# Another MongoDB client for the items collection
items_client = MongoClient("mongodb+srv://EMDBUSER:GdtCXD46tdder4@cluster0.wkv7cqk.mongodb.net/?retryWrites=true&w=majority")
items_db = items_client['Site']
items_collection = items_db['items']

# Suppress only the single InsecureRequestWarning from urllib3 needed for unverified HTTPS requests.
urllib3.disable_warnings(InsecureRequestWarning)
jsq = jnsq.PerfMetric()


class APIConfig:
    base_url = "https://api-sni.avkn.co"
    login_url = f"{base_url}/auth/1/auth/1/login"
    profile_url = f"{base_url}/profile/1/profile/1/data"
    items_url = f"{base_url}/items/1/useritem/1/list"


def gen_consents(*, start: int = 0, stop: int = 16):
    consents = {}
    for index in range(start, stop):
        consents[f"age.{index}"] = True
        consents[f"terms.{index}"] = True
        consents[f"consent.{index}"] = True

    return consents


def gen_start_chat():
    curve = ec.SECP256R1()
    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    timestamp = int(time.time()+3).to_bytes(8, byteorder='little', signed=True)
    public_key_bytes += timestamp
    token = based58.b58encode(public_key_bytes, based58.Alphabet(
        b"MfoqFNBUnJ4l7DWedPvLs-YtVz8wK15rZc90Rm3EbiCSjhaApkxOHIy2XQ"))
    return str(token.decode())
# token1 = "eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.JDi405GJpVRouiqfD8EdqeZ05vEodILsQPXZJubytxa2a5kspbhx1l0OjFpRRolqGMrQHC-zUh5Mtsil2sf34ASIzwmnnPWBYlhymXvE3eNSzSyiduWqBpr1TCnG7hWNZSqI2HYFn1JAhl_Ifb8FSFKhz3mCXJVICmKH2zVlUa5gQlY0qBaR5fOTUkbmctwf1hNilzd1MQfTgYYf5RCJZV6qIjqGF_gYucHcpQpRN4rTRs2YjUo1fkII1UHZKZjLpBYkL9lCUltW-rD5RtYFDZAtZgK6MCd5p-9hLQNmZbNgET30zJQXtOl0z4uopDMbLE8XCfrI5ahbU5mcO0Yt5g.Z3MwaMhS3ZTVbon-wjS8XQ.15ElEjrIuMhgvmasq-6OIR6ty-TQMm3IUJhXr_BPIJnXZIxD7H3qyZ3LeiCCVrBR1CfGbRtqnW6A9TqjCQuWd4tOHZ3SLzdOkFTbKQj34wYWuApZfUDECCuzaKuHvbMZoijCm80iYLO73w4GobH1kUdDtMB19QVDiS4ussPwMbY.19jcsrBIBSKVAKkfDH-s4rCBoQ4g-zz9Q4MZjlIG6jY"
# token1 = "eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.uduv6U1qQi-bnGAp2InWJlDlDb9PoNgV9ynmgEHTZdb0h5mlul0FmMspdlskZROqMiGJLIAP-0beVh5GVpZDHYXbXrNOD-oM8tSakDEfU0ACdDBv2D8RhI7L-NRDxb4g1xSOgTM-qaU920-Wf93N46ACEZRr9mNdh_a7Lta3B3oAZ6PX6h_htgIBNF1QiGITiOBClF2oj-1l5khSzYimYV7JlhOsP0vwqb-Dg-L42RvuFnRdezc5-QfBB14kPfPgVRppIttm5os2ITVP72AadFu5i5TumCo8KGDS5_7emGqvgEJyzD6LJiGptM9TW6hEcqQour2Zgw6Zj0STtHyv3g.Ek4nTTBNxMcGKMLaLbSdSQ.wrz6GibecuPv7c1I4SL2wI6hxZTChNjXJ8U2Gr6MLnrAEYA-_K-DDlQQW-YF8grCj4KXJtn_z5JQVQhuzBeDAZjtxPrbdogU8ehTuEDII_tTlY5AsFJR3-M5QyrAHoDzUHt3ePT6Vraf1peXbCS9giK9aBfPkjcA9pb2mKMiEMU.2X6RK0I1wmnI7-tNSbqcc46Q3vt7ym8qEUY5oEG2NHc"
token1 = "eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.ZmhnMfaj8R6lPk3kpIXz7Lo1XCW_d907GJY6tA2uZfo_Nv8BSN8gmn_UbiEddASm00j2W-kULVR59bdp0EX60vWxFMiFrOpxKphWYWvwf4zVP4Tk4yDYExsxgpOQju2ek0FyeQBdE_5s-_gTPVHThLtZ6veLNI7yV5OrZfK1NMdybx5DY8TdXHstAuIPrvR2yO9Zl3TehdEDchZkyX-oseVtCWg0jz50D7zMPxzNiWpQ8g1QQLN3vz4CeoXZ-1MTRMP5ZmaaP_LS0eirufdzKEuy4oDJsYMGMdGGX8b_ApIrv_Vio4yvG1xX3MLgqKX6Ql-1rmv7PXQ1KwCdIrrlAw.lk5Bv7XK-Iq8IErMXQHx6w.Wk4VAd0RXHcA_JFnW7b1YWENQinPFWDM8fScSUfzCyrQymLdAv-6MwJLZNR-JixpMWKjpbqiv97lshd1uvHNRyVRV9j9ChJHHy1gAvSu8AfeQ6DAVy2r9qvV1W8i5-VQPna3bLr_j8OvbBe4elECQNH_dInRETAd_445trBw_94.zqqJjjdiMhljx6bczMykOWG-iee02hrksxWmsa_hBvk"
# token1 = "eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.SSye9hNNQWQj1zjH-13rA7_9npGxIMz8Gu4MvKGZANZ8ATIJnsNFhJbNfus8T3nuPtHnOqOiMrsA9wNht4z4shcmK16EnRHtyQhJ2pwhQOV9Rpo6IzMAfWCUrk-K58motWdedriJet7Gnh1bXM_gqYpX2jDyxfMAHOARa_baa87ivdMWh1UTPsXVW-aJYWAgm3seAluMqyuKxqLlkSG78S2ly_yAL3n6Kc31Epa9h8zvQRw6W-Kr24j-0omwcOMufWTir9cQpzM8sfQJ9TEy-JCDTvDanuVbIB6t0IDQqJFxacWmLVkS7xLjm-0GF_qYHBsEef5RVMFK4xQgxLjKDQ.LW7AQQ_Uo8IDiUHs7ofEvg.hkfquidd4kmcAH3GRFT_3_6ivwWBhVOaU_KIHy5E0qDYsdmC06ZCGZbiNgnBrgkaqtfWhFjpoTavt1yhzZhSavHpizKNgsxpH1NFzpIZVVItmmuMHO8MW6k4fR0DRFRT9IX2OystihGq0uILU2BgbqmawgnwwMIxyvwycp8S3wg.lHP4WoTL3YTaLksgMFxFhKevjmxV-tGr-x03Q2YKSMQ"
# token1 ="eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.PgAD18JLum-EnsW_i1BbQNAN9VrFA_oPQYgevI1vl_yzdTu5Naac_leF8mKzd-AZVgJ7uU5x_JKcx-V88KurWCThaKr5qGszjkoYemjJTGyYaAUVkKh8_T0mse7CBNLVORgv4NfP-YkKyd_Q9qJWMjMJc44xKLckYOWT9jc26ZIggNyPYYpy24HO869NpOVszNmIpLyR-aZGp4HeDOhzl3Q5su84RbhbU1l3T9OFssis1D7V4yfCNqkgvU8imp-Yxn8RFbxy2Tx_e8ApkO44GJLjNDsnVb2I6NFfjdrMu2hC-gMoId0Zvw2ERdHikV1D1lyrn776lLlbI2-OooKyhA.vhs7AXIHUkf27Ji0I1VVow.H2lQDgtE6ifTKNdPsqt1KP7QLJ2X5b1UK2CxPyVdjb1FuS5-8Ofe6HWqTpaJqok6RjzL6znKLFl0YQrzoNLIQjRODLX9knmsEItj5J6VIpZx0KEf21joaLIu9K1W14NlrEHCtAXmhZqSK_TklSFBS9hoWqPL6UVACBOTCTPWym0.fDJd5LSmuEd1BAQzByaZY04Lw9S8QFNePUb-Oej-S8I"


def login():
    data = {
        "type": "token",
        "request": {
            "token": token1
        }
    }
    headers = {
        "content-type": "application/json; charset=utf-8",
        "x-avkn-apiversion": "15",
        "x-avkn-clientos": "GooglePlay",
        "x-avkn-clientplatform": "GooglePlay",
        "x-avkn-clientversion": "1.091.01",
        "x-avkn-gamesessionid": "0",
        "x-avkn-start-chat": jsq.gen_start_chat(),
        "user-agent": "BestHTTP/2 v2.8.2"
    }
    r = requests.post(
        "https://api.avkn.co/auth/1/auth/1/login",
        json=data,
        headers=headers,
        verify=False,
        allow_redirects=True,
    )
    print(r.content)
    print("Login: - ", r.status_code, r.headers)
    return r


def profile(jtag, login_response):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'BestHTTP/2 v2.8.2',
        'X-Avkn-ApiVersion': '15',
        'X-Avkn-ClientOS': 'GooglePlay',
        'X-Avkn-ClientPlatform': 'GooglePlay',
        "x-avkn-clientversion": "1.091.01",
        "x-avkn-gamesessionid": "0",
        'X-Avkn-Journey-Seq': jtag,
        'X-Avkn-JWTSession': login_response.headers['X-Avkn-JWTSession'],
        'X-Avkn-Session': login_response.headers['X-Avkn-Session']
    }
    payload = {
        "widgets": {
            "main": {
                "profile": None,
                "xp": None,
                "item_stats": None
            }
        }
    }
    response = requests.post(APIConfig.profile_url, json=payload, headers=headers, verify=False)
    response_json = response.json()
    beautified_json = json.dumps(response_json, indent=4)
    print(beautified_json)

    # Extract profile data
    profile_data = response_json['data']['main']['profile']['result']
    xp_data = response_json['data']['main']['xp']['result']['lkwd']['avakinlife']
    item_stats = response_json['data']['main']['item_stats']['result']

    # Determine gender based on the number of female and male clothes owned
    female_clothes = item_stats['owned_female_clothes']
    male_clothes = item_stats['owned_male_clothes']
    account_gender = "female" if female_clothes > male_clothes else "male"

    # Extract additional profile details
    account_level = xp_data['level']

    # Prepare profile information
    profile_info = {
        'gender': account_gender,
        'level': account_level
    }

    # Update the user document in MongoDB with the profile data
    user_id = login_response.json()["user_id"]
    user_data = response_json['data']['main']
    user_data['account_gender'] = account_gender  # Add inferred gender to the data

    accounts_collection_v2.update_one({
        "user_id": user_id
    }, {
        "$set": user_data
    }, upsert=True)

    return profile_info


def items(jtag, login_response, profile_info):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'BestHTTP/2 v2.8.2',
        'X-Avkn-ApiVersion': '15',
        'X-Avkn-ClientOS': 'GooglePlay',
        'X-Avkn-ClientPlatform': 'GooglePlay',
        "x-avkn-clientversion": "1.091.01",
        "x-avkn-gamesessionid": "0",
        'X-Avkn-Journey-Seq': jtag,
        'X-Avkn-JWTSession': login_response.headers['X-Avkn-JWTSession'],
        'X-Avkn-Session': login_response.headers['X-Avkn-Session']
    }
    payload = "null"
    response = requests.post(APIConfig.items_url, data=payload, headers=headers, verify=False)
    response_json = response.json()

    # Extract item IDs from the response
    items = response_json.get('items', [])
    item_ids = [item["unique_id"] for item in items]

    # Fetch full item details from the items collection
    item_details = list(items_collection.find({"id": {"$in": item_ids}}, {"_id": 0}))

    # Categorize items by their category and calculate account worth
    categorized_items = {}
    account_worth = {'Crowns': 0, 'Coins': 0, 'Gems': 0, 'Free': 0}
    currency_counts = {'Crowns': 0, 'Coins': 0, 'Gems': 0, 'Free': 0}
    user_id = login_response.json()["user_id"]

    gender = profile_info.get('gender', 'Unknown')
    level = profile_info.get('level', 'Unknown')
    account_profile_image = f'https://media.avakin.life/thumbnails/{user_id}:profile_headshot:256x256'
    buy_now = 'https://t.me/Doves34'

    title = f"Avakin {gender} Account level {level}"
    accounts_collection_v2.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "title": title,
                "account_profile_image": account_profile_image,
                "buy_now": buy_now
            }
        },
        upsert=True
    )

    for item in item_details:
        category = item.get('category', 'Uncategorized')
        categories_collection_v2.update_one({
            'name': category
        }, {"$set": {'name': category}}, upsert=True)

        sub_categories_collection_v2.update_one({
            'name': item['sub_category'],
            'category': category
        }, {'$set': {'name': item['sub_category'], 'category': category}}, upsert=True)

        item.update({
            'user_id': user_id
        })

        items_collection_v2.update_one({
            'id': item['id'],
            'user_id': user_id
        }, {"$set": item}, upsert=True)

        currency = item.get('currency', 'Free')  # Default to 'Free' if currency is not specified
        price = item.get('price', 0)
        if currency in account_worth:
            account_worth[currency] += price
            currency_counts[currency] += 1

    # Create the account worth structure
    account_worth_summary = {
        'crowns': f"{account_worth['Crowns']} out of {currency_counts['Crowns']} crowns items",
        'coins': f"{account_worth['Coins']} out of {currency_counts['Coins']} coins items",
        'gems': f"{account_worth['Gems']} out of {currency_counts['Gems']} gems items",
        'free': f"{account_worth['Free']} out of {currency_counts['Free']} free items"
    }



    # Update the user document in MongoDB with the categorized item details, account worth, Title, and profile image
    # Generate the Title and account_profile_image


    accounts_collection_v2.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "account_worth": account_worth_summary,
            }
        },
        upsert=True
    )

    # Print the account worth for each currency
    print("Account worth by currency:")
    for currency, summary in account_worth_summary.items():
        print(f"{currency}: {summary}")


def main():
    login_response = login()
    jsq.resolve_shared_key(login_response.headers['x-avkn-chat-tag'])
    jtag = jsq.get_journey_token(int(login_response.json()["user_id"]))

    profile_data = profile(jtag, login_response)  # Get profile data
    items(jtag, login_response, profile_data)  # Pass profile data to items function


main()

