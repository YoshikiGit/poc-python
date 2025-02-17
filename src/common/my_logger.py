import datetime

def my_logger(f):
    def _wrapper(*args, **keywords):
        # 前処理
        print(f'{f.__name__}の実行')
        print(f'開始: {datetime.datetime.now()}')

        # デコレート対象の関数の実行
        v = f(*args, **keywords)

        # 後処理
        print(f'終了: {datetime.datetime.now()}')
        print(f'実行結果: {v}')

        return v
    return _wrapper
