#!/usr/bin/env python3
import argparse
import sys
from .classes import Momentum

def main():

    # possible argument pairs for (--time_diff, --time_unit):
    # (1, 'minutes'),
    # (5, 'minutes'),
    # (10, 'minutes'),
    # (15, 'minutes'),
    # (30, 'minutes'),
    # (1, 'hours'),
    # (4, 'hours'),
    # (6, 'hours'),
    # (12, 'hours'),
    # (1, 'days'),
    # (7, 'days')
    # possible arguments for (--symbol_refrence):
    # 'None', 'USDT', 'BTC', ...
    
    parser = argparse.ArgumentParser(description='Universal Momentum Calculator')
    
    parser.add_argument('--time_diff', type=int, required=True, help='Time difference')
    parser.add_argument('--time_unit', type=str, required=True, choices=['minutes', 'hours', 'days'], help='Time unit')
    parser.add_argument('--symbol_refrence', type=str, default=None, help='Symbol reference')
    
    args = parser.parse_args()
    
    # Convert 'None' string to actual None
    symbol_refrence = None if args.symbol_refrence == 'None' else args.symbol_refrence
    
    # Create Momentum instance
    m = Momentum(time_diff=args.time_diff, time_unit=args.time_unit, symbol_refrence=symbol_refrence)
    
    # Execute and print result
    print(m.api__data)

if __name__ == '__main__':
    main()
