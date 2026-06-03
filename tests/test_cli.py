from __future__ import annotations

import pytest

from scripts import kedu


def test_cli_program_is_kedu():
    parser = kedu.build_parser()
    assert parser.prog == "kedu"


def test_cli_version_flag(capsys):
    parser = kedu.build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--version"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert out.strip() == f"kedu {kedu.KEDU_VERSION}"


def test_cli_version_matches_pyproject():
    import tomllib
    from pathlib import Path

    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    assert kedu.KEDU_VERSION == data["project"]["version"]


def test_init_cli_is_local_first_with_host():
    args = kedu.build_parser().parse_args(["init", "--host", "codex"])
    assert args.host == "codex"
    assert args.global_init is False


def test_init_cli_supports_optional_global():
    args = kedu.build_parser().parse_args(["init", "--host", "kiro", "--global"])
    assert args.host == "kiro"
    assert args.global_init is True
