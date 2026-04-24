#!/usr/bin/env python3

import argparse
import copy
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

ET.register_namespace("", MAIN_NS)
ET.register_namespace("r", REL_NS)


def qn(ns, tag):
    return f"{{{ns}}}{tag}"


def letters_to_index(letters):
    index = 0
    for char in letters:
        index = index * 26 + (ord(char.upper()) - 64)
    return index - 1


def col_letter(index):
    result = ""
    value = index + 1
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(65 + remainder) + result
    return result


def cell_ref_parts(cell_ref):
    match = re.match(r"([A-Z]+)(\d+)", cell_ref)
    if not match:
        raise ValueError(f"Invalid cell reference: {cell_ref}")
    return match.group(1), int(match.group(2))


class SharedStrings:
    def __init__(self, path):
        self.path = Path(path)
        if self.path.exists():
            self.tree = ET.parse(self.path)
            self.root = self.tree.getroot()
        else:
            self.root = ET.Element(qn(MAIN_NS, "sst"), {"count": "0", "uniqueCount": "0"})
            self.tree = ET.ElementTree(self.root)
        self.values = []
        self.lookup = {}
        for idx, si in enumerate(self.root.findall(qn(MAIN_NS, "si"))):
            text = "".join(node.text or "" for node in si.iterfind(f".//{qn(MAIN_NS, 't')}"))
            self.values.append(text)
            if text not in self.lookup:
                self.lookup[text] = idx

    def add(self, value):
        text = "" if value is None else str(value)
        if text in self.lookup:
            return self.lookup[text]
        idx = len(self.values)
        si = ET.Element(qn(MAIN_NS, "si"))
        t = ET.SubElement(si, qn(MAIN_NS, "t"))
        if text.strip() != text or "\n" in text:
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = text
        self.root.append(si)
        self.values.append(text)
        self.lookup[text] = idx
        return idx

    def save(self):
        count = len(self.values)
        self.root.set("count", str(count))
        self.root.set("uniqueCount", str(count))
        self.tree.write(self.path, encoding="utf-8", xml_declaration=True)


