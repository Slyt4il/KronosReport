strikers = {
    'akane': 13000,
    'aris': 10015,
    'aru': 10000,
    'atsuko': 10042,
    'cherino': 10017,
    'chise': 13001,
    'eimi': 10001,
    'haruka': 16000,
    'haruna': 10002,
    'haruna_(new_year)': 10057,
    'hibiki_(cheer_squad)': 16010,
    'hoshino': 10005,
    'hoshino_(swimsuit)': 10045,
    'iori': 10006,
    'junko': 13007,
    'junko_(new_year)': 16012,
    'kazusa': 10049,
    'marina': 10037,
    'miyako': 10038,
    'momoi': 13011,
    'neru_(bunny)': 10026,
    'shiroko': 10010,
    'shiroko_(cycling)': 10024,
    'shun': 10011,
    'tsubaki': 13009,
    'tsukuyo': 10040,
    'tsurugi': 10013,
    'wakamo_(swimsuit)': 10043,
    'yuuka': 13010,
    'yuuka_(track)': 10053,
}

specials = {
    'akane_(bunny)': 20019,
    'ako': 20008,
    'ayane_(swimsuit)': 26007,
    'fuuka': 23001,
    'hibiki': 20000,
    'himari': 20020,
    'iroha': 20016,
    'karin': 20001,
    'mashiro': 20003,
    'mashiro_(swimsuit)': 20004,
    'nodoka_(hot_spring)': 20010,
    'serina': 26003,
    'shizuko': 23006,
    'utaha': 23004,
}

def get_keys_strikers():
    return strikers.keys()

def get_keys_specials():
    return specials.keys()

def get_list_all():
    return list(get_keys_strikers()) + list(get_keys_specials())