from datetime import datetime

from app.performance.thresholds import evaluate_performance


def generate_performance_report(
    performance_result: dict
) -> dict:
    """
    Convert raw performance-test results into
    a structured performance report.
    """

    threshold_evaluation = evaluate_performance(
        average_response_time_ms=(
            performance_result["average_response_time_ms"]
        ),
        success_rate_percent=(
            performance_result["success_rate_percent"]
        )
    )

    return {
        "report": {
            "generated_at": datetime.now().isoformat(),
            "url": performance_result["url"],
            "total_requests": performance_result["total_requests"],
            "successful_requests": performance_result[
                "successful_requests"
            ],
            "failed_requests": performance_result[
                "failed_requests"
            ],
            "success_rate_percent": performance_result[
                "success_rate_percent"
            ],
            "average_response_time_ms": performance_result[
                "average_response_time_ms"
            ],
            "minimum_response_time_ms": performance_result[
                "minimum_response_time_ms"
            ],
            "maximum_response_time_ms": performance_result[
                "maximum_response_time_ms"
            ],
            "p95_response_time_ms": performance_result[
                "p95_response_time_ms"
            ],
            "p99_response_time_ms": performance_result[
                "p99_response_time_ms"
            ],
            "requests_per_second": performance_result[
                "requests_per_second"
            ],
            "total_test_time_seconds": performance_result[
                "total_test_time_seconds"
            ],
            "threshold_evaluation": threshold_evaluation,
            "performance_status": (
                "PASS"
                if threshold_evaluation["passed"]
                else "FAIL"
            )
        }
    }