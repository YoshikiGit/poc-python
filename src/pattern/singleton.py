class Singleton(object):
    def __init__(self):
        print("親init")

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

## Singletonを継承
class Myclass(Singleton):
    # コンストラクタ
    def __init__(self, input):
        print("子init")
        super().__init__()
        self.input = input

if __name__ == '__main__':
    one = Myclass(1)
    print("one.input={0}".format(one.input))
    two = Myclass(2)
    print("one.input={0}, two.input={1}".format(one.input, two.input))
    one.input = 0
    print("one.input={0}, two.input={1}".format(one.input, two.input))


class Singleton2():    
    instance = None

    #オブジェクトを作成する前に実行される処理
    def __new__(cls):
        if cls.instance is None:
            #Singletonクラスはobjectクラスを継承しているため、super()はobjectを指す
            cls.instance = super().__new__(cls)
            print("インスタンスを作成")
        return cls.instance

def client():
    resultSingletonA = Singleton()
    resultSingletonB = Singleton()

    if(resultSingletonA is resultSingletonB):
        print("同じインスタンスです")
    else:
        print("同じインスタンスではありません")

if __name__ == "__main__":
    client()