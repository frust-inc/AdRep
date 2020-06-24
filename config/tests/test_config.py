import mock

from config import _replace_with_env_var, _parse_and_replace


def test_replace_with_env_var():
    '''
    _replace_with_env_varが正しく値を変換できること
    '''

    with mock.patch('os.environ.get', return_value='EXPECTED'):
        assert _replace_with_env_var('HOGE') == 'HOGE'
        assert _replace_with_env_var('{ HOGE }') == '{ HOGE }'
        assert _replace_with_env_var('%{ HOGE }') == '%{ HOGE }'
        assert _replace_with_env_var('{{ HOGE }}') == 'EXPECTED'
        assert _replace_with_env_var('{{ HOGE_AND_HOGE }}') == 'EXPECTED'
        assert _replace_with_env_var('{{ hoge }}') == 'EXPECTED'


def test_parse_and_replace():
    '''
    parse_and_replaceで正しく値が変換されること
    '''
    config = {
        'DATA1': [
            {
                'DATA2': {
                    'DATA3': '{{ DATA4 }}',
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
        assert _parse_and_replace(config) == expected

