import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_loading')))

import pytest
from ..data_loading.parse_listings_info import (
    safe_get, replace_line_breaks, get_listing_presentation,
    parse_house_rules, parse_amenities, parse_description, parse_listing
)
from ..data_loading.utils import read_jsonl


# Helper functions
def get_sample_data(filename):
    return read_jsonl(os.path.join(os.path.dirname(__file__), 'test_data', filename))


def compare_results(expected, result, listing_id, context):
    assert result == expected, (
        f"Listing id: {listing_id}\n"
        f"Failed to {context} correctly.\n"
        f"Expected: {expected}\n"
        f"Got: {result}"
    )


# Sample and parsed data
samples = {
    '172222': get_sample_data('172222.jsonl'),
    '888757305688084444': get_sample_data('888757305688084444.jsonl')
}
parsed_data = {
    '172222': get_sample_data('172222_parsed_result.jsonl')[0],
    '888757305688084444': get_sample_data('888757305688084444_parsed_result.jsonl')[0]
}


# Test functions
def test_safe_get():
    sample_dict = {"a": {"b": {"c": "value"}}}
    assert safe_get(sample_dict, ["a", "b", "c"]) == "value"
    assert safe_get(sample_dict, ["a", "x", "c"]) is None


def test_replace_line_breaks():
    sample_dict = {"key1": "line1\nline2", "key2": ["line3\nline4"]}
    expected_output = {"key1": "line1 %%% line2", "key2": ["line3 %%% line4"]}
    assert replace_line_breaks(sample_dict) == expected_output


def test_get_listing_presentation():
    for listing_id, sample in samples.items():
        expected = get_sample_data(f'{listing_id}_expected_presentation.jsonl')[0]
        result = get_listing_presentation(sample, "test_id")
        compare_results(expected, result, listing_id, "get listing presentation")


def test_parse_house_rules():
    for listing_id, sample in samples.items():
        presentation = get_listing_presentation(sample, "test_id")
        result = parse_house_rules("test_id", presentation)
        expected = {k: parsed_data[listing_id][k] for k in parsed_data[listing_id] if k.endswith('_house_rule')}
        compare_results(expected, result, listing_id, "parse house rules")


def test_parse_amenities():
    for listing_id, sample in samples.items():
        presentation = get_listing_presentation(sample, "test_id")
        result = parse_amenities("test_id", presentation)
        expected = {k: parsed_data[listing_id][k] for k in parsed_data[listing_id] if k.endswith('_amenities')}
        compare_results(expected, result, listing_id, "parse amenities")


def test_parse_description():
    for listing_id, sample in samples.items():
        presentation = get_listing_presentation(sample, "test_id")
        result = parse_description("test_id", presentation)
        expected = {k: parsed_data[listing_id][k] for k in parsed_data[listing_id] if k.endswith('_description')}
        compare_results(expected, result, listing_id, "parse description")


def test_parse_listing():
    for listing_id, sample in samples.items():
        result = parse_listing(sample, listing_id)
        compare_results(parsed_data[listing_id], result, listing_id, "parse listing")
