"""celery tasks"""
import logging

from celery import shared_task

from core.alphavantage_utility import alphavantage_request

logger = logging.getLogger(__name__)


@shared_task
def fetch_price_alphavantage_hourly():
    """
    Periodic task running every hour to fetch data from alphavantage website
    """
    try:
        serializer = alphavantage_request()
        serializer.is_valid()
        serializer.save()
    except UserWarning as exc:
        logger.error(f'During requesting and saving model error occurs: {exc}')
