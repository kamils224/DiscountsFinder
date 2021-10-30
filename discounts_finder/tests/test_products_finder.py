import os
from typing import Tuple, List

import pytest
import pandas as pd

from discounts_finder.parsers.products_finder.default import DefaultProductsFinder
from discounts_finder.parsers.products_finder.models import WebShopProduct

SAMPLES_DIR = "samples"
GROUND_TRUTH_DIR = "reference_data"


def _build_testing_paths() -> List[Tuple[str, str]]:
    shop_dirs = [os.path.join(SAMPLES_DIR, shop_directory_name) for shop_directory_name in os.listdir(SAMPLES_DIR)]
    results = []
    for shop_path in shop_dirs:
        for sample in os.listdir(shop_path):
            name, _ = sample.split(".")
            input_name = os.path.join(shop_path, sample)
            ground_truth_path = os.path.join(GROUND_TRUTH_DIR, os.path.basename(shop_path), f"{name}.csv")
            results.append((input_name, ground_truth_path))

    return sorted(results, key=lambda x: x[0])


@pytest.mark.parametrize("input_name, ground_truth_path", _build_testing_paths())
def test_products_finder(input_name: str, ground_truth_path: str) -> None:
    with open(input_name, "r") as input_file:
        html_text = input_file.read()
        products_finder = DefaultProductsFinder(html_text)
        products = products_finder.get_products()

    gt_result = pd.read_csv(ground_truth_path, dtype=str).to_dict("record")
    gt_products = [WebShopProduct(
        url=gt_product["url"],
        image_url=gt_product["image_url"],
        discount_price=gt_product["discount_price"],
        price=gt_product["price"]) for gt_product in gt_result]

    sorted_products = sorted(products, key=lambda prod: prod.url)
    sorted_gt_products = sorted(gt_products, key=lambda prod: prod.url)

    assert len(sorted_products) == len(sorted_gt_products)
    assert set(sorted_products) == set(sorted_gt_products)
