import argparse

def main1():
    parser = argparse.ArgumentParser()
    parser.add_argument('echo')
    args = parser.parse_args()

    print(args.echo)

if __name__ == '__main__':
    main1()


