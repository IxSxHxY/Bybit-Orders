import requests
from pybit.unified_trading import HTTP

def getLinearPrice(symbol: str) -> str:
    """
    Retrieves the latest price for a given symbol from the linear market.
    
    Args:
        symbol (str): The symbol for which the price is to be retrieved.

    Returns:
        float: The latest price for the given symbol.
    """
    url = f"https://api-testnet.bybit.com/v5/market/tickers?category=linear&symbol={symbol}"
    payload={}
    headers = {}
    response = requests.get(url, headers=headers, data=payload)
    # print(response.json())
    return response.json()["result"]["list"][0]["lastPrice"]

def translateSide(side: str, inverse: bool = False):
    """
    side:
    - 'Buy' -> True
    - 'Sell' -> False

    1 ^ 1 = 0
    0 ^ 1 = 1
    1 ^ 0 = 1
    0 ^ 0 = 0

    True -> "LONG"
    False -> "SHORT"
    """
    isLong = int(side.lower() in ('buy', 'long')) ^ inverse
    return "LONG" if isLong else 'SHORT'

# def checkOrdersExists(symbol: str):
#     session = HTTP(
#         testnet=True,
#         api_key="AwLxR3J9iRMjweyNMz",
#         api_secret="lrSryPniO6HIk3sb6rcf0InCNXOITp7dyqjo",
#     )
#     print(session.get_positions(
#         category="linear",
#         symbol=symbol
#     ))
    

# def getExecList(orderId: str):
#     url = f"https://api-testnet.bybit.com/contract/v3/private/execution/list?orderId={orderId}"
#     payload={}
#     headers = {}
#     response = requests.request("GET", url, headers=headers, data=payload)
#     # print(response.json())
#     return response.json()["result"]["list"][0]["execPrice"]