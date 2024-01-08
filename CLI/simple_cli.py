import argparse

def main():
    parser = argparse.ArgumentParser(description='Simple CLI Tool')
    parser.add_argument('command', choices=['greet', 'calculate'],
                        help='Select command: greet or calculate')
    parser.add_argument('--name', help='Your name')
    parser.add_argument('--numbers', nargs='+', type=int,
                        help='List of numbers for calculation')

    args = parser.parse_args()

    if args.command == 'greet':
        if args.name:
            print(f'Hello, {args.name}!')
        else:
            print('Hello!')

    elif args.command == 'calculate':
        if args.numbers:
            result = sum(args.numbers)
            print(f'Sum of numbers: {result}')
        else:
            print('Please provide numbers to calculate.')

if __name__ == "__main__":
    main()
