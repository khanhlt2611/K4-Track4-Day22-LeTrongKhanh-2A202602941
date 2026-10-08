"""Kiểm tra phần chấm bằng dữ liệu giả, không dùng GPU hoặc mạng."""
import json
import pytest
from evaluate_practice import _load_eval_config, run_trackeval, stage


def test_missing_config_uses_lab(tmp_path):
    assert _load_eval_config(tmp_path) == {"benchmark": "LAB", "split": "train"}


def test_explicit_config(tmp_path):
    folder = tmp_path / "video_1"
    folder.mkdir()
    config = {"benchmark": "LAB", "split": "test"}
    (folder / "eval_config.json").write_text(json.dumps(config), encoding="utf-8")
    assert _load_eval_config(tmp_path) == config


def test_stage_respects_split(tmp_path):
    source = tmp_path / "lab/video_1"
    (source / "gt").mkdir(parents=True)
    (source / "gt/gt.txt").write_text("1,1,0,0,10,10,1,1,1")
    (source / "seqinfo.ini").write_text("[Sequence]\nseqLength=1")
    submission = tmp_path / "video_1.txt"
    submission.write_text("1,1,0,0,10,10,0.9,-1,-1,-1")
    root = tmp_path / "evaluation"
    stage(root, tmp_path / "lab", submission, "solo", "LAB", "test")
    assert (root / "data/gt/mot_challenge/LAB-test/video_1/gt/gt.txt").is_file()
    assert (root / "data/trackers/mot_challenge/LAB-test/solo/data/video_1.txt").read_text() == submission.read_text()


def test_missing_labels_fail(tmp_path):
    with pytest.raises(FileNotFoundError):
        stage(tmp_path, tmp_path / "lab", tmp_path / "video_1.txt", "solo", "LAB")


def test_patch_in_child(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr("evaluate_practice.subprocess.run", lambda cmd, **kwargs: calls.append(cmd))
    run_trackeval(tmp_path, "solo", "LAB", "train")
    assert calls[0][1] == "-c"
    assert "np.float = float" in calls[0][2]
    assert calls[0][calls[0].index("--SEQ_INFO") + 1] == "video_1"
