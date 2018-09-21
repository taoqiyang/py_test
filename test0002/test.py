import random
import pymysql



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
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd="12345678", db='test')
        with conn.cursor() as cursor:
            for key in result:
                cursor.execute('insert into test(`key`) values(%s)', key)
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()
