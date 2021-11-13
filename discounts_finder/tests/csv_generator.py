import logging
import os.path
import argparse
from typing import List, Union

import pandas as pd

from discounts_finder.parsers.products_finder.default import DefaultProductsFinder
from discounts_finder.parsers.products_finder.models import WebShopProduct

"""
Script prepared for generating csv results from html samples.
Use carefully - do not overwrite the reference data.
Example usage inside project (from root dir):
python csv_generator.py --input ./samples/x-kom/ --output ./ --prefix page
"""

logging.getLogger().setLevel(logging.DEBUG)


# use for html files
def get_products_from_file(input_path: str) -> List[WebShopProduct]:
    with open(input_path, "r") as file:
        html_content = file.read()
    return DefaultProductsFinder(html_content).get_products()


def save_products_to_csv(
    input_path: Union[str, List[str]], output_dir: str, output_prefix: str = "result"
):
    paths = input_path
    if isinstance(input_path, str):
        paths = [input_path]

    logging.info(f"Running discounts finder...")

    for index, single_path in enumerate(paths):
        logging_title = f"[{index + 1}/{len(paths)}][{single_path}] "
        logging.info(f"{logging_title}Started")

        products = get_products_from_file(single_path)
        logging.info(products[0])
        logging.info(f"{logging_title}Found {len(products)} products")

        df = pd.DataFrame(
            [
                [product.url, product.image_url, product.discount_price, product.price]
                for product in products
            ],
            index=None,
            columns=["url", "image_url", "discount_price", "price"],
        )

        output_path = os.path.join(output_dir, output_prefix + f"_{index}.csv")
        df.to_csv(output_path, index=False, header=True)

        logging.info(f"{logging_title}Saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Directory or single html file")
    parser.add_argument("--output", type=str, help="Result directory")
    parser.add_argument("--prefix", type=str, default="result")
    args = parser.parse_args()

    input_name = args.input
    if os.path.isdir(args.input):
        input_name = [
            os.path.join(args.input, filename) for filename in os.listdir(args.input)
        ]

    path = args.input if not os.path.isdir(args.input) else os.listdir(args.input)
    try:
        save_products_to_csv(input_name, args.output, args.prefix)
    except Exception as e:
        logging.error(e)
