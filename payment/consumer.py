import time
from main import redis, Order

key = 'refund_order'
group = 'payment-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exist!')


while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()
                #
                # if order:
                #     print(order)
                #     product.quantity = product.quantity - int(obj['quantity'])
                #     product.save()
                # else:
                #     redis.xadd('refund_order', obj, '*')
    except Exception as e:
        print(str(e))
    time.sleep(1)
