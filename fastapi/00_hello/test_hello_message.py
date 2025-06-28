from .hello_message import addition

def test_addition():
    assert addition(1 , 2) == 3, "3"
    assert addition(4 , 2) == 6, "6"
    assert addition(-4 , -2) == -6 , "-6"
    assert addition(0 , 0) == 0 , "0"