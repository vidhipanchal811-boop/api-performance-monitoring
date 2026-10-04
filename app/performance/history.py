performance_history = []


def add_performance_report(report: dict) -> None:
    performance_history.append(report)


def get_performance_history() -> list:
    return performance_history


def clear_performance_history() -> None:
    performance_history.clear()


def get_performance_summary() -> dict:
    if not performance_history:
        return {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "average_response_time_ms": 0.0,
            "average_success_rate_percent": 0.0,
            "latest_status": None
        }

    reports = [item["report"] for item in performance_history]

    passed_tests = sum(
        1 for report in reports
        if report["performance_status"] == "PASS"
    )

    failed_tests = len(reports) - passed_tests

    average_response_time = sum(
        report["average_response_time_ms"]
        for report in reports
    ) / len(reports)

    average_success_rate = sum(
        report["success_rate_percent"]
        for report in reports
    ) / len(reports)

    return {
        "total_tests": len(reports),
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "average_response_time_ms": round(average_response_time, 2),
        "average_success_rate_percent": round(average_success_rate, 2),
        "latest_status": reports[-1]["performance_status"]
    }