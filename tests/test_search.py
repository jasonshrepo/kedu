from __future__ import annotations

from scripts import capture, paths, query_log, search, util
from tests.conftest import sample_entry


def test_current_project_scope(kedu_env):
    capture.log_entry(sample_entry(id="a:1", project="repo"), source="manual", project="repo", cwd=kedu_env["project"])
    capture.log_entry(sample_entry(id="b:1", project="other", body_md="auth in other"), source="manual", project="other", cwd=kedu_env["project"])
    results = search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"], query="auth")
    assert [entry["project"] for entry in results] == ["repo"]


def test_all_scope_searches_multiple_projects(kedu_env):
    capture.log_entry(sample_entry(id="a:1", body_md="deploy auth"), source="manual", project="repo", cwd=kedu_env["project"])
    capture.log_entry(sample_entry(id="b:1", body_md="deploy auth"), source="manual", project="other", cwd=kedu_env["project"])
    results = search.search_entries(scope="all", cwd=kedu_env["project"], query="deploy")
    assert {entry["project"] for entry in results} == {"repo", "other"}


def test_sort_order_controls_direction(kedu_env):
    capture.log_entry(sample_entry(id="a:1", ts="2026-06-01T10:00:00+10:00"), source="manual", project="repo", cwd=kedu_env["project"])
    capture.log_entry(sample_entry(id="b:1", ts="2026-06-03T10:00:00+10:00"), source="manual", project="repo", cwd=kedu_env["project"])
    desc = search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"])
    assert [entry["id"] for entry in desc] == ["b:1", "a:1"]
    asc = search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"], order="asc")
    assert [entry["id"] for entry in asc] == ["a:1", "b:1"]


def test_sort_by_arbitrary_field(kedu_env):
    capture.log_entry(sample_entry(id="a:1", title="Zeta"), source="manual", project="repo", cwd=kedu_env["project"])
    capture.log_entry(sample_entry(id="b:1", title="Alpha"), source="manual", project="repo", cwd=kedu_env["project"])
    results = search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"], sort="title", order="asc")
    assert [entry["title"] for entry in results] == ["Alpha", "Zeta"]


def test_body_scan_finds_terms_not_in_metadata(kedu_env):
    entry = sample_entry(search_terms=[], title="Unrelated", tags=[], next_steps=[], body_md="Need to fix auth_cookie_expired")
    capture.log_entry(entry, source="manual", project="repo", cwd=kedu_env["project"])
    results = search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"], query="auth_cookie_expired")
    assert len(results) == 1


def test_query_log_is_written_and_redacted(kedu_env):
    capture.log_entry(sample_entry(body_md="hello"), source="manual", project="repo", cwd=kedu_env["project"])
    search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"], query="AKIAIOSFODNN7EXAMPLE")
    kedu_paths = paths.resolve_paths(project="repo", cwd=kedu_env["project"])
    events = util.read_jsonl(kedu_paths.query_log)
    assert events
    assert events[-1]["query"] == "[REDACTED:aws_access_key]"


def test_query_log_failure_does_not_abort_search(kedu_env, monkeypatch, capsys):
    capture.log_entry(sample_entry(body_md="hello"), source="manual", project="repo", cwd=kedu_env["project"])

    def fail_append(*_args, **_kwargs):
        raise OSError("query log unavailable")

    monkeypatch.setattr(query_log.util, "append_jsonl", fail_append)
    results = search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"], query="hello")

    assert len(results) == 1
    assert "warning: failed to write query log: query log unavailable" in capsys.readouterr().err


def test_agent_filter(kedu_env):
    capture.log_entry(sample_entry(id="claude:1", agent="claude-code", body_md="shared fix"), source="manual", project="repo", cwd=kedu_env["project"])
    capture.log_entry(sample_entry(id="codex:1", agent="codex", body_md="shared fix"), source="manual", project="repo", cwd=kedu_env["project"])
    results = search.search_entries(scope="current_project", project="repo", cwd=kedu_env["project"], query="shared", agent="codex")
    assert [entry["agent"] for entry in results] == ["codex"]
