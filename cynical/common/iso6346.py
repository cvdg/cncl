lookup = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 12,
    'c': 13,
    'd': 14,
    'e': 15,
    'f': 16,
    'g': 17,
    'h': 18,
    'i': 19,
    'j': 20,
    'k': 21,
    'l': 23,
    'm': 24,
    'n': 25,
    'o': 26,
    'p': 27,
    'q': 28,
    'r': 29,
    's': 30,
    't': 31,
    'u': 32,
    'v': 34,
    'w': 35,
    'x': 36,
    'y': 37,
    'z': 38,
}


def checksum(name):
    s = 0

    s += lookup[name[0:1]] * 1
    s += lookup[name[1:2]] * 2
    s += lookup[name[2:3]] * 4
    s += lookup[name[3:4]] * 8
    s += lookup[name[4:5]] * 16
    s += lookup[name[5:6]] * 32
    s += lookup[name[6:7]] * 64
    s += lookup[name[7:8]] * 128
    s += lookup[name[8:9]] * 256
    s += lookup[name[9:10]] * 512
    c = s % 11

    if c == 10:
        c = 0

    return c


def is_valid(name):
    valid = False
    c = checksum(name[0:10])

    if c == lookup[name[10:11]]:
        valid = True

    return valid


def create(name):
    s = 0
    s += lookup[name[0:1]] * 1
    s += lookup[name[1:2]] * 2
    s += lookup[name[2:3]] * 4
    s += lookup[name[3:4]] * 8
    s += lookup[name[4:5]] * 16
    s += lookup[name[5:6]] * 32
    s += lookup[name[6:7]] * 64
    s += lookup[name[7:8]] * 128
    s += lookup[name[8:9]] * 256
    s += lookup[name[9:10]] * 512

    c = s % 11

    if c == 10:
        c = 0

    return f'{name}{c}'


if __name__ == '__main__':
    print(create('csqu305438'))
    print(create('asrv000001'))

    print('csqu3054382: ', is_valid('csqu3054382'))
    print('csqu3054383: ', is_valid('csqu3054383'))
    print('csqu3054384: ', is_valid('csqu3054384'))

    print('asrv0000011: ', is_valid('asrv0000011'))
    print('asrv0000012: ', is_valid('asrv0000012'))
    print('asrv0000013: ', is_valid('asrv0000013'))
