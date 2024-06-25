import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_loading')))

import pytest
from ..data_loading.parse_listings_info import safe_get, replace_line_breaks, get_listing_presentation
from ..data_loading.utils import read_jsonl

# Sample data from the .jsonl file
sample_file_path = os.path.join(os.path.dirname(__file__), 'test_data', '172222.jsonl')
sample_data = read_jsonl(sample_file_path)
sample_listing_info_json = sample_data

# expected_parsed_result_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'parsed_result.jsonl')
# expected_parsed_result = read_jsonl(sample_file_path)[0]



# # Sample presentation extracted from sample data
# sample_presentation = sample_listing_info_json[0]['presentation']


def test_safe_get():
    sample_dict = {"a": {"b": {"c": "value"}}}
    assert safe_get(sample_dict, ["a", "b", "c"]) == "value"
    assert safe_get(sample_dict, ["a", "x", "c"]) is None


def test_replace_line_breaks():
    sample_dict = {"key1": "line1\nline2", "key2": ["line3\nline4"]}
    expected_output = {"key1": "line1 %%% line2", "key2": ["line3 %%% line4"]}
    assert replace_line_breaks(sample_dict) == expected_output


def test_get_listing_presentation():
    expected_presentation_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'expected_presentation.jsonl')
    expected_presentation = read_jsonl(expected_presentation_file_path)[0]

    result = get_listing_presentation(sample_listing_info_json, "test_id")
    assert result == expected_presentation


# def test_parse_house_rules_json():
#     result = parse_house_rules_json("test_id", sample_presentation)
#     expected = {
#         "no_smoking_house_rule": ["No smoking anywhere on the property"],
#         "additional_rules_house_rule": ["Additional rules: Be quiet after 10 PM", "Be quiet after 10 PM"]
#     }
#     assert result == expected