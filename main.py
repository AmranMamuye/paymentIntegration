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
from flask import Flask, request, jsonify, abort
from payment import *
from ml import connections

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

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route('/execute_payment', methods=['GET'])
def execute_payment():
    content = request.json
    content_keys = set(content.keys())
    sender_keys = set(['sender_card', 'sender_cvv', 'sender_zip', 'sender_exp', 'sender_email'])
    receiver_keys = set(['receiver_card', 'receiver_cvv', 'receiver_zip', 'receiver_exp', 'receiver_email'])
    missing_sender_keys = sender_keys - content_keys.intersection(sender_keys)
    missing_receiver_keys = receiver_keys - content_keys.intersection(receiver_keys)
    if len(missing_sender_keys) > 0 and len(missing_receiver_keys) > 0:
        abort(404, description=f'missing following sender keys: {missing_sender_keys} and receiver keys: {receiver_keys}')
    elif len(missing_sender_keys) > 0:
        abort(404, description=f'missing following sender keys: {missing_sender_keys}')
    elif len(missing_receiver_keys) > 0:
        abort(404, description=f'missing following receiver keys: {missing_receiver_keys}')
    else:
        pass

    if 'amount' not in content:
        abort(404, description=f'missing amount key in payload')
    
    sender_customer = stripe.Customer.list(email=content['sender_email'])['data']
    if len(sender_customer) == 0:
        sender = stripe.Customer.create(
          email=content['sender_email'],
        )
        sender_payment = stripe.PaymentMethod.create(
          type="card",
          card={
            "number": str(content['sender_card']),
            "exp_month": content['sender_exp'][0],
            "exp_year": content['sender_exp'][1],
            "cvc": content['sender_cvv'],
          },
        )
        stripe.PaymentMethod.attach(
          sender_payment.id,
          customer=sender.id,
        )
        stripe.Customer.modify(
          sender.id,
          invoice_settings={"default_payment_method": sender_payment.id},
        )
        sender_customer_id = sender.id
    else:
        sender_customer_id = sender_customer[0]['id']

    receiver_customer = stripe.Customer.list(email=content['receiver_email'])['data']
    if len(receiver_customer) == 0:
        receiver = stripe.Customer.create(
          email=content['receiver_email'],
        )
        receiver_payment = stripe.PaymentMethod.create(
          type="card",
          card={
            "number": str(content['receiver_card']),
            "exp_month": content['receiver_exp'][0],
            "exp_year": content['receiver_exp'][1],
            "cvc": content['receiver_cvv'],
          },
        )
        stripe.PaymentMethod.attach(
          receiver_payment.id,
          customer=receiver.id,
        )
        stripe.Customer.modify(
          receiver.id,
          invoice_settings={"default_payment_method": receiver_payment.id},
        )
        receiver_customer_id = receiver.id
    else:
        receiver_customer_id = receiver_customer[0]['id']

    out = stripe.PaymentIntent.create(
      amount=int(content['amount']),
      currency="usd",
      payment_method_types=["card"],
      confirm=True,
      customer=sender_customer_id,
      payment_method=stripe.Customer.retrieve(sender_customer_id)['invoice_settings']['default_payment_method']
    )

    return jsonify({'payment': 'success'})

@app.route('/connections', methods = ['GET'])
def get_connections():
    interests = request.get_json()["interests"]
    return connections(interests)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
