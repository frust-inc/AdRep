from config import load_config
from provider import TamagoRepeat
from writer import WriterBuilder


def main():
    config = load_config("config.yaml")

    shops = [
        # TamagoRepeat(config=config['SHOP']['TAMAGO_REPEAT']),
    ]

    reports = []
    for shop in shops:
        with shop.fetch() as response:
            reports += shop.build_reports(response.data, time='9:00')

    writer_conf = config['WRITER'][config['AD']['OUTPUT']['WRITER']]
    with WriterBuilder(config=writer_conf).build() as writer:
        writer.write(reports)


if __name__ == "__main__":
    main()
