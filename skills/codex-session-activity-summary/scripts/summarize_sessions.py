#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


LANGUAGE_LABELS = {
    "en": {
        "summary_header": "Work activity summary {date}:",
        "timeline_header": "Work activity timeline {date}:",
        "workspace_header": "Work activity by workspace {date}:",
        "no_activity": "No activity could be extracted from Codex sessions for {date}.",
        "no_sessions": "No Codex sessions found for {date}.",
        "workspace_label": "Workspace: {repo_label} ({workspace_path})",
        "workspace_label_no_path": "Workspace: {repo_label}",
        "unknown_workspace": "unknown-workspace",
        "timeline_item": "{time} [{repo_label}] {activity}",
        "timeline_time_unknown": "unknown-time",
        "activities": {
            "activity_summary": "Summarized work activity or progress from Codex sessions.",
            "skill_workflow": "Created or adjusted Codex skills for a specific workflow.",
            "review_changes": "Reviewed changes or implementation work in progress.",
            "recaptcha": "Analyzed and adjusted the reCAPTCHA implementation on the token generator page.",
            "browser_error": "Investigated browser errors and failing application flows.",
            "copy_token": "Checked user interaction flows such as captcha load, widget reset, and token copy.",
            "git_status": "Checked repository status, file changes, or commit history.",
            "search_issue": "Searched the codebase or logs for issue-related keywords.",
            "read_problematic_impl": "Read application files to understand the failing flow.",
            "inspect_core_files": "Reviewed core project files to understand configuration or implementation details.",
            "search_project_structure": "Explored the project structure and searched for relevant files.",
            "inspect_file_single": "Reviewed the implementation in `{target}`.",
            "inspect_file_multi": "Reviewed several relevant files, including {targets}.",
            "skill_codex_sessions": "Created a skill to summarize work activity from Codex sessions.",
            "skill_deploy": "Adjusted the deploy skill so commit rules, env handling, and release numbering stay consistent.",
            "skill_commit_push": "Adjusted the commit and push skill workflow to match repository needs.",
            "skill_pr_mr": "Created a skill for PR or MR workflows, including target branch and message needs.",
            "skill_glab": "Created a `glab` setup skill that can be used across operating systems.",
        },
    },
    "id": {
        "summary_header": "Ringkasan aktivitas {date}:",
        "timeline_header": "Timeline aktivitas {date}:",
        "workspace_header": "Aktivitas per workspace {date}:",
        "no_activity": "Tidak ada aktivitas yang berhasil diekstrak dari Codex sessions untuk {date}.",
        "no_sessions": "No Codex sessions found for {date}.",
        "workspace_label": "Workspace: {repo_label} ({workspace_path})",
        "workspace_label_no_path": "Workspace: {repo_label}",
        "unknown_workspace": "unknown-workspace",
        "timeline_item": "{time} [{repo_label}] {activity}",
        "timeline_time_unknown": "jam-tidak-diketahui",
        "activities": {
            "activity_summary": "Merangkum aktivitas atau progres kerja dari sesi Codex.",
            "skill_workflow": "Menyusun atau menyesuaikan skill Codex untuk kebutuhan workflow tertentu.",
            "review_changes": "Melakukan review terhadap perubahan atau implementasi yang sedang dikerjakan.",
            "recaptcha": "Menganalisis dan menyesuaikan implementasi reCAPTCHA pada halaman token generator.",
            "browser_error": "Menginvestigasi penyebab error dan kegagalan alur aplikasi di browser.",
            "copy_token": "Memeriksa alur interaksi pengguna seperti load captcha, reset widget, dan copy token.",
            "git_status": "Memeriksa status kerja, perubahan file, atau riwayat repository.",
            "search_issue": "Menelusuri penyebab issue melalui pencarian kata kunci pada kode atau log.",
            "read_problematic_impl": "Membaca implementasi file aplikasi untuk memahami alur yang sedang bermasalah.",
            "inspect_core_files": "Memeriksa file inti proyek untuk memahami konfigurasi atau implementasi yang sedang dikerjakan.",
            "search_project_structure": "Menelusuri struktur proyek dan mencari file yang relevan dengan task.",
            "inspect_file_single": "Memeriksa implementasi pada file `{target}`.",
            "inspect_file_multi": "Memeriksa implementasi pada beberapa file yang relevan, termasuk {targets}.",
            "skill_codex_sessions": "Membuat skill baru untuk merangkum aktivitas kerja dari Codex sessions.",
            "skill_deploy": "Menyesuaikan skill deploy agar aturan commit, env, dan penomoran rilis lebih konsisten.",
            "skill_commit_push": "Menyesuaikan workflow skill commit dan push agar sesuai kebutuhan repository.",
            "skill_pr_mr": "Menyusun skill untuk alur request PR atau MR, termasuk kebutuhan target branch dan message.",
            "skill_glab": "Membuat skill setup `glab` yang bisa dipakai lintas OS.",
        },
    },
}

