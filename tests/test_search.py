import helm


def test_search_hub():
    assert helm.search.hub(dry_run=True) == []


def test_search_repo():
    assert helm.search.repo(dry_run=True) == []
