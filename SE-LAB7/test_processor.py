from hypothesis import given, strategies as st

from processor import (
    verify_isbn10_format,
    calculate_depreciation_factor,
    lookup_condition_multiplier
)


# Strategies for testing different input types
arbitrary_inputs = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.text(),
    st.lists(st.integers()),
    st.dictionaries(st.text(), st.integers())
)


# --------------------------------------------------
# 1. ISBN-10 FORMAT VALIDATION
# --------------------------------------------------

@given(arbitrary_inputs)
def test_verify_isbn10_format_no_crash(s):
    verify_isbn10_format(s)


@given(
    prefix=st.text(
        alphabet="0123456789",
        min_size=9,
        max_size=9
    ),
    check=st.sampled_from("0123456789X")
)
def test_verify_isbn10_format_valid_input(prefix, check):
    isbn = prefix[:1] + "-" + prefix[1:4] + "-" + prefix[4:] + "-" + check

    expected = (
        f"Group {prefix[1:4]}: "
        f"Starts {prefix[0]}, Checksum {check}"
    )

    assert verify_isbn10_format(isbn) == expected


def test_verify_isbn10_format_invalid_inputs():
    invalid_inputs = [
        None,
        "",
        "123",
        "abcdefghij",
        "123456789YZ"
    ]

    for value in invalid_inputs:
        assert verify_isbn10_format(value) is None


# --------------------------------------------------
# 2. DEPRECIATION FACTOR
# --------------------------------------------------

@given(arbitrary_inputs)
def test_calculate_depreciation_factor_no_crash(s):
    calculate_depreciation_factor(s)


@given(
    age=st.integers(min_value=0, max_value=10000),
    life=st.integers(min_value=1, max_value=10000)
)
def test_calculate_depreciation_factor_valid_input(age, life):
    result = calculate_depreciation_factor(f"{age}/{life}")

    expected = round(max(0.1, 1.0 - (age / life)), 2)

    assert result == expected


def test_calculate_depreciation_factor_invalid_inputs():
    invalid_inputs = [
        None,
        "",
        "/",
        "abc/10",
        "1/0",
        "-1/10",
        "1/-10",
        "nan/10",
        "inf/10",
        "1/inf",
        "1/2/3"
    ]

    for value in invalid_inputs:
        assert calculate_depreciation_factor(value) is None


# --------------------------------------------------
# 3. CONDITION MULTIPLIER
# --------------------------------------------------

@given(arbitrary_inputs)
def test_lookup_condition_multiplier_no_crash(s):
    lookup_condition_multiplier(s)


@given(
    condition=st.sampled_from([
        "MINT",
        "LIKE_NEW",
        "VERY_GOOD",
        "GOOD",
        "POOR"
    ])
)
def test_lookup_condition_multiplier_valid_input(condition):
    expected = {
        "MINT": 1.25,
        "LIKE_NEW": 1.00,
        "VERY_GOOD": 0.80,
        "GOOD": 0.60,
        "POOR": 0.30
    }

    assert lookup_condition_multiplier(condition) == expected[condition]


def test_lookup_condition_multiplier_normalization():
    assert lookup_condition_multiplier("mint") == 1.25
    assert lookup_condition_multiplier("  good  ") == 0.60
    assert lookup_condition_multiplier("Like_New") == 1.00


def test_lookup_condition_multiplier_invalid_inputs():
    invalid_inputs = [
        None,
        "",
        "INVALID",
        "EXCELLENT",
        "BAD"
    ]

    for value in invalid_inputs:
        assert lookup_condition_multiplier(value) is None