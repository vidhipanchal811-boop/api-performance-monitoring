performance_history = []


def add_performance_report(report: dict) -> None:
    performance_history.append(report)


def get_performance_history() -> list:
    return performance_history


def clear_performance_history() -> None:
    performance_history.clear()