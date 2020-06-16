from config import load_config
from provider import GoogleAdSense
from writer import WriterBuilder


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
            reports += provider.build_reports(response.data, time='9:00')

    writer_conf = config['WRITER'][config['AD']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)


if __name__ == "__main__":
    main()
