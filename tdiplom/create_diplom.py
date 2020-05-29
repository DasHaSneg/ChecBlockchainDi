'''
Creates a certificate template
'''
import uuid


from tdiplom.helper import URN_UUID_PREFIX, encode_image

from cert_schema import OPEN_BADGES_V2_CANONICAL_CONTEXT, BLOCKCERTS_V2_CANONICAL_CONTEXT

OPEN_BADGES_V2_CONTEXT = OPEN_BADGES_V2_CANONICAL_CONTEXT
BLOCKCERTS_V2_CONTEXT = BLOCKCERTS_V2_CANONICAL_CONTEXT


class TemplateJson (object):

    def __index__(self, user_jobtitle, user_name, diplom_description, diplom_name, org_name, org_url, org_email):
        self.user_jobtitle = user_jobtitle
       # self.si_image = si_image
        self.user_name = user_name
        self.diplom_description = diplom_description
        #self.t_image = t_image
        self.diplom_name = diplom_name
       # self.t_id = t_id
        self.org_name = org_name
       # self.iss_image = iss_image
        self.org_url = org_url
        self.org_email = org_email

    def create_diplom_template(self):
        t_uuid = str(uuid.uuid4())
        ss_uuid = str(uuid.uuid4())
        badge = create_diplom_section(t_uuid,self.diplom_name, self.diplom_description, ss_uuid,self.org_name, self.org_url,self.org_email, self.user_jobtitle, self.user_name)
        assertion = create_assertion_section()
        recipient = create_recipient_section()
        recipient_profile = create_recipient_profile_section()

        assertion['recipient'] = recipient
        assertion['recipientProfile'] = recipient_profile
        assertion['badge'] = badge

        return assertion


def create_diplom_section(t_id, t_name, t_description, iss_id, iss_name,iss_url,iss_email, si_jobtitle, si_name):
    badge = {
        'type': 'BadgeClass',
        'id': URN_UUID_PREFIX + t_id,
        'name': t_name,
        'description': t_description,
      #  'image': encode_image(t_image),
        'issuer': {
            'id': URN_UUID_PREFIX + iss_id,
            'type': 'Profile',
            'name': iss_name,
            'url': iss_url,
            'email': iss_email,
           # 'image': encode_image(iss_image),
        }
    }

    badge['criteria'] = {}
    badge['criteria']['narrative'] = 'k1'

    signature_lines = []

    signature_lines.append(
        {
            'type': [
                'SignatureLine',
                'Extension'
            ],
            'jobTitle': si_jobtitle,
            #'image': si_image,
            'name': si_name
        }
    )
    badge['signatureLines'] = signature_lines

    return badge

def create_recipient_section():
    recipient = {
        'type': 'email',
        'identity': '*|EMAIL|*',
        'hashed': True
    }
    return recipient


def create_recipient_profile_section():
    return {
        'type': ['RecipientProfile', 'Extension'],
        'name': '*|NAME|*',
        'publicKey': 'ecdsa-koblitz-pubkey:*|PUBKEY|*'
    }


def create_assertion_section():
    assertion = {
        '@context': [
            OPEN_BADGES_V2_CONTEXT,
            BLOCKCERTS_V2_CONTEXT,
            {
                "displayHtml": {"@id": "schema:description"}
            }
        ],
        'type': 'Assertion',
        'displayHtml': 'no',
        'issuedOn': '*|DATE|*',
        'id': URN_UUID_PREFIX + '*|CERTUID|*'
    }
    return assertion