class WorkbookEditor:
    def __init__(self, workbook_dir):
        self.workbook_dir = Path(workbook_dir)
        self.xl_dir = self.workbook_dir / "xl"
        self.workbook_path = self.xl_dir / "workbook.xml"
        self.workbook_rels_path = self.xl_dir / "_rels" / "workbook.xml.rels"
        self.content_types_path = self.workbook_dir / "[Content_Types].xml"
        self.shared_strings = SharedStrings(self.xl_dir / "sharedStrings.xml")

        self.workbook_tree = ET.parse(self.workbook_path)
        self.workbook_root = self.workbook_tree.getroot()
        self.rels_tree = ET.parse(self.workbook_rels_path)
        self.rels_root = self.rels_tree.getroot()
        self.content_types_tree = ET.parse(self.content_types_path)
        self.content_types_root = self.content_types_tree.getroot()

        self.sheets_parent = self.workbook_root.find(qn(MAIN_NS, "sheets"))
        self.sheet_entries = list(self.sheets_parent.findall(qn(MAIN_NS, "sheet")))
        self.rel_targets = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in self.rels_root.findall(qn(PKG_REL_NS, "Relationship"))
        }

    def save(self):
        self.shared_strings.save()
        self.workbook_tree.write(self.workbook_path, encoding="utf-8", xml_declaration=True)
        self.rels_tree.write(self.workbook_rels_path, encoding="utf-8", xml_declaration=True)
        self.content_types_tree.write(self.content_types_path, encoding="utf-8", xml_declaration=True)

    def get_sheet_by_name(self, name):
        for sheet in self.sheets_parent.findall(qn(MAIN_NS, "sheet")):
            if sheet.attrib.get("name") == name:
                return sheet
        return None

    def get_sheet_path(self, sheet):
        rel_id = sheet.attrib[qn(REL_NS, "id")]
        target = self.rel_targets[rel_id]
        return self.xl_dir / target

    def load_sheet_tree(self, sheet):
        path = self.get_sheet_path(sheet)
        return ET.parse(path), path

    def remove_sheet(self, sheet_name):
        sheet = self.get_sheet_by_name(sheet_name)
        if sheet is not None:
            self.sheets_parent.remove(sheet)

    def set_sheet_name(self, old_name, new_name):
        sheet = self.get_sheet_by_name(old_name)
        if sheet is None:
            raise ValueError(f"Sheet not found: {old_name}")
        sheet.set("name", sanitize_sheet_name(new_name))
        return sheet

    def next_sheet_id(self):
        sheet_ids = [int(sheet.attrib["sheetId"]) for sheet in self.sheets_parent.findall(qn(MAIN_NS, "sheet"))]
        return max(sheet_ids, default=0) + 1

    def next_sheet_file_name(self):
        worksheet_dir = self.xl_dir / "worksheets"
        existing = []
        for path in worksheet_dir.glob("sheet*.xml"):
            match = re.match(r"sheet(\d+)\.xml$", path.name)
            if match:
                existing.append(int(match.group(1)))
        return f"worksheets/sheet{max(existing, default=0) + 1}.xml"

    def next_relationship_id(self):
        values = []
        for rel in self.rels_root.findall(qn(PKG_REL_NS, "Relationship")):
            match = re.match(r"rId(\d+)$", rel.attrib.get("Id", ""))
            if match:
                values.append(int(match.group(1)))
        return f"rId{max(values, default=0) + 1}"

    def ensure_content_type(self, part_name):
        part_name = "/" + part_name.lstrip("/")
        for override in self.content_types_root.findall(qn(CT_NS, "Override")):
            if override.attrib.get("PartName") == part_name:
                return
        ET.SubElement(
            self.content_types_root,
            qn(CT_NS, "Override"),
            {
                "PartName": part_name,
                "ContentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml",
            },
        )

    def clone_sheet(self, source_name, new_name):
        source_sheet = self.get_sheet_by_name(source_name)
        if source_sheet is None:
            raise ValueError(f"Source sheet not found: {source_name}")

        source_tree, source_path = self.load_sheet_tree(source_sheet)
        new_target = self.next_sheet_file_name()
        new_path = self.xl_dir / new_target
        new_path.write_bytes(source_path.read_bytes())

        rel_id = self.next_relationship_id()
        ET.SubElement(
            self.rels_root,
            qn(PKG_REL_NS, "Relationship"),
            {
                "Id": rel_id,
                "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet",
                "Target": new_target,
            },
        )
        self.rel_targets[rel_id] = new_target

        new_sheet = copy.deepcopy(source_sheet)
        new_sheet.set("name", sanitize_sheet_name(new_name))
        new_sheet.set("sheetId", str(self.next_sheet_id()))
        new_sheet.set(qn(REL_NS, "id"), rel_id)
        self.sheets_parent.append(new_sheet)
        self.ensure_content_type(new_target)
        return new_sheet


def sanitize_sheet_name(name):
    sanitized = re.sub(r"[:\\\\/?*\\[\\]]", " ", (name or "Sheet").strip())
    sanitized = re.sub(r"\\s+", " ", sanitized).strip()
    return sanitized[:31] or "Sheet"


def normalize_rows(payload):
    roles = payload.get("roles") or []
    normalized_roles = []
    jira_key = payload["jira_key"]
    for role_index, role_entry in enumerate(roles, start=1):
        role_name = role_entry.get("role") or f"Role {role_index}"
        sprint = role_entry.get("sprint", "")
        cases = []
        for case_index, case in enumerate(role_entry.get("test_cases") or [], start=1):
            feature_suite = case.get("feature_suite") or payload.get("story_title", "")
            tc_id = case.get("tc_id") or build_tc_id(jira_key, role_name, case_index)
            cases.append(
                {
                    "sprint": sprint,
                    "tc_id": tc_id,
                    "link_story": payload["jira_url"],
                    "feature_suite": feature_suite,
                    "role_user": role_name,
                    "platform": case.get("platform") or payload.get("platform") or "Web CMS",
                    "test_case": case.get("test_case", ""),
                    "preconditions": join_lines(case.get("preconditions")),
                    "steps": join_lines(case.get("steps")),
                    "data": join_lines(case.get("data")),
                    "expected": join_lines(case.get("expected")),
                    "behaviour": case.get("behaviour", "Positive"),
                    "priority": case.get("priority", "Medium"),
                    "severity": case.get("severity", "Normal"),
                    "complexity": case.get("complexity", "Medium"),
                    "type": case.get("type", "Functional"),
                }
            )
        normalized_roles.append({"role": role_name, "test_cases": cases})
    return normalized_roles


