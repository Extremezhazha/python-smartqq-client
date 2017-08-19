def smartqq_hash(uin, ptwebqq):
    n = [0] * 4
    for T in range(len(ptwebqq)):
        n[T % 4] ^= ord(ptwebqq[T])
    u, v = 'ECOK', [0] * 4
    v[0] = ((uin >> 24) & 255) ^ ord(u[0])
    v[1] = ((uin >> 16) & 255) ^ ord(u[1])
    v[2] = ((uin >> 8) & 255) ^ ord(u[2])
    v[3] = ((uin >> 0) & 255) ^ ord(u[3])
    u1 = [0] * 8
    for T in range(8):
        u1[T] = n[T >> 1] if T % 2 == 0 else v[T >> 1]
    n1, v1 = '0123456789ABCDEF', ''
    for aU1 in u1:
        v1 += n1[((aU1 >> 4) & 15)]
        v1 += n1[((aU1 >> 0) & 15)]
    return v1
