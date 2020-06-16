from config import load_config
from provider import TamagoRepeat
from report import WriterBuilder


def main():
    config = load_config("config.yaml")

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
