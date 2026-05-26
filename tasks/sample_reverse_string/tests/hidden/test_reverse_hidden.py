from sample_reverse_string import reverse_string


def test_empty() -> None:
    assert reverse_string("") == ""


def test_non_palindrome() -> None:
    assert reverse_string("agent") == "tnega"
