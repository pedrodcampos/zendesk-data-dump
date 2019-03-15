from settings import ZENDESK_HELPCENTER_INSTANCE, ZENDESK_INSTANCE, AUTH
from zendesk import ZendeskHC, ZendeskClient
from helpers import to_csv
zendesk = ZendeskClient(ZENDESK_INSTANCE, AUTH)
zendesk_hc = ZendeskHC(ZENDESK_HELPCENTER_INSTANCE, AUTH)

# = zendesk.users()
if __name__ == '__main__':

    results, = zendesk.search('type:user role:admin')
    for result in results:
        result.update({'tags': ", ".join(result['tags'])})
        result.update(
            {'user_fields_agent_legacy': result['user_fields']['agent_legacy']})
        result.update(
            {'user_fields_agent_type': result['user_fields']['agent_type']})
        result.update({'user_fields_xo_id': result['user_fields']['xo_id']})
        result.pop('user_fields')
    to_csv(results, 'admin_search_dump.csv')
