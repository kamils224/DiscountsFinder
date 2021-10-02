import os
from dataclasses import asdict
from decimal import Decimal
from typing import Tuple, List

import pytest
import pandas as pd

from discounts_finder.parsers.products_finder.default import DefaultProductsFinder
from discounts_finder.parsers.products_finder.models import WebShopProduct

SAMPLES_DIR = "samples"
GROUND_TRUTH_DIR = "ground_truth_data"


def build_testing_paths() -> List[Tuple[str, str]]:
    shop_dirs = [os.path.join(SAMPLES_DIR, shop_directory_name) for shop_directory_name in os.listdir(SAMPLES_DIR)]
    results = []
    for shop_path in shop_dirs:
        for sample in os.listdir(shop_path):
            name, _ = sample.split(".")
            input_path = os.path.join(shop_path, sample)
            ground_truth_path = os.path.join(GROUND_TRUTH_DIR, os.path.basename(shop_path), f"{name}.csv")
            results.append((input_path, ground_truth_path))

    return sorted(results, key=lambda x: x[0])


@pytest.mark.parametrize("input_path, ground_truth_path", build_testing_paths())
def test_products_finder(input_path: str, ground_truth_path: str) -> None:
    with open(input_path, "r") as input_file:
        html_text = input_file.read()
        products_finder = DefaultProductsFinder(html_text)
        products = products_finder.get_products()

    gt_result = pd.read_csv(ground_truth_path).to_dict("records")
    gt_products = [WebShopProduct(
                    url=gt_product["url"],
                    image_url=gt_product["image_url"],
                    price=str(gt_product["price"]),
                    discount_price=str(gt_product["discount_price"])) for gt_product in gt_result]
    
    for p, gt in zip(products, gt_products):
        print(p.price)
        print(gt.price)
        print(p.price == gt.price)


if __name__ == '__main__':
    for input_path, gt_path in build_testing_paths():
        test_products_finder(input_path, gt_path)