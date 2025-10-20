from .classes import Momentum

def get_bulks():
    argument_pairs = [
        (1, 'minutes'),
        (5, 'minutes'),
        (10, 'minutes'),
        (15, 'minutes'),
        (30, 'minutes'),
        (1, 'hours'),
        (4, 'hours'),
        (6, 'hours'),
        (12, 'hours'),
        (1, 'days'),
        (7, 'days'),
    ]

    argument_triple_none = [(time_diff, time_unit, None) for time_diff, time_unit in argument_pairs]
    argument_triple_usdt = [(time_diff, time_unit, 'USDT') for time_diff, time_unit in argument_pairs]
    argument_triple_btc = [(time_diff, time_unit, 'BTC') for time_diff, time_unit in argument_pairs]

    for time_diff, time_unit, symbol_refrence in argument_triple_none:
        m = Momentum(time_diff=time_diff, time_unit=time_unit, symbol_refrence=symbol_refrence)
        m.api__data

    # 각각각 돌려야 할듯... 지금은 하나의 프로세스에서 돌리고 있음
    for time_diff, time_unit, symbol_refrence in argument_triple_usdt:
        m = Momentum(time_diff=time_diff, time_unit=time_unit, symbol_refrence=symbol_refrence)
        m.api__data

    for time_diff, time_unit, symbol_refrence in argument_triple_btc:
        m = Momentum(time_diff=time_diff, time_unit=time_unit, symbol_refrence=symbol_refrence)
        m.api__data

if __name__ == '__main__':
    get_bulks()