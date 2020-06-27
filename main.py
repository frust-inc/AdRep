import base64
import datetime
import logging
import pytz

from core.config import load_config
from core.logger import init_logger
from provider import GoogleAds, TamagoRepeat
from writer import WriterBuilder

TODAY = 'TODAY'
YESTERDAY = 'YESTERDAY'
JST = pytz.timezone('Asia/Tokyo')


def run_triggered_from_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    config = load_config("config_gf.yaml")
    init_logger(config["LOGGER"])

    # default today
    target_date = datetime.datetime.now(JST)
    if pubsub_message == YESTERDAY:
        target_date = target_date - datetime.timedelta(days=1)

    logging.info("Fetch and update report ({})".format(target_date.date()))
    fetch_and_update_ad_report(config, target_date.date())
    fetch_and_update_shop_report(config, target_date.date())


def fetch_and_update_ad_report(config, target_date):
    providers = [
        GoogleAds(config=config['AD']['INPUT']['GOOGLE']),
        # Facebook(config=config['AD']['INPUT']['FACEBOOK']),
        # Yahoo(config=config['AD']['YAHOO']),
    ]

    now = datetime.datetime.now(JST)
    reports = []
    for provider in providers:
        with provider.fetch(target_date) as response:
            reports += provider.build_reports(response.data, time=now.strftime("%m/%d %H:%M"))

    writer_conf = config['WRITER'][config['AD']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)


def fetch_and_update_shop_report(config, target_date):
    shops = [
        TamagoRepeat(config=config['SHOP']['INPUT']['TAMAGO_REPEAT']),
    ]

    now = datetime.datetime.now(JST)
    reports = []
    for shop in shops:
        with shop.fetch() as response:
            reports += shop.build_reports(response.data, time=now.strftime("%m/%d %H:%M"))

    writer_conf = config['WRITER'][config['SHOP']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)
