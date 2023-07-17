from pytest import mark

from .stuffToTest import calculations

@mark.parametrize("x, y, xpected", [
    (1, 2, 3),
    (13, 12, 25),
    (3, 1, 4),
    (5, 2, 7)
])
def test_add(x, y, xpected):
    # print("testing add...")
    assert calculations.add(x ,y) == xpected
