
import sys

from main import parse_args



def test_parse_args_defaults(monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py"]
    )

    args = parse_args()

    assert args.red is None
    assert args.timeout == 3.0
    assert args.iface is None
    assert args.save is None
    assert args.json_output is None
    assert args.no_name is False



def test_parse_args_custom_values(monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "-r",
            "10.0.0.0/24",
            "--timeout",
            "5",
            "--max-workers",
            "10",
            "--no-name",
        ],
    )

    args = parse_args()

    assert args.red == "10.0.0.0/24"
    assert args.timeout == 5.0
    assert args.max_workers == 10
    assert args.no_name is True
