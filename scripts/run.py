from config import load_config
from provider import GoogleAdSense  #, Facebook, Yahoo, TamagoRepeat
from report import WriterBuilder


def main():
    config = load_config("config.yaml")
    fetch_and_update_ad_report(config)
    # fetch_and_update_shop_report(config)


def fetch_and_update_ad_report(config):
    providers = [
        GoogleAdSense(config=config['AD']['INPUT']['GOOGLE']),
        # Facebook(config=config['AD']['FACEBOOK']),
        # Yahoo(config=config['AD']['YAHOO']),
    ]

    reports = []
    for provider in providers:
        with provider.fetch() as response:
            reports.append(response.to_dict())

    writer_conf = config['WRITER'][config['AD']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)


def fetch_and_update_shop_report(config):
    shops = [
        # TamagoRepeat(config=config['SHOP']['TAMAGO_REPEAT']),
    ]

    reports = []
    for shop in shops:
        with shop.fetch() as response:
            shops.append(response.to_dict())

    writer_conf = config['WRITER'][config['AD']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)


if __name__ == "__main__":
    main()
