import mock

from core.config import ConfigLoader


class DummySecretManager():
    def get(self, key):
        return '{}:EXPECTED'.format(key)


def test_replace_with_env_var():
    '''
    _replace_strが環境変数で正しく値を変換できること
    '''
    loader = ConfigLoader('')

    with mock.patch('os.environ.get', return_value='EXPECTED'):
        assert loader._replace_str('HOGE') == 'HOGE'
        assert loader._replace_str('{ HOGE }') == '{ HOGE }'
        assert loader._replace_str('%{ HOGE }') == '%{ HOGE }'
        assert loader._replace_str('{{ ENV:HOGE }}') == 'EXPECTED'
        assert loader._replace_str('{{ ENV:HOGE_AND_HOGE }}') == 'EXPECTED'
        assert loader._replace_str('{{ ENV:hoge }}') == 'EXPECTED'


def test_replace_with_secret_var():
    '''
    _replace_strがシークレットで正しく値を変換できること
    '''
    secret_manager = DummySecretManager()
    loader = ConfigLoader('', secret_manager)

    assert loader._replace_str('HOGE') == 'HOGE'
    assert loader._replace_str('{ HOGE }') == '{ HOGE }'
    assert loader._replace_str('%{ HOGE }') == '%{ HOGE }'
    assert loader._replace_str('{{ SECRET:HOGE }}') == 'HOGE:EXPECTED'
    assert loader._replace_str('{{ SECRET:HOGE_AND_HOGE }}') == 'HOGE_AND_HOGE:EXPECTED'
    assert loader._replace_str('{{ SECRET:hoge }}') == 'hoge:EXPECTED'


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
