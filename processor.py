from helper import translateSide, getLinearPrice
from collections import OrderedDict
from conn_discord import bot, send_message
import asyncio

curr_orders = OrderedDict()
SIZE_LIMIT = 100

def process_orders(orders):
    """
    A function to process the given orders and perform various actions based on the order details.
    """
    # print(len(orders))
    # for order in orders:
    #     print(order)

    createdByTP = list(
        filter(lambda x: x.get("createType") == "CreateByTakeProfit", orders)
    )
    createdBySL = list(
        filter(lambda x: x.get("createType") == "CreateByStopLoss", orders)
    )
    createdByUser = list(
        filter(lambda x: x.get("createType") == "CreateByUser", orders)
    )
    createdByClosing = list(
        filter(lambda x: x.get("createType") == "CreateByClosing", orders)
    )

    checking = {
        "NewLimitOrder": lambda x: (
            x.get("orderType") == "Limit"
            and x.get("createType") == "CreateByUser"
            and x.get("orderStatus") == "New"
        ),
        "CancelledLimitOrder": lambda x: (
            x.get("orderType") == "Limit"
            and x.get("orderStatus") == "Cancelled"
            and x.get("cancelType") == "CancelByUser"
        ),
        "MarketOrder": lambda x: (
            x.get("orderType") == "Market"
            and x.get("createType") == "CreateByUser"
            and x.get("orderStatus") == "Filled"
        ),
        "ClosedOrder": lambda x: (
            x.get("orderType") == "Market"
            and x.get("createType") == "CreateByClosing"
            and x.get("orderStatus") == "Filled"
        ),
        "FilledLimitOrder": lambda x: (
            x.get("orderType") == "Limit"
            and x.get("createType") == "CreateByUser"
            and x.get("orderStatus") == "Filled"
        )
    }

    newLimitOrder = list(filter(checking["NewLimitOrder"], orders))
    cancelledLimitOrder = list(filter(checking["CancelledLimitOrder"], orders))
    marketOrder = list(filter(checking["MarketOrder"], orders))
    closedOrder = list(filter(checking["ClosedOrder"], orders))
    filledLimitOrder = list(filter(checking["FilledLimitOrder"], orders))
    # bitArr = (createdByTP, createdBySL, createdByUser, createdByClosing)
    print("The length of order createdByTP:", len(createdByTP))
    print("The length of order createdBySL:", len(createdBySL))
    print("The length of order createdByUser:", len(createdByUser))
    print("The length of order createdByClosing:", len(createdByClosing))
    
    try:
        if newLimitOrder:
            print("Got New LIMIT Order!!!")
            order = newLimitOrder[0]
            reply_to = None
            if order.get("orderId") in curr_orders:
                reply_to = curr_orders[order.get("orderId")]
            currPrice = getLinearPrice(order.get("symbol"))
            content = "================================\n"
            content += (
                "↓AMEND THIS LIMIT ORDER↓\n--------------------------------\n"
                if order.get("orderId") in curr_orders
                else ""
            )
            content += f'LIMIT {translateSide(order.get("side").lower())} {order.get("symbol")}\n\n'
            content += f'{order.get("price")}\n\n'
            # content += f'{order.get("price")}, {currPrice}\n\n'
            content += f'TP: {order.get("takeProfit")}\n' if order.get("takeProfit") else ""
            content += f'SL: {order.get("stopLoss")}\n' if order.get("stopLoss") else ""
            content += "================================"
            
            # print(content)
            sent = asyncio.run_coroutine_threadsafe(send_message(content, reply_to=reply_to), bot.loop)
            res = sent.result()
            curr_orders[order.get('orderId')] = res
            
            # print("Result:", res)
            # print(curr_orders)

        elif cancelledLimitOrder:
            print("LIMIT Order Cancelled")
            order = cancelledLimitOrder[0]
            reply_to = None
            if order.get("orderId") in curr_orders:
                reply_to = curr_orders[order.get("orderId")]
            currPrice = getLinearPrice(order.get("symbol"))
            content = "================================\n"
            content += "↓CANCEL THIS LIMIT ORDER↓\n--------------------------------\n"
            content += (
                f'LIMIT {translateSide(order.get("side").lower())} {order.get("symbol")}\n\n'
            )
            content += f'{order.get("price")}\n\n'
            # content += f'{order.get("price")}, {currPrice}\n\n'
            content += f'TP: {order.get("takeProfit")}\n' if order.get("takeProfit") else ""
            content += f'SL: {order.get("stopLoss")}\n' if order.get("stopLoss") else ""
            content += "================================"
            # curr_orders[order.get('orderId')] = order
            # print(content)
            asyncio.run_coroutine_threadsafe(send_message(content, reply_to=reply_to), bot.loop)
            # print(curr_orders)
        elif marketOrder:
            print("Market Order Placed")
            order = marketOrder[0]

            tp_order = createdByTP[0] if createdByTP else {}
            sl_order = createdBySL[0] if createdBySL else {}
            currPrice = getLinearPrice(order.get("symbol"))
            content = "================================\n"
            content += (
                f'{translateSide(order.get("side").lower())} {order.get("symbol")}\n\n'
            )
            content += f"{currPrice}\n\n"
            # content += f'{order.get("price")}, {currPrice}\n\n'
            content += f'TP: {tp_order.get("triggerPrice")}\n' if tp_order else ""
            content += f'SL: {sl_order.get("triggerPrice")}\n' if sl_order else ""
            content += "================================"
            # print(content)
            asyncio.run_coroutine_threadsafe(send_message(content), bot.loop)
        elif filledLimitOrder:
            print("LIMIT Order Filled")
            order = filledLimitOrder[0]
            print(filledLimitOrder)
            if order.get("orderId") in curr_orders:
                reply_to = curr_orders[order.get("orderId")]
                content = "LIMIT Order Filled" 
                asyncio.run_coroutine_threadsafe(send_message(content, reply_to=reply_to), bot.loop)
            else:
                tp_order = createdByTP[0] if createdByTP else {}
                sl_order = createdBySL[0] if createdBySL else {}
                currPrice = getLinearPrice(order.get("symbol"))
                content = "↓LIMIT Order Filled↓\n================================\n"
                content += (
                    f'{translateSide(order.get("side").lower())} {order.get("symbol")}\n\n'
                )
                content += f"{currPrice}\n\n"
                content += f'TP: {tp_order.get("triggerPrice")}\n' if tp_order else ""
                content += f'SL: {sl_order.get("triggerPrice")}\n' if sl_order else ""
                content += "================================"
                # print(content)
                asyncio.run_coroutine_threadsafe(send_message(content), bot.loop)
    except Exception as e:
        print(e)

    if curr_orders and len(curr_orders) > SIZE_LIMIT:
            curr_orders.popitem(last=False)
    print("-----------------------------------------------------------------")
