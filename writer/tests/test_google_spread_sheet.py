from writer.google_spread_sheet import GoogleSpreadSheetWriter
from report import AdReport


def test_headers_with_report():
    '''
    _headersメソッドで正しく値が取得できること
    '''
    expected = ['配信日', '集計時間', '媒体', 'インプレッション数', 'クリック数',
                'コンバージョン数', 'クリック率', 'クリック単価', 'インプレッション単価', '消化予算']
    config = get_test_config()
    w = GoogleSpreadSheetWriter(config=config)

    values = w._headers()
    assert values == expected


def test_values_with_report():
    '''
    _valuesメソッドで正しくレポートから値が取得できること
    '''
    expected = [['2020/06/01', '9:00', 'google', 10000, 100, 10, 0.01, 100.0, 1000.0, 10000]]
    report = AdReport(date='2020/06/01', time='9:00', name='google', impression=10000, click=100,
                      conversion=10, used_budget=10000)

    config = get_test_config()
    w = GoogleSpreadSheetWriter(config=config)

    values = w._values([report])
    assert values == expected


def get_test_config():
    return {
        'SA_KEY': "",
        'FIELDNAMES': [
            "date",
            "time",
            "provider",
            "impression",
            "click",
            "conversion",
            "ctr",
            "cpc",
            "cpm",
            "used_budget",
        ],
        'FOLDER_ID': "",
        'SPREADSHEET_NAME': "",
        'SHEET_NAME': "テスト",
        'SHEET_RANGE': "A1:H",
        'HEADERS': {
            "date": "配信日",
            "time": "集計時間",
            "provider": "媒体",
            "impression": "インプレッション数",
            "click": "クリック数",
            "conversion": "コンバージョン数",
            "ctr": "クリック率",
            "cpc": "クリック単価",
            "cpm": "インプレッション単価",
            "used_budget": "消化予算",
        },
    }
