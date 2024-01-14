from src.data_cleaning import clean_data
from utils.arg_utils import parse_args

if __name__ == "__main__":
    args = parse_args()
    clean_data(args.dir)
