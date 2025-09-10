import pytest
from api.image_utils import ImageUtils


def test_image_dimensions_should_be_scaled_correctly_with_width():
    original_width, original_height = 2048, 1536
    new_width, expected_height = 512, 384

    width, height = ImageUtils.calculate_scaled_size(
        original_width=original_width, original_height=original_height, width=new_width
    )
    assert height == expected_height
    assert width == new_width


def test_image_dimensions_should_be_scaled_correctly_with_height():
    original_width, original_height = 1536, 2048
    expected_width, new_height = 384, 512

    width, height = ImageUtils.calculate_scaled_size(
        original_width=original_width,
        original_height=original_height,
        height=new_height,
    )
    assert height == new_height
    assert width == expected_width


def test_image_dimensions_should_be_scaled_correctly_with_smaller_width():
    original_width, original_height = 1536, 2048
    new_width, expected_height = 384, 512

    width, height = ImageUtils.calculate_scaled_size(
        original_width=original_width, original_height=original_height, width=new_width
    )
    assert height == expected_height
    assert width == new_width


def test_image_dimensions_should_be_scaled_correctly_with_smaller_height():
    original_width, original_height = 2048, 1536
    expected_width, new_height = 512, 384

    width, height = ImageUtils.calculate_scaled_size(
        original_width=original_width,
        original_height=original_height,
        height=new_height,
    )
    assert height == new_height
    assert width == expected_width
