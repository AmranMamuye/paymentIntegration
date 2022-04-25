import requests

payload = {
    'sender_card': 4242424242424242,
    'sender_cvv': 630,
    'sender_zip': 85286,
    'sender_email': 'bobbydodd@gmail.com',
    'sender_exp': [8, 23],
    'amount': 150,
    'receiver_card': 5555555555554444,
    'receiver_cvv': 630,
    'receiver_zip': 85286,
    'receiver_email': 'sachk@gmail.com',
    'receiver_exp': [8, 23],
}
print(requests.get('http://127.0.0.1:8080/execute_payment', json=payload).json())