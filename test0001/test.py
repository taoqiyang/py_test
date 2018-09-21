import random

def test():
    l = list()
    for i in range(0, 10):
        l.append(str(i))
    for i in range(ord('a'), ord('z') + 1):
        l.append(chr(i))

    for i in range(ord('A'), ord('Z') + 1):
        l.append(chr(i))

    random.shuffle(l)

    result = list()
    for i in range(100):
        result.append(''.join(random.sample(l, 16)))
    return result

if __name__ == '__main__':
    result = test()
    print(result)