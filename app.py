from pybit.unified_trading import WebSocket
from time import sleep
from processor import process_orders #, loadOpenedPosition, loadOrders
from conn_discord import bot
import requests
from dotenv import load_dotenv
import os

load_dotenv()

discord_token = os.environ.get('DISCORD_TOKEN')
api_key = os.environ.get('BYBIT_API_TOKEN')
api_secret = os.environ.get('lrSryPniO6HIk3sb6rcf0InCNXOITp7dyqjo')

ws = WebSocket(
    testnet=True,
    channel_type="private",
    api_key=api_key,
    api_secret=api_secret,
)


map_position = {
    'buy': "LONG",
    'sell': "SHORT"
}

# neccessary = (
#     'cancelType', 
#     'symbol', 
#     'side', 
#     'orderType', 
#     'orderStatus',
#     'takeProfit', 
#     'stopLoss', 
#     'price',
#     'createType'
#     )



    # if side.lower() == 'buy':
    #     return "LONG" if not inverse else 'SHORT
    # return 'SHORT' if not inverse else 

# exec_info = (
#     'execPrice',
#     ''
# )
# def handle_execution(message):
#     print("This is execution message")
#     # print(len(message['data']))
#     # print(messages)
#     for msg in message['data']:
#         print(msg)
#         print("========")
#         # print(msg)
#         # # for key in neccessary:
#         # #     value = msg.get(key)
#         # #     print(key)
#         # #     print(f"{key}: {msg.get(key)}")
            
#         # print("========")
#     print("qweqw")
#     print("-----------------------------------------------------------------")



def handle_order(response):
    """ 
    The number of the orders determined the type of order made
    - 1 => LIMIT orders / Market without SL and TP
    - 2 => TP and SL orders
    - 3 => Market orders / Fulfilled LIMIT orders
    """
    # print("This is order message")
    # print(len(response['data']))
    orders = response['data']
    process_orders(orders)
    


# position_key = (
#     'symbol',
#     'side',
#     'entryPrice',
#     'takeProfit',
#     'stopLoss'
# )

# def handle_position(message):
#     response = message
#     print("This is Position message")
#     print(len(response['data']))
#     for msg in response['data']:
#         print(msg)
#         # print("========")

#         # for key in neccessary:
#         #     print(f"{key}: {msg.get(key)}")
#         print("========")
#     print("-----------------------------------------------------------------")





if __name__ == "__main__":
    # ws.execution_stream(callback=handle_execution)
    ws.order_stream(callback=handle_order)
    # ws.position_stream(callback=handle_position)
    bot.run(discord_token)
    # while True:
    #     sleep(1)