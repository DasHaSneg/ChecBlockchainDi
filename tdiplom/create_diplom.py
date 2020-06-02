'''
Creates a certificate template
'''
import uuid


from tdiplom.helper import URN_UUID_PREFIX, encode_image

from cert_schema import OPEN_BADGES_V2_CANONICAL_CONTEXT

OPEN_BADGES_V2_CONTEXT = OPEN_BADGES_V2_CANONICAL_CONTEXT



class TemplateJson (object):

    def __index__(self, user_name, user_jobtitle, signature_image,
                  diplom_name, diplom_descr, orgn_name,
                  org_url, org_email, seal_image, logo_image,):
        self.user_name = user_name
        self.user_jobtitle = user_jobtitle
        self.signature_image = signature_image
        self.diplom_name = diplom_name
        self.diplom_descr = diplom_descr
        self.org_name = orgn_name
        self.org_url = org_url
        self.org_email = org_email
        self.logo_image = logo_image
        self.seal_image = seal_image

    def create_diplom_template(self):
        t_uuid = str(uuid.uuid4())
        ss_uuid = str(uuid.uuid4())
        diplom = create_diplom_section(t_uuid,self.diplom_name, self.diplom_descr,
                                       ss_uuid,self.org_name, self.org_url,self.org_email,
                                       self.user_jobtitle, self.user_name, self.seal_image,
                                       self.logo_image, self.signature_image)
        assertion = create_assertion_section()
        recipient = create_recipient_section()
        recipient_profile = create_recipient_profile_section()
        assertion['recipient'] = recipient
        assertion['recipientProfile'] = recipient_profile
        assertion['badge'] = diplom
        return assertion


def create_diplom_section(t_id, t_name, t_description, iss_id, iss_name,iss_url,iss_email, si_jobtitle, si_name, t_image, iss_image, si_image):
    badge = {
        'type': 'BadgeClass',
        'id': URN_UUID_PREFIX + t_id,
        'name': t_name,
        'description': t_description,
        'image': encode_image(t_image),
        'issuer': {
            'id': URN_UUID_PREFIX + iss_id,
            'type': 'Profile',
            'name': iss_name,
            'url': iss_url,
            'email': iss_email,
            'image': encode_image(iss_image),
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
            'image': encode_image(si_image),
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


