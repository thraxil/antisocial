

def get_feed_guid(feed, url):
    """ get the guid for a feed

    takes a feedparser feed object and the url
    that it was fetched from and tries to
    return the best option to use as a guid.

    in order of preference:
    'guid', 'id', 'link', or the original url
    """
    return feed.get(
        'guid',
        feed.get(
            'id',
            feed.get('link', url)
        )
    )