def join_lines(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return "\n".join(str(item) for item in value if item is not None)
    return str(value)


def build_tc_id(jira_key, role_name, index):
    role_code = "".join(part[:1].upper() for part in re.findall(r"[A-Za-z0-9]+", role_name)) or "R"
    return f"{jira_key}-{role_code}-{index:02d}"


def template_row_styles(sheet_root, row_number):
    sheet_data = sheet_root.find(qn(MAIN_NS, "sheetData"))
    for row in sheet_data.findall(qn(MAIN_NS, "row")):
        if row.attrib.get("r") == str(row_number):
            styles = {}
            for cell in row.findall(qn(MAIN_NS, "c")):
                col, _ = cell_ref_parts(cell.attrib["r"])
                styles[col] = cell.attrib.get("s")
            return styles
    return {}


def build_string_cell(shared_strings, column_index, row_number, style_id, text):
    attrs = {"r": f"{col_letter(column_index)}{row_number}"}
    if style_id is not None:
        attrs["s"] = style_id
    if text:
        attrs["t"] = "s"
    cell = ET.Element(qn(MAIN_NS, "c"), attrs)
    if text:
        value = ET.SubElement(cell, qn(MAIN_NS, "v"))
        value.text = str(shared_strings.add(text))
    return cell


def rewrite_testcase_sheet(editor, sheet_name, role_entry):
    sheet = editor.get_sheet_by_name(sheet_name)
    if sheet is None:
        raise ValueError(f"Sheet not found: {sheet_name}")
    sheet_tree, sheet_path = editor.load_sheet_tree(sheet)
    root = sheet_tree.getroot()
    sheet_data = root.find(qn(MAIN_NS, "sheetData"))
    rows = sheet_data.findall(qn(MAIN_NS, "row"))
    if not rows:
        raise ValueError(f"Sheet has no rows: {sheet_name}")

    header_row = copy.deepcopy(rows[0])
    style_source = template_row_styles(root, 2) or template_row_styles(root, 3)
    sheet_data.clear()
    header_row.set("r", "1")
    for cell in header_row.findall(qn(MAIN_NS, "c")):
        col, _ = cell_ref_parts(cell.attrib["r"])
        cell.set("r", f"{col}1")
    sheet_data.append(header_row)

    for row_index, case in enumerate(role_entry["test_cases"], start=2):
        row = ET.Element(qn(MAIN_NS, "row"), {"r": str(row_index), "spans": "1:24"})
        values = [
            str(row_index - 1),
            case["sprint"],
            case["tc_id"],
            case["link_story"],
            case["feature_suite"],
            case["role_user"],
            case["platform"],
            case["test_case"],
            case["preconditions"],
            case["steps"],
            case["data"],
            case["expected"],
            case["behaviour"],
            case["priority"],
            case["severity"],
            case["complexity"],
            case["type"],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        for col_idx, value in enumerate(values):
            style_id = style_source.get(col_letter(col_idx))
            row.append(build_string_cell(editor.shared_strings, col_idx, row_index, style_id, value))
        sheet_data.append(row)

    last_row = max(2, len(role_entry["test_cases"]) + 1)
    dimension = root.find(qn(MAIN_NS, "dimension"))
    if dimension is not None:
        dimension.set("ref", f"A1:X{last_row}")
    auto_filter = root.find(qn(MAIN_NS, "autoFilter"))
    if auto_filter is not None:
        auto_filter.set("ref", f"A1:X{last_row}")
    sheet_tree.write(sheet_path, encoding="utf-8", xml_declaration=True)


def rewrite_summary_sheet(editor, metadata):
    sheet = editor.get_sheet_by_name("Summary")
    if sheet is None:
        return
    sheet_tree, sheet_path = editor.load_sheet_tree(sheet)
    root = sheet_tree.getroot()
    sheet_data = root.find(qn(MAIN_NS, "sheetData"))
    rows = sheet_data.findall(qn(MAIN_NS, "row"))
    header_style_map = template_row_styles(root, 1)
    value_style_map = template_row_styles(root, 2) or header_style_map
    sheet_data.clear()

    summary_rows = [
        ("Generated Test Case Workbook", ""),
        ("Jira Key", metadata.get("jira_key", "")),
        ("Story URL", metadata.get("jira_url", "")),
        ("Story Title", metadata.get("story_title", "")),
        ("Generated At", metadata.get("generated_at", "")),
        ("Platform", metadata.get("platform", "Web CMS")),
        ("Total Roles", str(metadata.get("total_roles", 0))),
        ("Total Test Cases", str(metadata.get("total_test_cases", 0))),
        ("Sheets", ", ".join(metadata.get("sheet_names", []))),
    ]

    for row_index, (label, value) in enumerate(summary_rows, start=1):
        row = ET.Element(qn(MAIN_NS, "row"), {"r": str(row_index), "spans": "1:2"})
        a_style = header_style_map.get("A")
        b_style = value_style_map.get("B")
        row.append(build_string_cell(editor.shared_strings, 0, row_index, a_style, label))
        row.append(build_string_cell(editor.shared_strings, 1, row_index, b_style, value))
        sheet_data.append(row)

    dimension = root.find(qn(MAIN_NS, "dimension"))
    if dimension is not None:
        dimension.set("ref", f"A1:B{len(summary_rows)}")
    sheet_tree.write(sheet_path, encoding="utf-8", xml_declaration=True)


def repack_directory(source_dir, output_path):
    source_dir = Path(source_dir)
    output_path = Path(output_path)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(source_dir).as_posix())


def load_payload(path):
    with open(path, "r", encoding="utf-8") as file:
        payload = json.load(file)
    required = ["jira_key", "jira_url", "story_title", "roles"]
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    return payload


def main():
    parser = argparse.ArgumentParser(description="Generate a Jira QA test-case workbook from JSON input.")
    parser.add_argument("--input-json", required=True, help="Path to the structured JSON input.")
    parser.add_argument("--output", help="Output XLSX path. Defaults to ~/Downloads/<jira_key>_test-cases.xlsx")
    args = parser.parse_args()

    payload = load_payload(args.input_json)
    template_path = Path(__file__).resolve().parent.parent / "assets" / "template.xlsx"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    default_output = Path.home() / "Downloads" / f"{payload['jira_key']}_test-cases.xlsx"
    output_path = Path(args.output).expanduser() if args.output else default_output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        working_xlsx = tmp_dir_path / "working.xlsx"
        shutil.copyfile(template_path, working_xlsx)
        unpacked_dir = tmp_dir_path / "unzipped"
        unpacked_dir.mkdir()
        with zipfile.ZipFile(working_xlsx) as zf:
            zf.extractall(unpacked_dir)

        editor = WorkbookEditor(unpacked_dir)
        roles = normalize_rows(payload)
        if not roles:
            raise ValueError("At least one role with test cases is required.")

        template_sheet_name = "Global Admin"
        existing_role_sheets = [template_sheet_name, "PIC Organization"]

        sheet_names = []
        first_role = roles[0]
        editor.set_sheet_name(template_sheet_name, first_role["role"])
        rewrite_testcase_sheet(editor, first_role["role"], first_role)
        sheet_names.append(sanitize_sheet_name(first_role["role"]))

        for stale_name in existing_role_sheets[1:]:
            editor.remove_sheet(stale_name)

        for role_entry in roles[1:]:
            new_sheet = editor.clone_sheet(sheet_names[0], role_entry["role"])
            rewrite_testcase_sheet(editor, new_sheet.attrib["name"], role_entry)
            sheet_names.append(new_sheet.attrib["name"])

        rewrite_summary_sheet(
            editor,
            {
                "jira_key": payload["jira_key"],
                "jira_url": payload["jira_url"],
                "story_title": payload["story_title"],
                "generated_at": payload.get("generated_at", ""),
                "platform": payload.get("platform", "Web CMS"),
                "total_roles": len(roles),
                "total_test_cases": sum(len(role["test_cases"]) for role in roles),
                "sheet_names": sheet_names,
            },
        )
        editor.save()
        repack_directory(unpacked_dir, output_path)

    print(output_path)


if __name__ == "__main__":
    main()
