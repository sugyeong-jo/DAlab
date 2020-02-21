import argparse
parser = argparse.ArgumentParser()
parser.add_argument('date', type = str)
args = parser.parse_args()

date = args.date
print(date)