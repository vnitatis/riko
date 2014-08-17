# pipefetchsitefeed.py
#

# note: this is really a macro module

from pipefeedautodiscovery import pipe_feedautodiscovery
from pipefetch import pipe_fetch
from pipeforever import pipe_forever
from pipe2py import util


def pipe_fetchsitefeed(context=None, _INPUT=None, conf=None, **kwargs):
    """This source fetches and parses the first feed found on one or more sites
       to yield the feed entries.

    Keyword arguments:
    context -- pipeline context
    _INPUT -- not used
    conf:
        URL -- url

    Yields (_OUTPUT):
    feed entries
    """
    forever = pipe_forever()

    urls = conf['URL']
    if not isinstance(urls, list):
        urls = [urls]

    for item in _INPUT:
        for item_url in urls:
            url = util.get_value(item_url, item, **kwargs)

            if not '://' in url:
                url = 'http://' + url

            if context and context.verbose:
                print "pipe_fetchsitefeed loading:", url

            autodsc_conf = {u'URL': {u'type': u'url', u'value': url}}

            for feed in pipe_feedautodiscovery(context, forever, autodsc_conf):
                ftch_conf = {u'URL': {u'type': u'url', u'value': feed['link']}}

                for feed_item in pipe_fetch(context, forever, ftch_conf):
                    yield feed_item

        if item.get('forever'):
            # _INPUT is pipeforever and not a loop,
            # so we just yield our item once
            break
