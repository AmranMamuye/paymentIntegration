import stripe 


# Stripe needs API  keys to authenticate API requests
# using test API keys


# publishable API key for our account 
# pk_test_51KkdljGLKnmKi3AeFV0V6Aftdrb42SrtIupdU4Dx2epulnohPrZluvTzahmbpWxR9gaf6wYcWU7doZLDKoFIVM1d00jpqe35Ai for later integration 


SECRET_KEY = "sk_test_51KkdljGLKnmKi3AeBxcJfMGVacqKloNbPF95FM6FmcJus15LVrMmkmjo6jf5KArOYbFAmLgfdPdmD6JWlzYm085c00aCAs06Ux"

stripe.api_key=SECRET_KEY

# create a card token from the card info 
def generate_card_token(id,cardnumber,expmonth,expyear,cvv):
    data = stripe.Token.create(
            card={
                "id": str(id),
                "number": str(cardnumber),
                "exp_month": int(expmonth),
                "exp_year": int(expyear),
                "cvc": str(cvv),
            })
    cardId = data['card'['id']]

    return cardId


# create a charge from the generated token 
def create_payment_charge(chargeId,amount,cardId):
    charge = stripe.Charge.create(
            card={ "id": str(cardId),},
            amount=int(amount)*100,        
            currency='usd',
            id=chargeId,
        )
    charged = charge['paid']    # return True if charge was successful 

    return charged

# retrieve a charge 
def get_payment_charge(chargeId):
    charge = stripe.Charge.retrieve(id = chargeId)
    
    return charge["amount"]

# update a charge 
def update_payment_charge(chargeId, amount):
    update = stripe.Charge.modify(
        id = chargeId,
        amount=int(amount)*100,
    )
    
    return update["status"]


# representing our Stripe balance. 
# the Balance object will contain funds that are available to be transferred or paid out
# retrieve balance
def getBalance():
    
    return stripe.Balance.retrieve()


# Balance transactions represent funds moving through our Stripe account
# get a balance transaction 
# balanceId
def balanceTransaction(balanceId):
    transacation = stripe.BalanceTransaction.retrieve(balanceId)
    type = transacation["type"]
    amount = transacation["amount"]
    status = transacation["status"]

    return (type, amount, status)


# list transaction history 
def allTransaction():
    return stripe.BalanceTransaction.list()



# A Payout object is created when you receive funds from Stripe
# or when you initiate a payout to either a card of a connected Stripe account. 
# create a payout 
# destination - card Id payment is sent to 

def create_payout(payoutId,amount,cardId):
    payout = stripe.Payout.create(
                id = payoutId,
                amount=int(amount)*100,        
                currency='usd',
                destination= cardId,
                )
    payout_status = payout['status']    # returns paid, pending, in_transit, canceled or failed

    return payout_status


# retrive a payout
def get_payout_amount(payoutid):
    payout = stripe.Charge.retrieve(id = payoutid)
    return payout["amount"]

# list all payouts

def allPayout():
    return stripe.Payout.list()


# cancel a payout
def cancel_payout(payoutid):
    canceled = stripe.Payout.cancel(payoutid)

    return canceled["status"]

def delete_all_customers():
    for cust in stripe.Customer.list()['data']:
        stripe.Customer.delete(cust['id'])

delete_all_customers()











