import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.performance.tester import run_concurrent_test
from app.performance.thresholds import evaluate_performance


LOAD_LEVELS = [10, 50, 100]
TARGET_URL = "http://127.0.0.1:8000/"


async def run_load_tests() -> None:
    print("\nAPI Performance Load Test")
    print("=" * 50)

    test_results = []

    for number_of_requests in LOAD_LEVELS:
        print(
            f"\nTesting {number_of_requests} concurrent requests..."
        )

        result = await run_concurrent_test(
            TARGET_URL,
            number_of_requests
        )

        evaluation = evaluate_performance(
            average_response_time_ms=result["average_response_time_ms"],
            success_rate_percent=result["success_rate_percent"]
        )

        status = "PASS" if evaluation["passed"] else "FAIL"

        test_results.append({
            "load_level": number_of_requests,
            "status": status
        })

        print(f"Total requests:       {result['total_requests']}")
        print(f"Successful requests:  {result['successful_requests']}")
        print(f"Failed requests:      {result['failed_requests']}")
        print(
            f"Success rate:          "
            f"{result['success_rate_percent']:.2f}%"
        )
        print(
            f"Average response:     "
            f"{result['average_response_time_ms']:.2f} ms"
        )
        print(
            f"P95 response:         "
            f"{result['p95_response_time_ms']:.2f} ms"
        )
        print(
            f"P99 response:         "
            f"{result['p99_response_time_ms']:.2f} ms"
        )
        print(
            f"Requests per second:  "
            f"{result['requests_per_second']:.2f}"
        )
        print(f"Performance status:   {status}")

    overall_passed = all(
        result["status"] == "PASS"
        for result in test_results
    )

    print("\n" + "=" * 50)
    print("Load Test Summary")
    print("=" * 50)

    for result in test_results:
        print(
            f"{result['load_level']} requests:".ljust(20)
            + result["status"]
        )

    print(
        f"\nOverall performance: "
        f"{'PASS' if overall_passed else 'FAIL'}"
    )


if __name__ == "__main__":
    asyncio.run(run_load_tests())