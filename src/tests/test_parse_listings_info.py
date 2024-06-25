import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_loading')))

import pytest
from ..data_loading.parse_listings_info import safe_get, replace_line_breaks, \
    get_listing_presentation, parse_house_rules, parse_amenities, parse_description, \
    parse_listing
from ..data_loading.utils import read_jsonl

# Sample data from downloaded jsons out of htmls
sample_file_path_172222 = os.path.join(os.path.dirname(__file__), 
                                       'test_data', 
                                       '172222.jsonl')
sample_listing_info_json_172222 = read_jsonl(sample_file_path_172222)

sample_file_path_888757305688084444 = os.path.join(os.path.dirname(__file__), 
                                                   'test_data', 
                                                   '888757305688084444.jsonl')
sample_listing_info_json_888757305688084444 = read_jsonl(sample_file_path_888757305688084444)

# Parsed listing data 
expected_parsed_result_file_path_172222 = os.path.join(os.path.dirname(__file__), 
                                                       'test_data', 
                                                       '172222_parsed_result.jsonl')
parsed_listing_data_172222 = read_jsonl(expected_parsed_result_file_path_172222)[0]

expected_parsed_result_file_path_888757305688084444 = os.path.join(os.path.dirname(__file__), 
                                                                   'test_data', 
                                                                   '888757305688084444_parsed_result.jsonl')
parsed_listing_data_888757305688084444 = read_jsonl(expected_parsed_result_file_path_888757305688084444)[0]


def test_safe_get():
    sample_dict = {"a": {"b": {"c": "value"}}}
    assert safe_get(sample_dict, ["a", "b", "c"]) == "value"
    assert safe_get(sample_dict, ["a", "x", "c"]) is None


def test_replace_line_breaks():
    sample_dict = {"key1": "line1\nline2", "key2": ["line3\nline4"]}
    expected_output = {"key1": "line1 %%% line2", "key2": ["line3 %%% line4"]}
    assert replace_line_breaks(sample_dict) == expected_output


def test_get_listing_presentation():
    expected_presentation_file_path = os.path.join(os.path.dirname(__file__), 
                                                   'test_data', 
                                                   '172222_expected_presentation.jsonl')
    expected_presentation = read_jsonl(expected_presentation_file_path)[0]

    result_presentation = get_listing_presentation(sample_listing_info_json_172222, "test_id")

    assert result_presentation == expected_presentation, (
        f"Listing id: 172222\n"
        f"Failed to get listing presentation correctly.\n"
        f"Expected: {expected_presentation}\n"
        f"Got: {result_presentation}"
    )

    expected_presentation_file_path = os.path.join(os.path.dirname(__file__), 
                                                   'test_data', 
                                                   '888757305688084444_expected_presentation.jsonl')
    expected_presentation = read_jsonl(expected_presentation_file_path)[0]

    result_presentation = get_listing_presentation(sample_listing_info_json_888757305688084444, "test_id")

    assert result_presentation == expected_presentation, (
        f"Listing id: 888757305688084444\n"
        f"Failed to get listing presentation correctly.\n"
        f"Expected: {expected_presentation}\n"
        f"Got: {result_presentation}"
    )


def test_parse_house_rules():
    presentation = get_listing_presentation(sample_listing_info_json_172222, "test_id")
    result_house_rules = parse_house_rules("test_id", presentation)

    expected_house_rules = dict((key, parsed_listing_data_172222[key]) 
                                for key in parsed_listing_data_172222.keys() if key.endswith('_house_rule'))

    assert result_house_rules == expected_house_rules,  (
        f"Listing id: 172222\n"
        f"Failed to parse house rules correctly.\n"
        f"Expected: {expected_house_rules}\n"
        f"Got: {result_house_rules}"
    )

    presentation = get_listing_presentation(sample_listing_info_json_888757305688084444, "test_id")
    result_house_rules = parse_house_rules("test_id", presentation)

    expected_house_rules = dict((key, parsed_listing_data_888757305688084444[key]) 
                                for key in parsed_listing_data_888757305688084444.keys() if key.endswith('_house_rule'))

    assert result_house_rules == expected_house_rules,  (
        f"Listing id: 888757305688084444\n"
        f"Failed to parse house rules correctly.\n"
        f"Expected: {expected_house_rules}\n"
        f"Got: {result_house_rules}"
    )


def test_parse_amenities():
    presentation = get_listing_presentation(sample_listing_info_json_172222, "test_id")
    result_amenities = parse_amenities("test_id", presentation)

    expected_amenities = dict((key, parsed_listing_data_172222[key]) 
                              for key in parsed_listing_data_172222.keys() if key.endswith('_amenities'))

    assert result_amenities == expected_amenities, (
        f"Listing id: 172222\n"
        f"Failed to parse amenities correctly.\n"
        f"Expected: {expected_amenities}\n"
        f"Got: {result_amenities}"
    )

    presentation = get_listing_presentation(sample_listing_info_json_888757305688084444, "test_id")
    result_amenities = parse_amenities("test_id", presentation)

    expected_amenities = dict((key, parsed_listing_data_888757305688084444[key]) 
                              for key in parsed_listing_data_888757305688084444.keys() if key.endswith('_amenities'))

    assert result_amenities == expected_amenities, (
        f"Listing id: 888757305688084444\n"
        f"Failed to parse amenities correctly.\n"
        f"Expected: {expected_amenities}\n"
        f"Got: {result_amenities}"
    )


def test_parse_description():
    presentation = get_listing_presentation(sample_listing_info_json_172222, "test_id")
    result_description = parse_description("test_id", presentation)

    expected_description = dict((key, parsed_listing_data_172222[key]) 
                                for key in parsed_listing_data_172222.keys() if key.endswith('_description'))

    assert result_description == expected_description, (
        f"Listing id: 172222\n"
        f"Failed to parse description correctly.\n"
        f"Expected: {expected_description}\n"
        f"Got: {result_description}"
    )

    presentation = get_listing_presentation(sample_listing_info_json_888757305688084444, "test_id")
    result_description = parse_description("test_id", presentation)

    expected_description = dict((key, parsed_listing_data_888757305688084444[key]) 
                                for key in parsed_listing_data_888757305688084444.keys() if key.endswith('_description'))

    assert result_description == expected_description, (
        f"Listing id: 888757305688084444\n"
        f"Failed to parse description correctly.\n"
        f"Expected: {expected_description}\n"
        f"Got: {result_description}"
    )


def test_parse_listing():
    result_parcing_dict_172222 = parse_listing(sample_listing_info_json_172222, "172222")

    assert result_parcing_dict_172222 == parsed_listing_data_172222, (
        f"Listing id: 172222\n"
        f"Failed to parse description correctly.\n"
        f"Expected: {parsed_listing_data_172222}\n"
        f"Got: {result_parcing_dict_172222}"
    )

    result_parcing_dict_888757305688084444 = parse_listing(sample_listing_info_json_888757305688084444,
                                                        "888757305688084444")

    assert result_parcing_dict_888757305688084444 == parsed_listing_data_888757305688084444, (
        f"Listing id: 888757305688084444\n"
        f"Failed to parse description correctly.\n"
        f"Expected: {parsed_listing_data_888757305688084444}\n"
        f"Got: {result_parcing_dict_888757305688084444}"
    )
