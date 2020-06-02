import json
import requests
from pdiplom.issuer_diplom import hash_byte_array
import base64
from pdiplom.issuer_diplom import val_url

def check_tx(di_id):
    message = di_id
    message_bytes =  message.encode('utf-8')
    mes ='0X' + message_bytes.hex().upper()
    response = requests.get(
        'http://'+val_url+':26657/abci_query?data=' + mes).json()
    try:
        response["error"]
    except KeyError:
        log_response = response["result"]["response"]["log"]
        value_response = response["result"]["response"]["value"]
        value_response = base64.b64decode(value_response).decode('utf-8')
        return log_response, value_response

def verify_diplom(diplom_json):
    diplom = json.loads(diplom_json)
    targetHash = diplom['signature']['targetHash']
    del diplom['signature']
    diplom_no_sign = json.dumps(diplom)
    diplom_no_sign_byte = diplom_no_sign.encode()
    hashed = hash_byte_array(diplom_no_sign_byte)
    di_id = diplom['id']
    di_id = di_id.replace("urn:uuid:", "")
    log_response, value_response = check_tx(di_id)
    if log_response == 'exists':
        message1 = 'exist'
    elif log_response == 'recalled':
        message1 = 'recalled'
    else:
        message1 = 'not exist'
    if hashed == value_response == targetHash:
        message2 = 'same'
    else:
        message2 = 'not same'
    return message1, message2


