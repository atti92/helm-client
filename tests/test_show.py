import helm


def test_show_all():
    cp = helm.show.all(dry_run=True)
    assert cp.args == ("helm", "show", "all")
