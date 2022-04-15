# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, request
from payment import *

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World this is the Stripe app!'

@app.route('/generate_card_token', methods=['GET'])
def generate_card_token_flask():
    id_token = request.args.get('id')
    cardnum = request.args.get('cardnumber')
    expmonth = request.args.get('expmonth')
    expyear = request.args.get('cvv')

    return generate_card_token(id_token, cardnum, expmonth, expyear)

@app.route('/create_payment_charge', methods=['GET'])
def create_payment_charge_flask():
    chargeId = request.args.get('chargeId')
    amount = request.args.get('amount')
    cardId = request.args.get('cardId')

    return create_payment_charge(chargeId, amount, cardId)

@app.route('/get_payment_charge', methods=['GET'])
def get_payment_charge_flask():
    chargeId = request.args.get('chargeId')
    amount = request.args.get('amount')

    return get_payment_charge(chargeId, amount)

@app.route('/getBalance', methods=['GET'])
def getBalance_flask():
    return getBalance()

@app.route('/balanceTransaction', methods=['GET'])
def balanceTransaction_flask():
    balanceId = request.args.get('balanceId')

    return balanceTransaction(balanceId)

@app.route('/allTransaction', methods=['GET'])
def allTransaction_flask():
    return allTransaction()

@app.route('/create_payout', methods=['GET'])
def create_payout_flask():
    payoutId = request.args.get('payoutId')
    amount = request.args.get('amount')
    cardId = request.args.get('cardId')

    return create_payout(payoutId,amount,cardId)

@app.route('/get_payout_amount', methods=['GET'])
def get_payout_amount_flask():
    payoutid = request.args.get('payoutid')

    return get_payout_amount(payoutid)

@app.route('/allPayout', methods=['GET'])
def allPayout_flask():
    return allPayout()

@app.route('/cancel_payout', methods=['GET'])
def cancel_payout_flask():
    payoutid = request.args.get('payoutid')

    return cancel_payout(payoutid)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
