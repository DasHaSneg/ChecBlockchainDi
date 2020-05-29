import json

def get_formatted_award_and_verification_info(diplom_json, ver_responce):
    diplom = json.loads(diplom_json)

    award = {
        'name': diplom['recipientProfile']['name'],
        'title': diplom['badge']['name'],
        'organization': diplom['badge']['issuer']['name'],
        'text': diplom['badge']['description'],
        'issuedOn': diplom['issuedOn'],
        'email': diplom['badge']['issuer']['email'],
        'url': diplom['badge']['issuer']['url'],
        'ver_responce': ver_responce
    }

    return award




