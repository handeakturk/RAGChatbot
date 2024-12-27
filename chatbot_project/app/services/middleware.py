import time
from fastapi import Request
from app.configs.logger.logging import logger
from app.configs.logger.logger_utils import add_log, determine_log_level

async def log_requests(request: Request, call_next):
    start_time = time.time()  # Başlangıç zamanını Unix zaman damgası olarak al
    response = await call_next(request)  # İsteği işle
    process_time = time.time() - start_time  # Süreyi hesapla

    # Log kaydını ekle
    try:
        add_log(
            request=f"{request.method} {request.url.path}",
            response=str(response.status_code),
            duration=process_time,
            log_level=determine_log_level(response.status_code)
        )
    except Exception as e:
        logger.error(f"Log kaydedilemedi: {e}")

    return response

