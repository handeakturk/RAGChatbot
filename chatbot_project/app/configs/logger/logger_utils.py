from datetime import datetime
from app.configs.logger.logging import logger
from app.configs.database import Log
from app.configs.database import session
from sqlalchemy.exc import SQLAlchemyError
import logging

# Log seviyelerini eşleyen bir dictionary
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Log ekleme fonksiyonu
def add_log(request: str, response: str, duration: float, log_level: str, query_data: str = None):
    try:
        log_entry = Log(
            request=request,
            response=response,
            duration=duration,
            log_level=log_level,
            created_at=datetime.utcnow(),
            query_data=query_data
        )
        session.add(log_entry)
        session.commit()
        # log_level string'den integer'a dönüştürülüyor
        level = LOG_LEVELS.get(log_level.upper(), logging.INFO)
        logger.log(level, f"Log kaydedildi: {log_entry}")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Log kaydedilemedi: {e}")

def determine_log_level(status_code: int) -> str:
    if 200 <= status_code < 300:
        return "INFO"
    elif 400 <= status_code < 500:
        return "WARNING"
    elif 500 <= status_code:
        return "ERROR"
    return "INFO"
