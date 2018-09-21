import re
import os.path


def test():
    reg = re.compile('[0-9a-zA-Z]+')
    with open('test.txt', mode='r') as fp:
        text = fp.read()

    result = dict()
    for item in reg.finditer(text):
        key = item[0]
        if key in result:
            result[key] = result[key] + 1
        else:
            result[key] = 1

    print(result)


if __name__ == '__main__':
    test()
