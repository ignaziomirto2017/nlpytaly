import requests
from diskcache import Cache

cache = Cache(".")


@cache.memoize(name="tags")
def request_tags(sentence: str):
    """
    Implement you own request_tags. The expected result is
    a list of tuples. Each of these tuples represents a
    TreeTagger tag, containing its occurrence (t[0]), PoS (t[1])
    and its lemma (t[2]) as recognised by TreeTagger.
    Please see README.md for more information.
    """
    raise NotImplementedError
