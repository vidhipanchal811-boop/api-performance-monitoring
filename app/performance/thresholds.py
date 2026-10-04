DEFAULT_MAX_AVERAGE_RESPONSE_TIME_MS = 500.0
DEFAULT_MIN_SUCCESS_RATE_PERCENT = 95.0


def evaluate_performance(
    average_response_time_ms: float,
    success_rate_percent: float,
    max_average_response_time_ms: float = (
        DEFAULT_MAX_AVERAGE_RESPONSE_TIME_MS
    ),
    min_success_rate_percent: float = (
        DEFAULT_MIN_SUCCESS_RATE_PERCENT
    )
) -> dict:
    response_time_passed = (
        average_response_time_ms
        <= max_average_response_time_ms
    )

    success_rate_passed = (
        success_rate_percent
        >= min_success_rate_percent
    )

    overall_passed = (
        response_time_passed
        and success_rate_passed
    )

    return {
        "passed": overall_passed,
        "response_time_check": {
            "passed": response_time_passed,
            "actual_ms": average_response_time_ms,
            "maximum_allowed_ms": (
                max_average_response_time_ms
            )
        },
        "success_rate_check": {
            "passed": success_rate_passed,
            "actual_percent": success_rate_percent,
            "minimum_required_percent": (
                min_success_rate_percent
            )
        }
    }