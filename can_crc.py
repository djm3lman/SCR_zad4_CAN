def calculate_crc(data):
    crc = 0
    for current in data:
        crc ^= current << 7
        for i in range(8):
            crc <<= 1
            if crc & 0x8000:
                crc ^= 0x4599
        crc &= 0x7fff
    return hex(crc)[2:]


def bitStringToByteArray(input):
    byteList = []
    for i in range(len(input) - 1, -1, -8):
        byteString = ""
        for j in range(8):
            index = i - j
            if index >= 0:
                byteString = input[index] + byteString
        if byteString:
            byteList.append(int(byteString, 2))
    byteList.reverse()
    return byteList