def elkaCRC(data, crc):
    crc_poly = 0x1021
    for _ in range(8):
        if (crc & 0x8000) == 0x8000:
            if (data & 0x80) == 0x80:
                crc = (crc << 1) & 0xFFFF
            else:
                crc = ((crc << 1) & 0xFFFF) ^ crc_poly
        else:
            if (data & 0x80) == 0x80:
                crc = ((crc << 1) & 0xFFFF) ^ crc_poly
            else:
                crc = (crc << 1) & 0xFFFF
        data = (data << 1) & 0xFF
    return crc

def calculate_crc_for_telegram(telegram):
    crc = 0xFFFF
    for byte in telegram:
        crc = elkaCRC(byte, crc)
    upper = (crc >> 8) & 0xFF
    lower = crc & 0xFF
    return upper, lower

def main():
    telegrams = [
        [0x55, 0x02, 0x0C, 0x06],
        [0x55, 0x02, 0x07, 0x00],
        # Add more telegrams as needed
    ]
    
    for i, telegram in enumerate(telegrams):
        upper, lower = calculate_crc_for_telegram(telegram)
        print(f"Telegram {i+1} CRC byte0: {upper}, CRC byte1: {lower}")

if __name__ == "__main__":
    main()
