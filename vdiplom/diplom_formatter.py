import json

def get_formatted_award_and_verification_info(diplom_json, ver_responce, user_id):
    diplom = json.loads(diplom_json)
    issued_on = diplom['issuedOn'][8:10] + "." + diplom['issuedOn'][5:7] + "."+ diplom['issuedOn'][0:4]
    award = {
        'sign_name': diplom['badge']['signatureLines'][0]['name'],
        'sign_job': diplom['badge']['signatureLines'][0]['jobTitle'],
        'logoImg': diplom['badge']['image'],
        'signatureImg':  diplom['badge']['signatureLines'][0]['image'],
        'sealImg': diplom['badge']['issuer']['image'],
        'name': diplom['recipientProfile']['name'],
        'title': diplom['badge']['name'],
        'organization': diplom['badge']['issuer']['name'],
        'text': diplom['badge']['description'],
        'issuedOn': issued_on,
        'email': diplom['badge']['issuer']['email'],
        'url': diplom['badge']['issuer']['url'],
        'ver_responce': ver_responce
    }

    return award




