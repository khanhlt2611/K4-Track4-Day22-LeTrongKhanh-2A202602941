"""Kiểm tra định dạng kết quả bằng dòng giả, không dùng dữ liệu lab."""
import pytest
from validate_submission import validate_rows


def test_valid_rows_allow_frames_without_boxes():
    assert validate_rows(['1,1,0,0,10,20,.9,-1,-1,-1', '3,1,2,2,10,20,.8,-1,-1,-1'], 3) == 2


@pytest.mark.parametrize('row', [
    '1,1,0,0,10,20,.9',
    '4,1,0,0,10,20,.9,-1,-1,-1',
    '1.5,1,0,0,10,20,.9,-1,-1,-1',
    '1,-1,0,0,10,20,.9,-1,-1,-1',
    '1,1,nan,0,10,20,.9,-1,-1,-1',
    '1,1,0,0,0,20,.9,-1,-1,-1',
    '1,1,0,0,10,20,1.1,-1,-1,-1',
])
def test_invalid_rows_fail(row):
    with pytest.raises(ValueError):
        validate_rows([row], 3)


def test_duplicate_identity_fails():
    row='1,1,0,0,10,20,.9,-1,-1,-1'
    with pytest.raises(ValueError):
        validate_rows([row,row], 3)


def test_empty_result_fails():
    with pytest.raises(ValueError):
        validate_rows([], 3)
