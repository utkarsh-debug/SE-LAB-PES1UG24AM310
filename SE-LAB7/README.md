# L6_L7_09 — Bookstore Trade-In

## Lab 7: Fuzz Testing with Hypothesis

---

## 1. Lab Objective

The objective of this lab is to perform property-based fuzz testing using the Python Hypothesis library.

The testing targets three functions in the bookstore trade-in application:

1. `verify_isbn10_format()`
2. `calculate_depreciation_factor()`
3. `lookup_condition_multiplier()`

The goal is to identify unexpected crashes, discover edge cases, improve input validation, and verify that the functions behave correctly for both valid and invalid inputs.

---

## 2. Application Description

The Bookstore Trade-In application contains three functions responsible for processing book information.

| Function | Purpose |
|---|---|
| `verify_isbn10_format()` | Processes and extracts information from an ISBN-10 string. |
| `calculate_depreciation_factor()` | Calculates a book's depreciation factor based on its age and expected lifespan. |
| `lookup_condition_multiplier()` | Returns a multiplier based on the physical condition of a book. |

The original implementation contained insufficient input validation, which could cause runtime exceptions when unexpected inputs were supplied.

---

## 3. Description of the Three Functions

### 3.1 verify_isbn10_format()

This function accepts an ISBN-10 string, removes hyphens and surrounding whitespace, and extracts:

- The first digit.
- The group code.
- The checksum character.

It returns the extracted information in a formatted string.

### 3.2 calculate_depreciation_factor()

This function accepts a string in the format:

`age/lifespan`

It calculates depreciation using:

`Depreciation = 1 - (age / lifespan)`

The result is rounded to two decimal places, with a minimum depreciation factor of 0.1.

### 3.3 lookup_condition_multiplier()

This function accepts a book condition and returns its corresponding multiplier.

| Condition | Multiplier |
|---|---:|
| MINT | 1.25 |
| LIKE_NEW | 1.00 |
| VERY_GOOD | 0.80 |
| GOOD | 0.60 |
| POOR | 0.30 |

---

## 4. Hypothesis Testing Methodology

Hypothesis is a Python library used for property-based testing.

Unlike conventional testing, where test inputs are manually specified, Hypothesis automatically generates inputs from defined strategies.

It also performs shrinking, which attempts to reduce failing inputs to simpler examples that make bugs easier to understand.

The following testing approach was adopted:

1. Generate arbitrary inputs to identify unexpected crashes.
2. Generate valid inputs and verify expected outputs.
3. Test malformed and invalid inputs.
4. Test normalization behaviour, including whitespace and letter casing.
5. Verify mathematical and functional properties.

---

## 5. Hypothesis Strategies Used

The following strategies were used:

| Strategy | Purpose |
|---|---|
| `st.none()` | Generate None values. |
| `st.booleans()` | Generate Boolean values. |
| `st.integers()` | Generate integers. |
| `st.floats()` | Generate floating-point values, including NaN and infinity. |
| `st.text()` | Generate arbitrary strings. |
| `st.lists()` | Generate lists. |
| `st.dictionaries()` | Generate dictionaries. |
| `st.one_of()` | Combine multiple strategies. |
| `st.sampled_from()` | Select values from a predefined collection. |

For valid inputs, additional strategies were used to generate ISBN characters and valid age/lifespan combinations.

---

## 6. Original Failures Discovered

During the initial fuzz-testing phase, all three original functions exhibited unexpected exceptions.

### 6.1 ISBN-10 Function

| Input | Exception | Cause |
|---|---|---|
| `':'` | ValueError | First character could not be converted to an integer. |
| `'0'` | IndexError | String was too short to access index 9. |
| `''` | IndexError | Empty string caused an invalid index access. |
| `None` | AttributeError | `None` does not support the `replace()` method. |

### 6.2 Depreciation Function

