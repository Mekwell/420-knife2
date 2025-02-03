from esipy import EsiApp, EsiClient, EsiSecurity
import os

esi_app = EsiApp().get_latest_swagger
esi_security = EsiSecurity(
    redirect_uri=os.environ.get('CALLBACK_URL'),
    client_id=os.environ.get('CLIENT_ID'),
    secret_key=os.environ.get('CLIENT_SECRET')
)
client = EsiClient(security=esi_security, retry_requests=True)

SCOPES = [
    'esi-skills.read_skills.v1',
    'esi-wallet.read_character_wallet.v1',
    'esi-wallet.read_character_wallet_journal.v1',
    'esi-wallet.read_character_wallet_transactions.v1',
    'esi-mail.read_mail.v1',
    'esi-characters.read_contacts.v1',
    'esi-skills.read_skillqueue.v1'
]

def get_esi_data(char_id):
    ops = {
        'skills': esi_app.op['get_characters_character_id_skills'](character_id=char_id),
        'wallet': esi_app.op['get_characters_character_id_wallet'](character_id=char_id),
        'journal': esi_app.op['get_characters_character_id_wallet_journal'](character_id=char_id),
        'transactions': esi_app.op['get_characters_character_id_wallet_transactions'](character_id=char_id),
        'mail': esi_app.op['get_characters_character_id_mail'](character_id=char_id),
        'contacts': esi_app.op['get_characters_character_id_contacts'](character_id=char_id),
        'skillqueue': esi_app.op['get_characters_character_id_skillqueue'](character_id=char_id)
    }
    
    return {key: client.request(op).data for key, op in ops.items()}
