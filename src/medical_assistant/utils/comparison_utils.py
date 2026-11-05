
import re
from typing import Optional, Literal

from pydantic import BaseModel


class TestComparison(BaseModel):
    test_name: str

    previous_value: Optional[float] = None
    current_value: Optional[float] = None

    previous_unit: Optional[str] = None
    current_unit: Optional[str] = None

    difference: Optional[float] = None

    direction: Literal[
        "increased",
        "decreased",
        "unchanged",
        "new_test",
        "missing_in_current",
        "not_comparable"
    ]

    previous_range_status: Optional[str] = None
    current_range_status: Optional[str] = None


class ReportComparison(BaseModel):
    comparisons: list[TestComparison]


def normalize_test_name(name: str) -> str:
    """Normalize test names to make matching easier."""

    name = name.lower().strip()
    name = re.sub(r"\s+", " ", name)

    aliases = {
        "white blood cell count": "wbc",
        "white blood cells": "wbc",
        "total white blood cell count": "wbc",
        "platelet count": "platelets",
        "fasting blood glucose": "fasting glucose",
        "blood glucose fasting": "fasting glucose",
    }

    return aliases.get(name, name)


def normalize_unit(unit: Optional[str]) -> Optional[str]:
    """Normalize unit formatting without converting units."""

    if unit is None:
        return None

    return (
        unit.lower()
        .strip()
        .replace(" ", "")
        .replace("μ", "µ")
    )


def get_range_status(
    value: Optional[float],
    reference_range: Optional[str]
) -> Optional[str]:
    """
    Compare a value against a simple reference range.

    Supports:
        12-16
        12–16
        Below 200
        < 200
        Above 10
        > 10

    Returns None if the range cannot be interpreted.
    """

    if value is None or not reference_range:
        return None

    range_text = reference_range.lower().strip()

    # Below 200 or < 200
    match = re.search(
        r"(?:below|less than|under|<)\s*(\d+(?:\.\d+)?)",
        range_text
    )

    if match:
        upper = float(match.group(1))
        return "within_range" if value < upper else "above_range"

    # Above 10 or > 10
    match = re.search(
        r"(?:above|greater than|over|>)\s*(\d+(?:\.\d+)?)",
        range_text
    )

    if match:
        lower = float(match.group(1))
        return "within_range" if value > lower else "below_range"

    # 12-16 or 12–16
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)",
        range_text
    )

    if match:
        lower = float(match.group(1))
        upper = float(match.group(2))

        if lower > upper:
            return None

        if lower <= value <= upper:
            return "within_range"

        return "below_range" if value < lower else "above_range"

    return None


def build_test_dictionary(tests):
    """
    Convert extracted test list into a dictionary.

    Raises an error if duplicate normalized test names exist,
    rather than silently overwriting measurements.
    """

    result = {}

    for test in tests:
        normalized_name = normalize_test_name(test.test_name)

        if normalized_name in result:
            raise ValueError(
                f"Duplicate test name detected: {test.test_name}"
            )

        result[normalized_name] = test

    return result


def compare_reports(
    data
) -> ReportComparison:
    """
    Compare two MedicalReport Pydantic objects.

    Uses MedicalReport.test_info from your schema.
    """

    previous_report, current_report = data["report_1"], data["report_2"]

    previous_tests = build_test_dictionary(
        previous_report.test_info
    )

    current_tests = build_test_dictionary(
        current_report.test_info
    )

    all_test_names = set(previous_tests) | set(current_tests)

    results = []

    for test_name in sorted(all_test_names):

        old_test = previous_tests.get(test_name)
        new_test = current_tests.get(test_name)

        # Test exists only in current report
        if old_test is None:

            results.append(
                TestComparison(
                    test_name=new_test.test_name,
                    current_value=new_test.value,
                    current_unit=new_test.unit,
                    direction="new_test",
                    current_range_status=get_range_status(
                        new_test.value,
                        new_test.reference_range
                    )
                )
            )

            continue

        # Test exists only in previous report
        if new_test is None:

            results.append(
                TestComparison(
                    test_name=old_test.test_name,
                    previous_value=old_test.value,
                    previous_unit=old_test.unit,
                    direction="missing_in_current",
                    previous_range_status=get_range_status(
                        old_test.value,
                        old_test.reference_range
                    )
                )
            )

            continue

        old_unit = normalize_unit(old_test.unit)
        new_unit = normalize_unit(new_test.unit)

        old_value = old_test.value
        new_value = new_test.value

        old_status = get_range_status(
            old_value,
            old_test.reference_range
        )

        new_status = get_range_status(
            new_value,
            new_test.reference_range
        )

        # Do not compare missing values or incompatible units
        if (
            old_value is None
            or new_value is None
            or old_unit is None
            or new_unit is None
            or old_unit != new_unit
        ):

            results.append(
                TestComparison(
                    test_name=new_test.test_name,
                    previous_value=old_value,
                    current_value=new_value,
                    previous_unit=old_test.unit,
                    current_unit=new_test.unit,
                    direction="not_comparable",
                    previous_range_status=old_status,
                    current_range_status=new_status
                )
            )

            continue

        difference = new_value - old_value

        if difference > 0:
            direction = "increased"
        elif difference < 0:
            direction = "decreased"
        else:
            direction = "unchanged"

        results.append(
            TestComparison(
                test_name=new_test.test_name,
                previous_value=old_value,
                current_value=new_value,
                previous_unit=old_test.unit,
                current_unit=new_test.unit,
                difference=round(difference, 4),
                direction=direction,
                previous_range_status=old_status,
                current_range_status=new_status
            )
        )

    return ReportComparison(comparisons=results)
