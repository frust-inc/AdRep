# AdRep

AdRep is repoting tool for Advertisement providers (e.g. Google, Facebook etc).

## Test Status

![](https://github.com/frust-inc/AdRep/workflows/AdRep/badge.svg)

## Supported Providers

- Google
- Facebook (Developing)
- LINE (TBD)
- YAHOO (TBD)
- TikTok (TBD)

## Supported Outputs

- Stdout
- CSV
- Google Spread Sheet

## Setup

Clone this repository.

```
$ git clone git@github.com:frust-inc/AdRep.git
$ cd AdRep
```

Install dependency packages.

```
$ pipenv install
```


Copy `config.yaml` from template.

```
$ cp config.yaml.template config.yaml
```

Configure provider secrets.

```
$ vim config.yaml
```

## Run Script

Run script.

```
$ pipenv shell
$ python scripts/run.py
```

You can specify commandline args.

When you update report between `2020/06/01` and `2020/06/02`

```
$ run.py --start-date 2020/06/01 --end-date 2020/06/02
```

When you update report between 10 days ago and yesterday.

```
$ run.py --start-days-before 10 --end-days-before 1
```

## Run test

Run pytest and lint by flake8.

```
$ pytest --flake8
```

## License

MIT
