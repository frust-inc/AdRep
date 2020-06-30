import mock

from core.config import ConfigLoader


def test_replace_with_env_var():
    '''
    _replace_strが正しく値を変換できること
    '''
    loader = ConfigLoader('')

    with mock.patch('os.environ.get', return_value='EXPECTED'):
        assert loader._replace_str('HOGE') == 'HOGE'
        assert loader._replace_str('{ HOGE }') == '{ HOGE }'
        assert loader._replace_str('%{ HOGE }') == '%{ HOGE }'
        assert loader._replace_str('{{ ENV:HOGE }}') == 'EXPECTED'
        assert loader._replace_str('{{ ENV:HOGE_AND_HOGE }}') == 'EXPECTED'
        assert loader._replace_str('{{ ENV:hoge }}') == 'EXPECTED'


def test_parse_and_replace():
    '''
    parse_and_replaceで正しく値が変換されること
    '''
    loader = ConfigLoader('')
    config = {
        'DATA1': [
            {
                'DATA2': {
                    'DATA3': '{{ ENV:DATA4 }}',
                },
            }
        ]
    }

    expected = {
        'DATA1': [
            {
                'DATA2': {
                    'DATA3': 'EXPECTED',
                },
            }
        ]
    }

    with mock.patch('os.environ.get', return_value='EXPECTED'):
        assert loader._parse_and_replace(config) == expected
