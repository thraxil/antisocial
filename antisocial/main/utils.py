def get_feed_guid(feed, url):
    """get the guid for a feed

    takes a feedparser feed object and the url
    that it was fetched from and tries to
    return the best option to use as a guid.

    in order of preference:
    'guid', 'id', 'link', or the original url
    """
    return feed.get("guid", feed.get("id", feed.get("link", url)))


def get_entry_guid(entry):
    """get the guid for an entry

    prefer: 'guid', 'id', 'link'

    if it can't find any of those, None
    """
    return entry.get("guid", entry.get("id", entry.get("link", None)))
