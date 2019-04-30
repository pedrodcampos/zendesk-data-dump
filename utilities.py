from helpers import inject, to_csv, flatten_dict


def dump_search(zendesk, query, filename):
    print(f"# Downloading Search results for {query}...")
    search_results, = zendesk.client.search(query)
    print("\tDone.")

    print("# Flattening...")
    data = [flatten_dict(result) for result in search_results]
    print("\tDone.")

    if 'ticket' in query:
        print("# Parsing custom fields...")
        ticket_fields, = zendesk.client.ticket_fields()
        ticket_fields_mapping = {
            ticket_field['id']: ticket_field['title'] for ticket_field in ticket_fields}

        mapped = []
        for item in data:
            mapped_item = {}
            for key, value in item.items():
                if key in ticket_fields_mapping:
                    new_key = f"{ticket_fields_mapping[key]} ({str(key)})"
                    mapped_item.update({new_key: value})
                else:
                    mapped_item.update({key: value})
            mapped.append(mapped_item)
        data = mapped
        print("\tDone.")

    print("# Exporting...")
    file_full_path = to_csv(data, filename or 'search.csv')
    print(f"\tExported to{file_full_path}")
    print("Done.")


def dump_articles(zendesk, filename):
    print("# Downloading Articles, users, categories and sections...")
    articles, users, categories, sections = zendesk.helpcenter.articles(
        include='users,categories,sections')
    print("\tDone.")

    print("# Downloading User segments and permission groups...")
    user_segments, = zendesk.helpcenter.user_segments()
    permission_groups, = zendesk.client.permission_groups()
    print("\tDone.")

    print("# Stitching files...")
    articles = inject(users, 'author_id', articles, 'author')
    articles = inject(permission_groups, 'permission_group_id',
                      articles, 'permission_group')
    articles = inject(sections, 'section_id', articles, 'section')
    articles = inject(user_segments, 'user_segment_id',
                      articles, 'user_segment')
    for article in articles:
        article['section'] = inject(
            categories, 'category_id', article['section'], 'category')
    print("\tDone.")

    print("# Flattening...")
    data = [flatten_dict(article) for article in articles]
    print("\tDone.")

    print("# Exporting...")
    file_full_path = to_csv(data, filename or 'articles.csv')
    print(f"\tExported to{file_full_path}")
    print("Done.")
