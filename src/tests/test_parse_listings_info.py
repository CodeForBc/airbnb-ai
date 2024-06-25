import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_loading')))

import pytest
from ..data_loading.parse_listings_info import safe_get, replace_line_breaks, \
    get_listing_presentation, parse_house_rules, parse_amenities, parse_description
from ..data_loading.utils import read_jsonl

# Sample data from the .jsonl file
sample_file_path = os.path.join(os.path.dirname(__file__), 'test_data', '172222.jsonl')
sample_data = read_jsonl(sample_file_path)
sample_listing_info_json = sample_data

expected_parsed_result_file_path = os.path.join(os.path.dirname(__file__), 'test_data', '172222_parsed_result.jsonl')
parsed_listing_data = read_jsonl(expected_parsed_result_file_path)[0]



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
    expected_presentation_file_path = os.path.join(os.path.dirname(__file__), 'test_data', '172222_expected_presentation.jsonl')
    expected_presentation = read_jsonl(expected_presentation_file_path)[0]

    result_presentation = get_listing_presentation(sample_listing_info_json, "test_id")

    assert result_presentation == expected_presentation, (
        f"Failed to get listing presentation correctly.\n"
        f"Expected: {expected_presentation}\n"
        f"Got: {result_presentation}"
    )


def test_parse_house_rules():
    presentation = get_listing_presentation(sample_listing_info_json, "test_id")
    result_house_rules = parse_house_rules("test_id", presentation)

    expected_house_rules = dict((key, parsed_listing_data[key]) 
                                for key in parsed_listing_data.keys() if key.endswith('_house_rule'))

    assert result_house_rules == expected_house_rules,  (
        f"Failed to parse house rules correctly.\n"
        f"Expected: {expected_house_rules}\n"
        f"Got: {result_house_rules}"
    )


def test_parse_amenities():
    presentation = get_listing_presentation(sample_listing_info_json, "test_id")
    result_amenities = parse_amenities("test_id", presentation)

    expected_amenities = dict((key, parsed_listing_data[key]) 
                              for key in parsed_listing_data.keys() if key.endswith('_amenities'))

    assert result_amenities == expected_amenities, (
        f"Failed to parse amenities correctly.\n"
        f"Expected: {expected_amenities}\n"
        f"Got: {result_amenities}"
    )


def test_parse_description():
    presentation = get_listing_presentation(sample_listing_info_json, "test_id")
    result_description = parse_description("test_id", presentation)

    expected_description = dict((key, parsed_listing_data[key]) 
                                for key in parsed_listing_data.keys() if key.endswith('_description'))

    assert result_description == expected_description, (
        f"Failed to parse description correctly.\n"
        f"Expected: {expected_description}\n"
        f"Got: {result_description}"
    )