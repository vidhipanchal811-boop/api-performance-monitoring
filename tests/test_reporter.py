from app.performance.reporter import generate_performance_report


def test_generate_performance_report():
    performance_result = {
        "url": "http://example.com",
        "total_requests": 10,
        "successful_requests": 9,
        "failed_requests": 1,
        "success_rate_percent": 90.0,
        "average_response_time_ms": 25.5,
        "minimum_response_time_ms": 10.2,
        "maximum_response_time_ms": 50.8,
        "p95_response_time_ms": 48.5,
        "p99_response_time_ms": 50.2,
        "requests_per_second": 20.0,
        "total_test_time_seconds": 0.5,
        "results": []
    }

    report = generate_performance_report(
        performance_result
    )

    assert "report" in report

    report_data = report["report"]

    assert report_data["url"] == "http://example.com"
    assert report_data["total_requests"] == 10
    assert report_data["successful_requests"] == 9
    assert report_data["failed_requests"] == 1

    assert report_data["success_rate_percent"] == 90.0

    assert report_data["average_response_time_ms"] == 25.5
    assert report_data["minimum_response_time_ms"] == 10.2
    assert report_data["maximum_response_time_ms"] == 50.8

    assert report_data["p95_response_time_ms"] == 48.5
    assert report_data["p99_response_time_ms"] == 50.2

    assert report_data["requests_per_second"] == 20.0
    assert report_data["total_test_time_seconds"] == 0.5

    assert "generated_at" in report_data
    assert report_data["generated_at"]