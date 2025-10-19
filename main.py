import csv
from tabulate import tabulate
import argparse


def calculate_average_rating(file_paths):
    input_files = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            input_files.extend(list(reader))

    brand_ratings = {}
    for product in input_files:
        brand = product['brand']
        rating = float(product['rating'])
        brand_ratings.setdefault(brand, [])
        brand_ratings[brand].append(rating)

    finish = {}
    for brand in brand_ratings:
        ratings = brand_ratings[brand]
        average = sum(ratings) / len(ratings)
        finish[brand] = average
    result = sorted(finish.items(), key=lambda item: item[1], reverse=True)

    table_data = []
    for brand, rating in result:
        table_data.append([brand, f"{rating:.2f}"])

    headers = ['Brand', "Average rating"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))



report_generators = {"average-rating": calculate_average_rating}

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True, help='path')
    parser.add_argument('--report', required=True, help='type_report')

    args = parser.parse_args()

    if args.report in report_generators:
        report_generators[args.report](args.files)
    else:
        print('Unknown report')

