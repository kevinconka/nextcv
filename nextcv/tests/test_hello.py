import nextcv


def test_hello():
    msg = nextcv.hello()
    assert isinstance(msg, str)
    assert msg.startswith("Hello")

