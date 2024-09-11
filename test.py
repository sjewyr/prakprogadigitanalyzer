from analyzer import (
    Analyzer,
    UNITS,
    DECIMAL,
    DECIUNITS,
    HUNDREDS,
    InvalidReturn,
    ERRORS,
)
import pytest

INV_UNITS = {v: k for k, v in UNITS.items()}
INV_DECIMAL = {v: k for k, v in DECIMAL.items()}
INV_DECIUNITS = {v: k for k, v in DECIUNITS.items()}
INV_HUNDREDS = {v: k for k, v in HUNDREDS.items()}
VALUES = []
# Generate test cases in the form of (input, expected_output)
for i in range(1000):
    res = []
    res.append(INV_HUNDREDS.get(i // 100 * 100))
    dec = i % 100 // 10
    if dec == 1:
        res.append(INV_DECIUNITS.get(dec * 10 + i % 10))
        res = list(filter(lambda x: x is not None, res))
        VALUES.append((" ".join(res), i))
        continue
    else:
        res.append(INV_DECIMAL.get(dec * 10))
    res.append(INV_UNITS.get(i % 10))

    res = list(filter(lambda x: x is not None, res))
    VALUES.append((" ".join(res), i))


@pytest.mark.parametrize(("a, b"), (VALUES))
def test_analyzer(a, b):
    code = a
    analyzer = Analyzer(code)
    result = analyzer.analyze()
    assert result == b


def test_syntax_error():
    code = "one hundred twenty cheto tam"
    analyzer = Analyzer(code)
    result = analyzer.analyze()
    assert isinstance(result, InvalidReturn)
    assert type(result.type) == ERRORS.Syntax.value
    assert result.val == "cheto"


@pytest.mark.parametrize(
    ("a, b"), (["zero two", 1], ["nine eleven", 1], ["one hundred two hundred", 2])
)
def test_semantic_error(a, b):
    code = a
    analyzer = Analyzer(code)
    result = analyzer.analyze()
    assert isinstance(result, InvalidReturn)
    assert type(result.type) == ERRORS.Semantic.value
    assert result.pos == b
