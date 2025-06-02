import zmq
import time

#Input: Empty list
#Output: List of coupons
def loadCoupons(coupons):
    file = open("../couponList.txt", "r")
    for i in file.readlines():
        tmp = i.split(", ")
        coupons.append(tmp)
    file.close()

#Input: List of coupons, code used, original price
#Output: Discounted price as string. If code not found, return error
def applyCoupon(coupons, code, original):
    for i in coupons:
        if i[1] == code:
            return str(original - (original * (int(i[2])/100))) #Finds the amount of that percentage, then subtracts that much from the original
    return "Code Not Found"

#Each element of this list: [Name, Code, Percentage discounted]
coupons = []
loadCoupons(coupons)

print("Starting Server. Looking for requests.")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8888")

while True:
    message = socket.recv()
    print(f"Received request from the client: {message.decode()}")
    if len(message) > 0:
        if message == "q":
            break
        #decode is a list: [coupon code, original price]
        decode = message.decode().split(", ")
        response = applyCoupon(coupons, decode[0], float(decode[1]))
        time.sleep(1)
        socket.send_string(response)

context.destroy()