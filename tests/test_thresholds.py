from app.performance.thresholds import evaluate_performance


def test_performance_passes():
    result = evaluate_performance(
        average_response_time_ms=200.0,
        success_rate_percent=99.0
    )

    assert result["passed"] is True
    assert result["response_time_check"]["passed"] is True
    assert result["success_rate_check"]["passed"] is True


def test_response_time_fails():
    result = evaluate_performance(
        average_response_time_ms=600.0,
        success_rate_percent=99.0
    )

    assert result["passed"] is False
    assert result["response_time_check"]["passed"] is False
    assert result["success_rate_check"]["passed"] is True


def test_success_rate_fails():
    result = evaluate_performance(
        average_response_time_ms=200.0,
        success_rate_percent=90.0
    )

    assert result["passed"] is False
    assert result["response_time_check"]["passed"] is True
    assert result["success_rate_check"]["passed"] is False


def test_both_thresholds_fail():
    result = evaluate_performance(
        average_response_time_ms=600.0,
        success_rate_percent=90.0
    )

    assert result["passed"] is False
    assert result["response_time_check"]["passed"] is False
    assert result["success_rate_check"]["passed"] is False


def test_custom_thresholds():
    result = evaluate_performance(
        average_response_time_ms=700.0,
        success_rate_percent=92.0,
        max_average_response_time_ms=750.0,
        min_success_rate_percent=90.0
    )

    assert result["passed"] is True
    assert result["response_time_check"]["passed"] is True
    assert result["success_rate_check"]["passed"] is True