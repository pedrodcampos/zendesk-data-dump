from settings import ZENDESK_HC_API_URL, AUTH
from zendesk import ZendeskHC

zendesk_hc = ZendeskHC(ZENDESK_HC_API_URL, AUTH)

articles = zendesk_hc.articles()

print(len(articles))