INDONESIAN_HINT_RE = re.compile(
    r"\b(yang|dan|atau|buat|dong|gak|nggak|gua|gue|lu|aku|saya|aktivitas|ringkas|rangkum|rekap|kemarin|hari ini|lusa|bahasa)\b",
    re.I,
)

USER_HINT_PATTERNS = [
    (re.compile(r"\b(summary|ringkas|rangkum|rekap|worklog|aktivitas)\b", re.I), "activity_summary", 8),
    (re.compile(r"\b(skill)\b", re.I), "skill_workflow", 5),
    (re.compile(r"\b(review)\b", re.I), "review_changes", 8),
    (re.compile(r"\b(recaptcha|captcha)\b", re.I), "recaptcha", 9),
    (re.compile(r"\b(console log|error|gagal|failed|origin|localhost|domain|site key|sitekey)\b", re.I), "browser_error", 9),
    (re.compile(r"\b(copy token|clipboard|reset widget|load captcha)\b", re.I), "copy_token", 8),
]

COMMAND_HINT_PATTERNS = [
    (re.compile(r"\bgit\b.*\b(status|diff|log|show)\b", re.I), "git_status", 2),
    (re.compile(r"\brg\b.*\b(error|failed|exception|origin|localhost|domain|recaptcha|captcha)\b", re.I), "search_issue", 5),
    (re.compile(r"\bsed\b.*\b(index\.html|\.tsx?|\.jsx?)\b", re.I), "read_problematic_impl", 4),
    (re.compile(r"\b(cat|sed|nl)\b.*\b(package\.json|index\.html|README|AGENTS\.md|SKILL\.md)\b", re.I), "inspect_core_files", 2),
    (re.compile(r"\b(find|rg --files|rg\b)", re.I), "search_project_structure", 2),
]


@dataclass
class Candidate:
    text: str
    score: int
    source: str
    evidence: list[str] = field(default_factory=list)
    cwd: str | None = None
    timestamp: str | None = None


def get_text(lang: str, key: str, **kwargs: str) -> str:
    return LANGUAGE_LABELS[lang][key].format(**kwargs)


def get_activity_text(lang: str, key: str, **kwargs: str) -> str:
    return LANGUAGE_LABELS[lang]["activities"][key].format(**kwargs)


def resolve_language(lang_arg: str, user_text: str | None) -> str:
    if lang_arg in {"en", "id"}:
        return lang_arg
    if user_text and INDONESIAN_HINT_RE.search(user_text):
        return "id"
    return "en"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize work activity from Codex session JSONL logs.")
    parser.add_argument("--date", required=True, help="Target date in YYYY-MM-DD format.")
    parser.add_argument(
        "--sessions-root",
        default=str(Path.home() / ".codex" / "sessions"),
        help="Root path of Codex sessions.",
    )
    parser.add_argument("--max-items", type=int, default=0, help="Maximum number of items to return in the selected view.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--lang", choices=["auto", "en", "id"], default="auto", help="Output language.")
    parser.add_argument("--user-text", default="", help="Original user request for language auto-detection.")
    parser.add_argument(
        "--view",
        choices=["per_workspace", "timeline", "summary"],
        default="per_workspace",
        help="Primary output view. `summary` preserves the old compact behavior.",
    )
    parser.add_argument(
        "--discover-git-repos",
        action="store_true",
        help="Discover repository roots by scanning configured search roots for .git directories.",
    )
    parser.add_argument(
        "--repo-search-root",
        action="append",
        default=[],
        help="Search root used for scoped .git discovery. May be passed multiple times.",
    )
    return parser.parse_args()


