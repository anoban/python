def create_crc32_lookuptable() ->  list[int]:
    
    """
    
    """
    
    crc_table: list[int] = list(range(256))
    for i in range(256):
        for _ in range(8):
            if (crc_table[i] & 0x1 ) == 0:
                crc_table[i] >>= 1
            else:
                crc_table[i] = 0xEDB88320 ^ (crc_table[i] >> 1)
    return crc_table
