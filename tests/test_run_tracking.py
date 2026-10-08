"""Kiểm tra ảnh giả và màu ID; không tải mô hình hoặc dùng GPU."""
import cv2
import numpy as np
import pytest
from run_tracking import color_for_id, iter_frames


def test_color_is_stable_and_in_range():
    color = color_for_id(42)
    assert color == color_for_id(42)
    assert len(color) == 3
    assert all(64 <= channel <= 254 for channel in color)


def test_unicode_image_path(tmp_path):
    folder = tmp_path / 'ảnh thử'
    folder.mkdir()
    image = np.full((8, 8, 3), 120, dtype=np.uint8)
    ok, encoded = cv2.imencode('.jpg', image)
    assert ok
    encoded.tofile(folder / '000001.jpg')
    frames = list(iter_frames(folder))
    assert len(frames) == 1
    assert frames[0][0] == 0
    assert frames[0][1].shape == (8, 8, 3)


def test_corrupt_image_fails(tmp_path):
    (tmp_path / '000001.jpg').write_bytes(b'anh hong')
    with pytest.raises(ValueError):
        list(iter_frames(tmp_path))
