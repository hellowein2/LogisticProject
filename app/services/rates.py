import requests
import redis
from loguru import logger
from app.core.config import settings

CBR_URL = settings.CBR_URL
REDIS_KEY_USD_RUB = "rates:usd_rub"
REDIS_TTL_SECONDS = 60 * 60


class RateFetchError(RuntimeError):
    pass


def get_redis_client() -> redis.Redis:
    return redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def fetch_usd_rub_rate_from_cbr() -> float:
    try:
        logger.info("Fetching USD/RUB rate from CBR")
        resp = requests.get(CBR_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return float(data["Valute"]["USD"]["Value"])
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.error("Failed to fetch USD/RUB rate from CBR", exc_info=True)
        raise RateFetchError() from e


def get_usd_rub_rate_cached(r: redis.Redis) -> float:
    try:
        cached = r.get(REDIS_KEY_USD_RUB)
        if cached:
            logger.debug("USD/RUB rate cache hit")
            return float(cached)

        logger.debug("USD/RUB rate cache miss")
        rate = fetch_usd_rub_rate_from_cbr()
        r.setex(REDIS_KEY_USD_RUB, REDIS_TTL_SECONDS, str(rate))
        return rate

    except redis.RedisError as e:
        logger.error("Redis error while getting USD/RUB rate", exc_info=True)
        raise
