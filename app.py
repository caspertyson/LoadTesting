import time
import math
import json

import threading

import redis
from flask import Flask

lock = threading.Lock()

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def calculateFactorial(number):
    if(number<1):
        return 0
    i=1
    product = 1
    while(i<=number):
        product = product * i
        i=i+1
    return(product)

@app.route('/delete')
def delete():
    cache.flushdb()
    return 'cache deleted'

@app.route('/factorial/-<int:number>')
def factorialNegative(number):
    return 'Please enter smaller number\n'

@app.route('/factorial/<int:number>')
def factorial(number):
    result = calculateFactorial(number)
    if(result==0):
        return '{}'.format(number) + " is not larger than 0\n"
    else:
        cache.append('myCacheList', '{}!'.format(number) + " = " + "{}\n".format(result))
        return '{}!'.format(number) + " is {}\n".format(result)

@app.route('/calculationsStored')
def returnCalculations():
    list = cache.get("myCacheList")
    if(list is None):
        return "Nothing in Cache"
    return list


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

