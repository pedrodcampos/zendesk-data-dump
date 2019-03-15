from helpers import inject, to_csv


def dump_articles(zendesk, zendesk_hc):
    articles, users, categories, sections = zendesk_hc.articles(
        include='users,categories,sections')
    user_segments, = zendesk_hc.user_segments()

    permission_groups, = zendesk.permission_groups()

    articles = inject(users, 'author_id', articles, 'author')
    articles = inject(permission_groups, 'permission_group_id',
                      articles, 'permission_group')
    articles = inject(sections, 'section_id', articles, 'section')
    articles = inject(user_segments, 'user_segment_id',
                      articles, 'user_segment')
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
             'section_name':article['section']['name'],
             'draft':article['draft'],
             'url': article['url'],
             'permission_group': article['name'],
             'user_segment_name': article['user_segment']['name'] if article['user_segment'] else None,
             'user_segment_type':article['user_segment']['user_type'] if article['user_segment'] else None
             } for article in articles

            ]
    to_csv(data)
