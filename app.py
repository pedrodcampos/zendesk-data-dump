from settings import ZENDESK_HC_API_URL, AUTH
from helpers import inject, to_csv
from zendesk import ZendeskHC


zendesk_hc = ZendeskHC(ZENDESK_HC_API_URL, AUTH)


if __name__ == '__main__':
    articles, users, categories, sections = zendesk_hc.articles(
        include='users,categories,sections')

    articles = inject(users, 'author_id', articles, 'author')
    articles = inject(sections, 'section_id', articles, 'section')
    for article in articles:
        article['section'] = inject(
            categories, 'category_id', article['section'], 'category')

    data = [{'id': article['id'],
             'author_name': article['author']['name'],
             'title': article['title'],
             'created_at': article['created_at'],
             'edited_at': article['edited_at'],
             'updated_at': article['updated_at'],
             'category_name': article['section']['category']['name'],
             'section_name':article['section']['name']} for article in articles

            ]
    to_csv(data)
