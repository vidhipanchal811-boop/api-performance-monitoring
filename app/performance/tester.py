import asyncio
import time

import httpx


def calculate_percentile(
    response_times: list[float],
    percentile: float
) -> float:
    if not response_times:
        return 0

    sorted_times = sorted(response_times)

    index = (percentile / 100) * (len(sorted_times) - 1)

    lower_index = int(index)
    upper_index = min(
        lower_index + 1,
        len(sorted_times) - 1
    )

    fraction = index - lower_index

    percentile_value = (
        sorted_times[lower_index]
        + (
            sorted_times[upper_index]
            - sorted_times[lower_index]
        ) * fraction
    )

    return round(percentile_value, 2)


async def send_request(
    client: httpx.AsyncClient,
    url: str
) -> dict:
    start_time = time.perf_counter()

    try:
        response = await client.get(url)
        elapsed_time = time.perf_counter() - start_time

        return {
            "status_code": response.status_code,
            "response_time_ms": round(
                elapsed_time * 1000,
                2
            ),
            "success": response.is_success
        }

    except httpx.RequestError:
        elapsed_time = time.perf_counter() - start_time

        return {
            "status_code": None,
            "response_time_ms": round(
                elapsed_time * 1000,
                2
            ),
            "success": False
        }


async def run_concurrent_test(
    url: str,
    number_of_requests: int = 10
) -> dict:
    test_start_time = time.perf_counter()

    async with httpx.AsyncClient() as client:
        tasks = [
            send_request(client, url)
            for _ in range(number_of_requests)
        ]

        results = await asyncio.gather(*tasks)

    total_test_time = time.perf_counter() - test_start_time

    successful_requests = sum(
        1 for result in results
        if result["success"]
    )

    response_times = [
        result["response_time_ms"]
        for result in results
    ]

    total_requests = len(results)

    average_response_time = (
        sum(response_times) / total_requests
        if response_times
        else 0
    )

    minimum_response_time = (
        min(response_times)
        if response_times
        else 0
    )

    maximum_response_time = (
        max(response_times)
        if response_times
        else 0
    )

    requests_per_second = (
        total_requests / total_test_time
        if total_test_time > 0
        else 0
    )

    success_rate = (
        (successful_requests / total_requests) * 100
        if total_requests > 0
        else 0
    )

    p95_response_time = calculate_percentile(
        response_times,
        95
    )

    p99_response_time = calculate_percentile(
        response_times,
        99
    )

    return {
        "url": url,
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": total_requests - successful_requests,
        "success_rate_percent": round(
            success_rate,
            2
        ),
        "average_response_time_ms": round(
            average_response_time,
            2
        ),
        "minimum_response_time_ms": round(
            minimum_response_time,
            2
        ),
        "maximum_response_time_ms": round(
            maximum_response_time,
            2
        ),
        "p95_response_time_ms": p95_response_time,
        "p99_response_time_ms": p99_response_time,
        "requests_per_second": round(
            requests_per_second,
            2
        ),
        "total_test_time_seconds": round(
            total_test_time,
            2
        ),
        "results": results
    }


def run_performance_test(
    url: str,
    number_of_requests: int = 10
) -> dict:
    results = []

    test_start_time = time.perf_counter()

    with httpx.Client() as client:
        for _ in range(number_of_requests):
            start_time = time.perf_counter()

            try:
                response = client.get(url)
                elapsed_time = time.perf_counter() - start_time

                results.append(
                    {
                        "status_code": response.status_code,
                        "response_time_ms": round(
                            elapsed_time * 1000,
                            2
                        ),
                        "success": response.is_success
                    }
                )

            except httpx.RequestError:
                elapsed_time = time.perf_counter() - start_time

                results.append(
                    {
                        "status_code": None,
                        "response_time_ms": round(
                            elapsed_time * 1000,
                            2
                        ),
                        "success": False
                    }
                )

    total_test_time = time.perf_counter() - test_start_time

    successful_requests = sum(
        1 for result in results
        if result["success"]
    )

    response_times = [
        result["response_time_ms"]
        for result in results
    ]

    total_requests = len(results)

    average_response_time = (
        sum(response_times) / total_requests
        if response_times
        else 0
    )

    minimum_response_time = (
        min(response_times)
        if response_times
        else 0
    )

    maximum_response_time = (
        max(response_times)
        if response_times
        else 0
    )

    requests_per_second = (
        total_requests / total_test_time
        if total_test_time > 0
        else 0
    )

    success_rate = (
        (successful_requests / total_requests) * 100
        if total_requests > 0
        else 0
    )

    p95_response_time = calculate_percentile(
        response_times,
        95
    )

    p99_response_time = calculate_percentile(
        response_times,
        99
    )

    return {
        "url": url,
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": total_requests - successful_requests,
        "success_rate_percent": round(
            success_rate,
            2
        ),
        "average_response_time_ms": round(
            average_response_time,
            2
        ),
        "minimum_response_time_ms": round(
            minimum_response_time,
            2
        ),
        "maximum_response_time_ms": round(
            maximum_response_time,
            2
        ),
        "p95_response_time_ms": p95_response_time,
        "p99_response_time_ms": p99_response_time,
        "requests_per_second": round(
            requests_per_second,
            2
        ),
        "total_test_time_seconds": round(
            total_test_time,
            2
        ),
        "results": results
    }