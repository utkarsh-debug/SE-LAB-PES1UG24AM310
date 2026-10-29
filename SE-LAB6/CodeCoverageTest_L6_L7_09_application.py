import pytest

from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration,
)


def make_batch(
    approved=True,
    format_type="paperback",
    books=None,
    credit=False,
):
    return {
        "intake_approved": approved,
        "format": format_type,
        "payout_in_credit": credit,
        "books": books if books is not None else [],
    }


def make_book(
    condition="good",
    missing_pages=0,
    counterfeit=False,
):
    return {
        "condition": condition,
        "missing_pages": missing_pages,
        "counterfeit": counterfeit,
    }


# Input validation

def test_invalid_batches():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


# Batch approval and formats

def test_unapproved_batch_is_skipped():
    result = process_book_buybacks(
        [make_batch(approved=False, books=[make_book()])],
        5.0,
    )
    assert result == {
        "total_payout": 0.0,
        "status": "ZERO_CREDIT",
    }


def test_all_supported_formats():
    batches = [
        make_batch(format_type="textbook", books=[make_book()]),
        make_batch(format_type="hardcover", books=[make_book()]),
        make_batch(format_type="paperback", books=[make_book()]),
    ]

    result = process_book_buybacks(batches, 5.0)

    assert result["total_payout"] == 63.0
    assert result["status"] == "COMPLETED"


def test_unsupported_format():
    result = process_book_buybacks(
        [make_batch(format_type="magazine", books=[make_book()])],
        5.0,
    )

    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_missing_format_and_books_use_defaults():
    result = process_book_buybacks(
        [{"intake_approved": True}],
        5.0,
    )

    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


# Book conditions

@pytest.mark.parametrize(
    ("condition", "expected"),
    [
        ("mint", 10.0),
        ("good", 8.0),
        ("poor", 3.2),
        ("unknown", 8.0),
    ],
)
def test_book_conditions(condition, expected):
    result = process_book_buybacks(
        [make_batch(books=[make_book(condition=condition)])],
        5.0,
    )

    assert result["total_payout"] == expected
    assert result["status"] == "COMPLETED"


# Missing pages and counterfeit books

def test_book_with_missing_pages_is_rejected():
    result = process_book_buybacks(
        [make_batch(books=[make_book(missing_pages=2)])],
        5.0,
    )

    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_paperback():
    result = process_book_buybacks(
        [
            make_batch(
                books=[make_book(counterfeit=True)],
            )
        ],
        5.0,
    )

    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook_resets_batch_credit():
    books = [
        make_book(),
        make_book(counterfeit=True),
        make_book(),
    ]

    result = process_book_buybacks(
        [make_batch(format_type="textbook", books=books)],
        5.0,
    )

    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_hardcover_does_not_reset_batch_credit():
    books = [
        make_book(),
        make_book(counterfeit=True),
    ]

    result = process_book_buybacks(
        [make_batch(format_type="hardcover", books=books)],
        5.0,
    )

    assert result["total_payout"] == 15.0
    assert result["status"] == "COMPLETED"


# Store credit and final statuses

def test_store_credit_bonus():
    result = process_book_buybacks(
        [make_batch(books=[make_book()], credit=True)],
        5.0,
    )

    assert result["total_payout"] == 13.0
    assert result["status"] == "COMPLETED"


def test_empty_batches():
    result = process_book_buybacks([], 5.0)

    assert result == {
        "total_payout": 0.0,
        "status": "ZERO_CREDIT",
    }


def test_more_than_four_rejected_items_triggers_audit():
    batches = [
        make_batch(
            books=[
                make_book(missing_pages=1),
                make_book(missing_pages=1),
                make_book(missing_pages=1),
            ]
        ),
        make_batch(
            books=[
                make_book(missing_pages=1),
                make_book(missing_pages=1),
            ]
        ),
    ]

    result = process_book_buybacks(batches, 5.0)

    assert result["total_payout"] == 0.0
    assert result["status"] == "AUDIT_REJECTED"


def test_exactly_four_rejections_do_not_trigger_audit():
    batches = [
        make_batch(
            books=[make_book(missing_pages=1) for _ in range(4)]
        ),
        make_batch(books=[make_book()]),
    ]

    result = process_book_buybacks(batches, 5.0)

    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


# Scanner calibration

def test_empty_scanner_matrix():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_with_no_readings():
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"


def test_scanner_with_readings_at_or_below_threshold():
    assert inspect_scanner_calibration([[5, 3, 5]]) == "CALIBRATED"


def test_single_high_scanner_reading():
    assert inspect_scanner_calibration([[6]]) == "CALIBRATED"


def test_consecutive_high_readings_trigger_recalibration():
    assert inspect_scanner_calibration([[6, 7]]) == "RECALIBRATE"


def test_low_reading_resets_misread_streak():
    assert (
        inspect_scanner_calibration([[6, 5, 7, 8]])
        == "RECALIBRATE"
    )


def test_recalibration_in_later_device():
    assert (
        inspect_scanner_calibration([[6], [7, 8]])
        == "RECALIBRATE"
    )
