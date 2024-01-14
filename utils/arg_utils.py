import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Data cleaning pipeline')

    parser.add_argument(
        '--dir', help='root path to image folder', type=str, required=True
    )

    args = parser.parse_args()

    return args
