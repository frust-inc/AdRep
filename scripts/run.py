import datetime
import fire

from config import load_config
from provider import GoogleAds, TamagoRepeat
from writer import WriterBuilder


def main(start_date=datetime.date.today(), end_date=datetime.date.today(),
         start_days_before=0, end_days_before=0):

    if type(start_date) == str:
        start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d")
        end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
    start_date = start_date - datetime.timedelta(days=start_days_before)
    end_date = end_date - datetime.timedelta(days=end_days_before)

    config = load_config("config.yaml")
    while start_date <= end_date:
        print(start_date)
        fetch_and_update_ad_report(config, start_date)
        fetch_and_update_shop_report(config, start_date)
        start_date += datetime.timedelta(days=1)


def fetch_and_update_ad_report(config, target_date):
    providers = [
        GoogleAds(config=config['AD']['INPUT']['GOOGLE']),
        # Facebook(config=config['AD']['FACEBOOK']),
        # Yahoo(config=config['AD']['YAHOO']),
    ]

    reports = []
    for provider in providers:
        with provider.fetch() as response:
            reports += provider.build_reports(response.data, time='9:00')

    writer_conf = config['WRITER'][config['AD']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)


def fetch_and_update_shop_report(config, target_date):
    shops = [
        TamagoRepeat(config=config['SHOP']['INPUT']['TAMAGO_REPEAT']),
    ]

    reports = []
    for shop in shops:
        with shop.fetch() as response:
            reports += shop.build_reports(response.data, time='9:00')

    writer_conf = config['WRITER'][config['SHOP']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)


if __name__ == "__main__":
    """
    run.py --start-date [startdate] --end [enddate]
    e.g. when you update report between 2020/06/01 and 2020/06/02
    $ run.py --start-date 2020/06/01 --end-date 2020/06/02

    run.py --start-days-before [start-days-before] --end-days-before [end-days-before]
    e.g. when you update report between 10 days and yesterday.
    $ run.py --start-days-before 10 --end-days-before 1
    """
    fire.Fire(main)
