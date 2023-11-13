# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5

def virginia(var="te amo"):
    assert var == "te amo"
