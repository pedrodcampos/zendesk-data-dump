from settings import ZENDESK_HC_API_URL, AUTH
from zendesk import ZendeskHC

zendesk_hc = ZendeskHC(ZENDESK_HC_API_URL, AUTH)

articles, users, categories, sections = zendesk_hc.articles(
    include='users,categories,sections')
