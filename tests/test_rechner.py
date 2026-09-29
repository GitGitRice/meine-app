from src.rechner import differenz, summe


def test_summe_ganze_zahlen():
    assert summe(2, 3) == 6

def test_summe_mit_null():
    assert summe(0, 7) == 7

def test_differenz():
    assert differenz(10, 4) == 6