| Input | Exception | Cause |
|---|---|---|
| `'/'` | ValueError | Empty age value could not be converted to float. |
| `''` | ValueError | Input did not contain two values separated by `/`. |
| `None` | AttributeError | `None` does not support the `split()` method. |

### 6.3 Condition Multiplier Function

| Input | Exception | Cause |
|---|---|---|
| `''` | KeyError | Empty string was not a valid dictionary key. |
| `None` | AttributeError | `None` does not support the `strip()` method. |

**Total: 9 distinct failure cases identified during initial fuzz testing.**

---

## 7. Bugs Discovered and Fixes Implemented

### 7.1 ISBN-10 Validation

**Problems identified:**
- No check for non-string inputs.
- No validation of string length.
- No validation of the first nine characters.
- Unsafe indexing of the checksum character.

**Fixes implemented:**
- Added type validation.
- Removed hyphens and surrounding whitespace.
- Added length validation.
- Validated the first nine characters as digits.
- Validated the final character as a digit or `X`.
- Invalid inputs return `None`.

### 7.2 Depreciation Calculation

**Problems identified:**
- Invalid string formats caused conversion errors.
- Zero lifespan caused division by zero.
- Negative and non-finite values were not handled.
- Non-string inputs caused attribute errors.

**Fixes implemented:**
- Added input type validation.
- Checked the input format.
- Added controlled float conversion using `try-except`.
- Used `math.isfinite()` to reject NaN and infinity.
- Rejected negative age and non-positive lifespan.
- Preserved the original depreciation calculation and minimum factor of 0.1.
- Invalid inputs return `None`.

### 7.3 Condition Multiplier Lookup

**Problems identified:**
- Non-string inputs caused attribute errors.
- Unsupported conditions caused dictionary lookup errors.

**Fixes implemented:**
- Added input type validation.
- Normalized input using `strip()` and `upper()`.
- Replaced direct dictionary indexing with `multipliers.get()`.
- Invalid conditions return `None`.

---

## 8. Final Test Results

After implementing the fixes, the test suite was expanded to include arbitrary input types, valid inputs, invalid inputs, and normalization tests.

The final test suite contains **10 tests**.

| Test | Result |
|---|---|
| ISBN-10 arbitrary input testing | PASS |
| ISBN-10 valid input testing | PASS |
| ISBN-10 invalid input testing | PASS |
| Depreciation arbitrary input testing | PASS |
| Depreciation valid input testing | PASS |
| Depreciation invalid input testing | PASS |
| Condition multiplier arbitrary input testing | PASS |
| Condition multiplier valid input testing | PASS |
| Condition normalization testing | PASS |
| Condition invalid input testing | PASS |

### Final Execution Summary

Command:

`pytest -v --hypothesis-show-statistics`

Result:

- Tests collected: 10
- Tests passed: 10
- Tests failed: 0
- Execution time: 0.45 seconds

**Final status: 10 PASSED**

---

## 9. Commands Required to Reproduce Results

### Step 1: Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 2: Install dependencies

```bash
pip install pytest hypothesis
```

### Step 3: Run all tests

```bash
pytest -v --hypothesis-show-statistics
```

### Step 4: Run an individual test

```bash
pytest -v --hypothesis-show-statistics test_processor.py::test_verify_isbn10_format_no_crash
```

Other individual tests can be executed by replacing the test function name.

---

## 10. Project Structure

```text
SE-LAB7/
│
├── .gitignore
├── README.md
├── processor.py
├── processor_original.py
├── test_processor.py
└── .venv/
```

The `.venv/` directory is excluded from version control through `.gitignore`.

---

## 11. Conclusion

This lab demonstrated the use of property-based fuzz testing with Hypothesis to identify unexpected failures in Python functions.

The initial testing phase exposed nine distinct failure cases across the three bookstore functions.

Defensive input validation and safer lookup and calculation mechanisms were implemented to address these issues.

The expanded test suite subsequently verified arbitrary inputs