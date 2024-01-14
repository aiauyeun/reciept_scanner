import json
import pickle
import requests

# this code reads the image(reciept1.jpg) and generates response1.json which is a dictionary of data that the API read from the picture of the reciept
# url = "https://ocr.asprise.com/api/v1/receipt"
# image = "reciept1.jpg"

# res = requests.post(url,
#                     data = {
#                         'api_key': 'TEST',
#                         'recognizer': 'auto',
#                         'ref_no': 'oct_python_123'
#                     },
#                     files = {
#                         'file': open(image, 'rb')
#                     })

# with open("response1.json", "w") as f:
#     json.dump(json.loads(res.text), f)



#this code opens that json folder and then calculates the discounts on the reciept and then prints out the output.
with open("response1.json", "r") as f:
    data = json.load(f)
print(data['receipts'][0].keys())

items = data['receipts'][0]['items']

print(f"Your purchase at {data['receipts'][0]['merchant_name']}")

descriptions = []
prices = []
current_sum = 0

for i in range(len(items)):
    if(items[i]['amount'] > 0):
        if(i < len(items)):
            descriptions.append(items[i]['description'])
            if(items[i+1]['amount'] < 0):
                # print(f"{items[i]['amount']} plus {items[i+1]['amount']}")
                prices.append(round(items[i]['amount'] + items[i+1]['amount'],2))
            elif(items[i+1]['amount'] > 0):
                prices.append(items[i]['amount'])
        else:
            descriptions.append(items[i]['description'])
            prices.append(items[i]['amount'])

for price, description in zip(prices, descriptions):
    print(f"{description} - ${round(price,2)}")

print(f"Tax: {data['receipts'][0]['tax']}")

print(prices)
print(f"Subtotal: {sum(prices)}")

######OUTPUT######## All correct except for SWISS MISS(the api failed to detect the $-2 discount of the hot chocolate and instead labled it as a $2 item) maybe detect discounts with the /(works on costco only tho...)
    # Your purchase at WHOLESALE South San Francisco #422
    # SELF-CHECKOUT - $33.99
    # 33825 WHOLE FRYERS - $17.34
    # 815544 KS BLUEBERRY - $7.89
    # 26161 LOBSTER TAIL - $114.99
    # 25969 BLACK COD FL - $19.69
    # E20397 NY THIN CUT - $38.76
    # 1032422 PALMOLIVE - $6.59
    # E1242231 SWISS MISS - $7.99
    # E 0000318782/1242231 - $2.0
    # 1292885 CHAMPION 85P - $12.49
    # 1292885 CHAMPTONBB5P - $12.49
    # 1275756 NASSIF MD - $23.99
    # 1275756 ASSIF MD - $23.99
    # 127576 NASSIF MD - $23.99
    # 1275756 NASSIF MD - $0.0
    # 1566355 SEKKISEI - $46.99
    # 1692422 NEXXUS ADV - $19.99
    # Tax: 16.84
    # [33.99, 17.34, 7.89, 114.99, 19.69, 38.76, 6.59, 7.99, 2.0, 12.49, 12.49, 23.99, 23.99, 23.99, 0.0, 46.99, 19.99]
    # Subtotal: 413.17