import requests
from pdiplom.create_unsigned_diploms import create_unsigned_diploms_fromfile
import logging
import hashlib
import base64
import json

val_url = 'localhost'

def connection_on():
    """Pings Google to see if the internet is on. If online, returns true. If offline, returns false."""
    try:
        requests.get('http://google.com')
        return True
    except requests.exceptions.RequestException:
        return False

def connection_rpc_on():
    url = "http://"+ val_url+":26657/status"

    # Example echo method
    payload = {
        "method": "echo",
        "params": ["echome!"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    try:
        response = requests.post(url).json()
    except requests.exceptions.ConnectionError:
        return False
    return True


def hash_byte_array(data):
    hashed = hashlib.sha256(data).hexdigest()
    return hashed

def broadcast_tx(uid, hashed):

    url = "http://"+ val_url+":26657"
    message = uid + '=' + hashed
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    payload = {
        "id": -1,
        "jsonrpc": "2.0",
        "method": "broadcast_tx_sync",
        "params": [base64_message]
    }
    response = requests.post(url, json=payload).json()
    try:
        response["error"]
    except KeyError:
        return response["result"]["hash"], False
    else:
        return response["error"]["data"], True


def sign_diplom(roster, template_file):
    diplom = create_unsigned_diploms_fromfile(roster, template_file)
    message = {}
    for uid in diplom.keys():
        diplom_json = json.dumps(diplom[uid])
        diplom_json_byte = diplom_json.encode()
        hashed = hash_byte_array(diplom_json_byte)
        result, err = broadcast_tx(uid, hashed)
        if err == True:
            message[uid] = result
        else:
            message[uid] = 'Диплом успешно добавлен'
        diplom[uid]['signature'] = {
            "type": ['Proof', 'Extension'],
            "targetHash": hashed,
        }

    return diplom, message
