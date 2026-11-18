import os
import socket
import time

from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    return JsonResponse(
        {
            "status": "healthy",
        }
    )


@require_GET
def server_info(request):
    return JsonResponse(
        {
            "message": "Scaling Lab",
            "hostname": socket.gethostname(),
            "process_id": os.getpid(),
        }
    )


@require_GET
def light_work(request):
    return JsonResponse(
        {
            "message": "Lightweight request completed",
            "hostname": socket.gethostname(),
            "process_id": os.getpid(),
        }
    )


@require_GET
def cpu_work(request):
    try:
        iterations = int(request.GET.get("iterations", 1_000_000))
    except ValueError:
        return JsonResponse(
            {"error": "iterations must be an integer"},
            status=400,
        )

    if not 1 <= iterations <= 10_000_000:
        return JsonResponse(
            {"error": "iterations must be between 1 and 10000000"},
            status=400,
        )

    start_time = time.perf_counter()

    result = 0

    for i in range(iterations):
        result += (i * i) % 97

    processing_time = time.perf_counter() - start_time

    return JsonResponse(
        {
            "hostname": socket.gethostname(),
            "process_id": os.getpid(),
            "iterations": iterations,
            "processing_time_seconds": round(processing_time, 6),
            "result": result,
        }
    )