def get_session_files(root: Path, date_str: str) -> list[Path]:
    yyyy, mm, dd = date_str.split("-")
    day_dir = root / yyyy / mm / dd
    if not day_dir.exists():
        return []
    return sorted(day_dir.glob("*.jsonl"))


def iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_key(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[`\"'.,:;()/_-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def trim_message(text: str, limit: int = 180) -> str:
    text = compact(text)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def derive_workspace_label(cwd: str | None) -> str | None:
    if not cwd:
        return None
    path = Path(cwd)
    name = path.name.strip()
    return name or cwd


def discover_repo_roots(search_roots: list[str]) -> list[str]:
    repo_roots: set[str] = set()
    for root in search_roots:
        root_path = Path(root).expanduser()
        if not root_path.exists():
            continue
        try:
            result = subprocess.run(
                ["find", str(root_path), "-type", "d", "-name", ".git"],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            continue
        if result.returncode not in {0, 1}:
            continue
        for line in result.stdout.splitlines():
            git_dir = line.strip()
            if git_dir:
                repo_roots.add(str(Path(git_dir).parent))
    return sorted(repo_roots)


def match_repo_root(cwd: str | None, repo_roots: list[str]) -> str | None:
    if not cwd:
        return None
    cwd_path = Path(cwd)
    best_match: Path | None = None
    for repo_root in repo_roots:
        repo_path = Path(repo_root)
        try:
            if not cwd_path.is_relative_to(repo_path):
                continue
        except ValueError:
            continue
        if best_match is None or len(repo_path.parts) > len(best_match.parts):
            best_match = repo_path
    return str(best_match) if best_match else None


def infer_file_activity(command: str, lang: str) -> str | None:
    file_matches = re.findall(r"([A-Za-z0-9_./-]+\.(?:html|json|jsx|js|tsx|ts|md|py|sh))(?![A-Za-z0-9_])", command)
    if not file_matches:
        return None
    targets = sorted({Path(match).name for match in file_matches})
    if len(targets) == 1:
        return get_activity_text(lang, "inspect_file_single", target=targets[0])
    joined = ", ".join(f"`{name}`" for name in targets[:3])
    return get_activity_text(lang, "inspect_file_multi", targets=joined)


def infer_skill_specific_activity(text: str, lang: str) -> str | None:
    lowered = text.lower()
    if "codex sessions" in lowered or "session" in lowered:
        return get_activity_text(lang, "skill_codex_sessions")
    if "deploy" in lowered:
        return get_activity_text(lang, "skill_deploy")
    if re.search(r"\b(commit|push)\b", lowered):
        return get_activity_text(lang, "skill_commit_push")
    if re.search(r"\b(pr|mr|merge request|pull request)\b", lowered):
        return get_activity_text(lang, "skill_pr_mr")
    if "glab" in lowered:
        return get_activity_text(lang, "skill_glab")
    return None


def infer_from_user_message(text: str, lang: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    cleaned = compact(text)
    for pattern, activity_key, score in USER_HINT_PATTERNS:
        if pattern.search(cleaned):
            candidates.append(
                Candidate(
                    text=get_activity_text(lang, activity_key),
                    score=score,
                    source="user_message",
                    evidence=[trim_message(cleaned)],
                )
            )
    specific_skill_activity = infer_skill_specific_activity(cleaned, lang)
    if specific_skill_activity:
        candidates.append(
            Candidate(
                text=specific_skill_activity,
                score=11,
                source="user_message",
                evidence=[trim_message(cleaned)],
            )
        )
    return candidates


def infer_from_command(command: str, lang: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    cmd = compact(command)
    for pattern, activity_key, score in COMMAND_HINT_PATTERNS:
        if pattern.search(cmd):
            candidates.append(
                Candidate(
                    text=get_activity_text(lang, activity_key),
                    score=score,
                    source="command",
                    evidence=[trim_message(cmd)],
                )
            )
    file_activity = infer_file_activity(cmd, lang)
    if file_activity:
        candidates.append(
            Candidate(
                text=file_activity,
                score=4,
                source="command",
                evidence=[trim_message(cmd)],
            )
        )
    return candidates


def merge_candidates(candidates: list[Candidate]) -> list[dict]:
    merged: dict[str, Candidate] = {}
    for item in candidates:
        key = normalize_key(item.text)
        existing = merged.get(key)
        if existing is None:
            merged[key] = item
            continue
        score_cap = 50 if existing.source == "user_message" or item.source == "user_message" else 18
        existing.score = min(existing.score + item.score, score_cap)
        for ev in item.evidence:
            if ev not in existing.evidence:
                existing.evidence.append(ev)
        if not existing.cwd and item.cwd:
            existing.cwd = item.cwd
        if not existing.timestamp or (item.timestamp and item.timestamp < existing.timestamp):
            existing.timestamp = item.timestamp

    def sort_key(item: Candidate) -> tuple[int, int, int, str]:
        source_rank = 2 if item.source == "user_message" else 1
        return (item.score, source_rank, len(item.evidence), item.text)

    ordered = sorted(merged.values(), key=sort_key, reverse=True)
    return [
        {
            "activity": item.text,
            "score": item.score,
            "source": item.source,
            "cwd": item.cwd,
            "timestamp": item.timestamp,
            "evidence": item.evidence[:3],
        }
        for item in ordered
    ]


def format_time_short(timestamp: str | None, lang: str) -> str:
    if not timestamp:
        return get_text(lang, "timeline_time_unknown")
    try:
        value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return timestamp
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    value = value.astimezone(timezone.utc)
    return value.strftime("%H:%M:%SZ")


def parse_timestamp(timestamp: str | None) -> datetime | None:
    if not timestamp:
        return None
    try:
        value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def dedupe_timeline_events(candidates: list[Candidate]) -> list[dict]:
    ordered = sorted(
        candidates,
        key=lambda item: (
            item.timestamp or "",
            item.cwd or "",
            item.source,
            item.text,
            item.evidence[0] if item.evidence else "",
        ),
    )
    deduped: list[Candidate] = []
    last_item_by_activity: dict[tuple[str | None, str], Candidate] = {}
    for item in ordered:
        activity_key = (item.cwd, normalize_key(item.text))
        last_item = last_item_by_activity.get(activity_key)
        if last_item is not None:
            current_ts = parse_timestamp(item.timestamp)
            previous_ts = parse_timestamp(last_item.timestamp)
            if current_ts and previous_ts and (current_ts - previous_ts).total_seconds() <= 120:
                continue
            if item.timestamp == last_item.timestamp and item.source == last_item.source:
                continue
        if deduped:
            previous_item = deduped[-1]
            if activity_key == (previous_item.cwd, normalize_key(previous_item.text)):
                continue
        deduped.append(item)
        last_item_by_activity[activity_key] = item
    return [
        {
            "timestamp": item.timestamp,
            "time": format_time_short(item.timestamp, "en"),
            "activity": item.text,
            "source": item.source,
            "cwd": item.cwd,
            "evidence": item.evidence[:1],
        }
        for item in deduped
    ]


def build_workspace_summaries(activities: list[dict], workspaces: list[str], repo_roots: list[str]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in activities:
        key = item.get("cwd") or "__unknown__"
        grouped[key].append(item)

    ordered_keys = [cwd for cwd in workspaces if cwd in grouped]
    if "__unknown__" in grouped:
        ordered_keys.append("__unknown__")

    summaries: list[dict] = []
    for key in ordered_keys:
        items = grouped[key]
        repo_root = match_repo_root(key, repo_roots) if key != "__unknown__" else None
        repo_label = derive_workspace_label(repo_root) if repo_root else (derive_workspace_label(key) if key != "__unknown__" else None)
        summaries.append(
            {
                "workspace": None if key == "__unknown__" else key,
                "repo_root": repo_root,
                "repo_label": repo_label,
                "activity_count": len(items),
                "activities": items,
            }
        )
    return summaries


def summarize_day(files: list[Path], lang: str, repo_roots: list[str]) -> dict:
    candidates: list[Candidate] = []
    timeline_candidates: list[Candidate] = []
    cwds: list[str] = []
    inspected_files: list[str] = []
    raw_counts = defaultdict(int)

    for session_file in files:
        cwd: str | None = None
        for entry in iter_jsonl(session_file):
            entry_type = entry.get("type")
            timestamp = entry.get("timestamp")

            if entry_type == "session_meta":
                payload = entry.get("payload", {})
                cwd = payload.get("cwd")
                if cwd:
                    cwds.append(cwd)
                continue

            if entry_type == "event_msg":
                payload = entry.get("payload", {})
                if payload.get("type") == "user_message":
                    message = payload.get("message") or ""
                    for candidate in infer_from_user_message(message, lang):
                        candidate.cwd = cwd
                        candidate.timestamp = timestamp
                        candidates.append(candidate)
                        timeline_candidates.append(candidate)
                        raw_counts["user_message_candidates"] += 1
                continue

            if entry_type != "response_item":
                continue

            payload = entry.get("payload", {})
            if payload.get("type") != "function_call" or payload.get("name") != "exec_command":
                continue

            arguments = payload.get("arguments")
            if isinstance(arguments, str):
                try:
                    parsed = json.loads(arguments)
                except json.JSONDecodeError:
                    parsed = {}
            else:
                parsed = arguments or {}

            command = parsed.get("cmd") or ""
            for candidate in infer_from_command(command, lang):
                candidate.cwd = cwd
                candidate.timestamp = timestamp
                candidates.append(candidate)
                timeline_candidates.append(candidate)
                raw_counts["command_candidates"] += 1

            for match in re.findall(r"([A-Za-z0-9_./-]+\.(?:html|json|jsx|js|tsx|ts|md|py|sh))(?![A-Za-z0-9_])", command):
                inspected_files.append(match)

    normalized = merge_candidates(candidates)
    unique_cwds = sorted({cwd for cwd in cwds if cwd})
    unique_files = sorted({Path(path).name for path in inspected_files})
    workspace_summaries = build_workspace_summaries(normalized, unique_cwds, repo_roots)
    timeline = dedupe_timeline_events(timeline_candidates)
    for item in timeline:
        item["time"] = format_time_short(item.get("timestamp"), lang)

    return {
        "language": lang,
        "session_count": len(files),
        "files_inspected": [str(path) for path in files],
        "repo_roots": repo_roots,
        "workspaces": unique_cwds,
        "workspace_summaries": workspace_summaries,
        "inspected_artifacts": unique_files,
        "raw_candidate_counts": dict(raw_counts),
        "activities": normalized,
        "timeline": timeline,
    }


def apply_max_items(payload: dict, max_items: int) -> dict:
    if max_items <= 0:
        return payload

    limited = dict(payload)
    limited["activities"] = payload.get("activities", [])[:max_items]
    limited["timeline"] = payload.get("timeline", [])[:max_items]

    remaining = max_items
    workspace_summaries = []
    for workspace in payload.get("workspace_summaries", []):
        if remaining <= 0:
            break
        items = workspace.get("activities", [])[:remaining]
        remaining -= len(items)
        workspace_summaries.append(
            {
                **workspace,
                "activity_count": len(items),
                "activities": items,
            }
        )
    limited["workspace_summaries"] = workspace_summaries
    return limited


def render_summary_markdown(date_str: str, summary: dict, max_items: int, lang: str) -> str:
    workspace_summaries = summary.get("workspace_summaries") or []
    activities = summary.get("activities") or []
    if not activities:
        return get_text(lang, "no_activity", date=date_str)

    lines = [get_text(lang, "summary_header", date=date_str)]
    if not workspace_summaries:
        items = activities[:max_items] if max_items > 0 else activities
        for idx, item in enumerate(items, start=1):
            lines.append(f"{idx}. {item['activity']}")
        return "\n".join(lines)

    multi_workspace = len(workspace_summaries) > 1
    remaining = max_items if max_items > 0 else None
    for workspace in workspace_summaries:
        items = workspace["activities"]
        if remaining is not None:
            if remaining <= 0:
                break
            items = items[:remaining]
            remaining -= len(items)
        if not items:
            continue

        repo_label = workspace["repo_label"] or get_text(lang, "unknown_workspace")
        workspace_path = workspace.get("workspace")
        if multi_workspace:
            lines.append(f"- {repo_label} ({workspace_path})" if workspace_path else f"- {repo_label}")
            for item in items:
                lines.append(f"  - {item['activity']}")
            continue

        if workspace_path:
            lines.append(get_text(lang, "workspace_label", repo_label=repo_label, workspace_path=workspace_path))
        else:
            lines.append(get_text(lang, "workspace_label_no_path", repo_label=repo_label))
        for idx, item in enumerate(items, start=1):
            lines.append(f"{idx}. {item['activity']}")
    return "\n".join(lines)


def render_workspace_markdown(date_str: str, summary: dict, max_items: int, lang: str) -> str:
    workspace_summaries = summary.get("workspace_summaries") or []
    if not workspace_summaries:
        return get_text(lang, "no_activity", date=date_str)

    lines = [get_text(lang, "workspace_header", date=date_str)]
    remaining = max_items if max_items > 0 else None
    for workspace in workspace_summaries:
        items = workspace.get("activities", [])
        if remaining is not None:
            if remaining <= 0:
                break
            items = items[:remaining]
            remaining -= len(items)
        if not items:
            continue
        repo_label = workspace.get("repo_label") or get_text(lang, "unknown_workspace")
        workspace_path = workspace.get("workspace")
        lines.append("")
        lines.append(f"**`{repo_label}`**")
        if workspace_path:
            lines.append(f"`{workspace_path}`")
        for item in items:
            lines.append(f"- {item['activity']}")
    return "\n".join(lines)


def render_timeline_markdown(date_str: str, summary: dict, max_items: int, lang: str) -> str:
    timeline = summary.get("timeline") or []
    if not timeline:
        return get_text(lang, "no_activity", date=date_str)

    items = timeline[:max_items] if max_items > 0 else timeline
    repo_roots = summary.get("repo_roots") or []
    lines = [get_text(lang, "timeline_header", date=date_str)]
    for idx, item in enumerate(items, start=1):
        cwd = item.get("cwd")
        repo_root = match_repo_root(cwd, repo_roots)
        repo_label = derive_workspace_label(repo_root) if repo_root else derive_workspace_label(cwd)
        repo_label = repo_label or get_text(lang, "unknown_workspace")
        lines.append(
            f"{idx}. "
            + get_text(
                lang,
                "timeline_item",
                time=format_time_short(item.get("timestamp"), lang),
                repo_label=repo_label,
                activity=item["activity"],
            )
        )
    return "\n".join(lines)


def render_markdown(date_str: str, summary: dict, max_items: int, lang: str, view: str) -> str:
    if view == "timeline":
        return render_timeline_markdown(date_str, summary, max_items, lang)
    if view == "summary":
        return render_summary_markdown(date_str, summary, max_items, lang)
    return render_workspace_markdown(date_str, summary, max_items, lang)


def main() -> int:
    args = parse_args()
    lang = resolve_language(args.lang, args.user_text)
    repo_roots = discover_repo_roots(args.repo_search_root) if args.discover_git_repos and args.repo_search_root else []
    files = get_session_files(Path(args.sessions_root).expanduser(), args.date)
    if not files:
        payload = {
            "language": lang,
            "view": args.view,
            "date": args.date,
            "session_count": 0,
            "files_inspected": [],
            "repo_roots": repo_roots,
            "workspaces": [],
            "workspace_summaries": [],
            "inspected_artifacts": [],
            "raw_candidate_counts": {},
            "activities": [],
            "timeline": [],
            "message": get_text(lang, "no_sessions", date=args.date),
        }
    else:
        payload = summarize_day(files, lang, repo_roots)
        payload["date"] = args.date
        payload["view"] = args.view

    rendered_payload = apply_max_items(payload, args.max_items)
    if args.format == "markdown":
        print(render_markdown(args.date, rendered_payload, args.max_items, lang, args.view))
    else:
        print(json.dumps(rendered_payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
