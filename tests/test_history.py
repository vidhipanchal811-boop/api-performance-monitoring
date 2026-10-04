from app.performance.history import (
    add_performance_report,
    clear_performance_history,
    get_performance_history,
)


def test_add_performance_report():
    clear_performance_history()

    report = {
        "performance_status": "PASS",
        "average_response_time_ms": 100.0
    }

    add_performance_report(report)

    history = get_performance_history()

    assert len(history) == 1
    assert history[0] == report

    clear_performance_history()


def test_multiple_performance_reports():
    clear_performance_history()

    first_report = {
        "performance_status": "PASS"
    }

    second_report = {
        "performance_status": "FAIL"
    }

    add_performance_report(first_report)
    add_performance_report(second_report)

    history = get_performance_history()

    assert len(history) == 2
    assert history[0] == first_report
    assert history[1] == second_report

    clear_performance_history()


def test_clear_performance_history():
    clear_performance_history()

    report = {
        "performance_status": "PASS"
    }

    add_performance_report(report)

    clear_performance_history()

    history = get_performance_history()

    assert history == []