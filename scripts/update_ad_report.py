from config import load_config
from provider import GoogleAdSense  #, Facebook, Yahoo, TamagoRepeat
from report import WriterBuilder


def main():
    config = load_config("config.yaml")
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


if __name__ == "__main__":
    main()
