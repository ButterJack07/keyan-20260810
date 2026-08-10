#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONL 表格编辑器
用法:
    python jsonl_editor.py [data.jsonl] [--port 8787]
启动后在浏览器中打开 http://localhost:8787
"""
import argparse
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JSONL 表格编辑器</title>
<style>
:root{ --border:#d0d7de; --headbg:#f6f8fa; --accent:#0969da; --errbg:#ffebe9; --err:#cf222e; }
*{box-sizing:border-box}
body{font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;margin:0;color:#1f2328;background:#fff}
header{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid var(--border);padding:10px 16px;box-shadow:0 1px 4px rgba(0,0,0,.04)}
h1{font-size:18px;margin:0 0 8px}
.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:13px}
.toolbar button,.toolbar select,.toolbar input{border:1px solid var(--border);background:#fff;border-radius:6px;padding:5px 10px;font-size:13px;cursor:pointer;font-family:inherit}
.toolbar button:hover{background:var(--headbg)}
.toolbar button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.toolbar button.primary:hover{background:#0550ae}
.toolbar input{width:220px;cursor:text}
#status{font-size:12px;color:#57606a;margin-top:4px}
#banner{position:sticky;top:0;z-index:9;background:#fff8c5;border-bottom:1px solid #d4a72c;padding:8px 16px;font-size:13px}
#banner button{margin-left:8px;border:1px solid #d4a72c;border-radius:6px;background:#fff;padding:3px 10px;cursor:pointer}
#tablewrap{overflow:auto;padding:16px;height:calc(100vh - 130px)}
table{border-collapse:collapse;font-size:13px;min-width:100%}
th,td{border:1px solid var(--border);padding:6px 8px;vertical-align:top}
th{background:var(--headbg);position:sticky;top:0;z-index:2;text-align:left;white-space:nowrap}
th .colpath{font-family:ui-monospace,Consolas,"Microsoft YaHei",monospace;font-size:12px}
.colpath.expandable{color:var(--accent);cursor:pointer}
.colpath.expandable:hover{text-decoration:underline}
.collapsebtn{margin-left:6px;border:none;background:#eaeef2;border-radius:4px;cursor:pointer;font-size:11px;padding:1px 6px;color:#57606a}
.collapsebtn:hover{background:#d0d7de}
td.rownum,td.actions{text-align:center;white-space:nowrap;color:#57606a;background:#fafbfc;width:30px}
td.cell{max-width:520px;min-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer;font-family:ui-monospace,Consolas,"Microsoft YaHei",monospace;font-size:12px}
td.cell.open{white-space:normal;overflow:visible;text-overflow:clip;word-break:break-word}
td.cell.empty{color:#999;font-style:italic}
td.cell.editing{cursor:text;padding:2px;white-space:normal;overflow:visible}
td.cell.editing textarea,td.cell.editing input{width:100%;border:2px solid var(--accent);border-radius:4px;font-family:inherit;font-size:12px;resize:vertical;background:#fff}
tr.invalid td{background:var(--errbg)}
.invalbox .err{color:var(--err);font-size:12px;margin-bottom:4px;word-break:break-all}
.invalbox textarea{width:100%;border:1px solid var(--border);border-radius:4px;font-family:ui-monospace,Consolas,monospace;font-size:12px;min-height:70px;padding:4px}
.actions button{border:none;background:none;cursor:pointer;font-size:14px;color:#57606a;padding:2px}
.actions button:hover{color:#cf222e}
tr:hover td{background:#f6f8fa}
#help{font-size:12px;color:#57606a;margin-top:6px;line-height:1.7}
.kbd{background:#eaeef2;border:1px solid #d0d7de;border-radius:4px;padding:0 4px;font-family:ui-monospace,monospace}
</style>
</head>
<body>
<header>
<h1>JSONL 表格编辑器</h1>
<div class="toolbar">
  <select id="fileSel"></select>
  <button id="loadBtn">加载</button>
  <span id="curFile"></span>
  <span style="flex:1"></span>
  <button id="addBtn" class="primary">＋ 新增行</button>
  <button id="foldBtn">全部折叠</button>
  <input id="savePath" placeholder="服务器保存路径" title="保存到服务器的路径（相对当前目录）">
  <button id="saveSrv">保存到服务器</button>
  <button id="copyBtn">复制全部</button>
  <button id="dlBtn">下载 .jsonl</button>
</div>
<div id="status"></div>
<div id="help">提示：<span class="kbd">双击</span>编辑单元格，<span class="kbd">Enter</span> 提交并移到下一行，<span class="kbd">Ctrl+Enter</span> 提交多行文本，<span class="kbd">Esc</span> 取消；<span class="kbd">点击列名</span>展开嵌套列（父.子 作为新列），<span class="kbd">«</span> 折叠回父级；<span class="kbd">单击</span>单元格可展开/收起查看完整内容；编辑过程自动保存草稿。</div>
</header>
<div id="banner" hidden></div>
<div id="tablewrap"></div>
<script>
"use strict";
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const DRAFT_KEY = "jsonlEditor.draft";

const S = {
  rows: [],
  columns: [],
  expanded: [],          // array of paths (each path = array of key segments)
  fileName: null,
};

/* ---------- path helpers ---------- */
const isObj = v => v && typeof v === "object" && !Array.isArray(v);
const isArr = v => Array.isArray(v);
const segKey = seg => /^\d+$/.test(seg) ? Number(seg) : seg;

function valueAt(obj, path) {
  let cur = obj;
  for (const seg of path) {
    if (cur == null) return undefined;
    cur = cur[segKey(seg)];
  }
  return cur;
}
function setAt(obj, path, val) {
  let cur = obj;
  for (let i = 0; i < path.length - 1; i++) {
    const k = segKey(path[i]);
    if (!isObj(cur[k]) && !isArr(cur[k])) cur[k] = {};
    cur = cur[k];
  }
  cur[segKey(path[path.length - 1])] = val;
}
function pathsEqual(a, b) {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}
function isAncestor(parent, child) {
  if (parent.length >= child.length) return false;
  for (let i = 0; i < parent.length; i++) if (parent[i] !== child[i]) return false;
  return true;
}
function hasPath(expanded, path) { return expanded.some(e => pathsEqual(e, path)); }

function displayVal(v) {
  if (v === undefined || v === null) return "";
  if (typeof v === "string") return v;
  return JSON.stringify(v);
}

/* ---------- structure discovery ---------- */
function topLevelChildren() {
  const objs = S.rows.filter(r => r.valid).map(r => r.obj);
  if (!objs.length) return [];
  if (objs.every(isObj)) {
    const keys = [], seen = new Set();
    for (const o of objs) for (const k of Object.keys(o)) if (!seen.has(k)) { seen.add(k); keys.push(k); }
    return keys.map(k => [k]);
  }
  if (objs.every(isArr)) {
    const mx = Math.max(0, ...objs.map(a => a.length));
    return Array.from({ length: mx }, (_, i) => [String(i)]);
  }
  return [];
}
function childPaths(path) {
  const vals = [];
  for (const r of S.rows) {
    if (!r.valid) continue;
    const v = valueAt(r.obj, path);
    if (v !== undefined) vals.push(v);
  }
  if (!vals.length) return null;
  if (vals.every(isObj)) {
    const keys = [], seen = new Set();
    for (const o of vals) for (const k of Object.keys(o)) if (!seen.has(k)) { seen.add(k); keys.push(k); }
    if (!keys.length) return null;
    return keys.map(k => [...path, k]);
  }
  if (vals.every(isArr)) {
    const mx = Math.max(0, ...vals.map(a => a.length));
    if (!mx) return null;
    return Array.from({ length: mx }, (_, i) => [...path, String(i)]);
  }
  return null;
}
function recomputeColumns() {
  const out = [];
  const walk = p => {
    if (hasPath(S.expanded, p)) {
      const kids = childPaths(p);
      if (kids && kids.length) { for (const c of kids) walk(c); return; }
    }
    out.push(p);
  };
  for (const c of topLevelChildren()) walk(c);
  S.columns = out;
}
function autoExpand() {
  S.expanded = [];
  const walk = p => {
    const kids = childPaths(p);
    if (kids && kids.length) {
      S.expanded.push(p);
      for (const c of kids) walk(c);
    }
  };
  for (const c of topLevelChildren()) walk(c);
  recomputeColumns();
}

/* ---------- editing ---------- */
function toValue(input, cur) {
  const s = input.trim();
  if (s === "") return null;
  if (cur && typeof cur === "string") {
    if (s.startsWith("{") || s.startsWith("[")) { try { return JSON.parse(s); } catch (e) { return input; } }
    return input;
  }
  try { return JSON.parse(s); } catch (e) { return input; }
}

function startEdit(td) {
  if (td.classList.contains("editing")) return;
  const path = JSON.parse(td.dataset.path);
  let cur = null;
  if (td.dataset.raw !== "") { try { cur = JSON.parse(td.dataset.raw); } catch (e) {} }
  const isLong = typeof cur === "string" && (cur.includes("\n") || cur.length > 120);
  td.classList.add("editing");
  td.innerHTML = "";
  const commit = text => {
    if (td.dataset.done) return;
    td.dataset.done = "1";
    const v = toValue(text, cur);
    const ri = +td.dataset.ri, ci = +td.dataset.ci;
    const row = S.rows[ri];
    if (row) setAt(row.obj, path, v);
    recomputeColumns();
    render();
    const next = document.querySelector('td.cell[data-ri="' + (ri + 1) + '"][data-ci="' + ci + '"]');
    if (next) startEdit(next);
  };
  const cancel = () => {
    if (td.dataset.done) return;
    td.dataset.done = "1";
    render();
  };
  if (isLong) {
    const ta = document.createElement("textarea");
    ta.value = cur || "";
    ta.addEventListener("keydown", e => {
      if (e.key === "Enter" && e.ctrlKey) { e.preventDefault(); commit(ta.value); }
      else if (e.key === "Escape") { e.preventDefault(); cancel(); }
    });
    ta.addEventListener("blur", () => commit(ta.value));
    td.appendChild(ta);
    ta.focus();
  } else {
    const inp = document.createElement("input");
    inp.type = "text";
    inp.value = displayVal(cur);
    inp.addEventListener("keydown", e => {
      if (e.key === "Enter") { e.preventDefault(); commit(inp.value); }
      else if (e.key === "Escape") { e.preventDefault(); cancel(); }
    });
    inp.addEventListener("blur", () => commit(inp.value));
    td.appendChild(inp);
    inp.focus();
  }
}

/* ---------- rendering ---------- */
function buildText() {
  const parts = [];
  for (const r of S.rows) {
    if (r.valid) parts.push(JSON.stringify(r.obj));
    else parts.push(r.raw || "");
  }
  return parts.join("\n") + (parts.length ? "\n" : "");
}

function render() {
  recomputeColumns();
  const N = S.columns.length;
  const parentExp = p => p.length > 1 && hasPath(S.expanded, p.slice(0, -1));

  let head = "<tr><th class='rownum'>#</th>";
  S.columns.forEach((c, ci) => {
    const expandable = childPaths(c) !== null;
    const pathText = c.join(".");
    const coll = parentExp(c) ? "<button class='collapsebtn' data-collapse='" + ci + "' title='折叠回上级'>«</button>" : "";
    head += "<th title='" + esc(pathText) + "'><span class='colpath" + (expandable ? " expandable" : "") + "' data-expand='" + ci + "'>" + (expandable ? "▸ " : "") + esc(pathText) + "</span>" + coll + "</th>";
  });
  head += "<th class='rownum'>操作</th></tr>";

  let body = "";
  S.rows.forEach((row, i) => {
    if (!row.valid) {
      body += "<tr class='invalid'><td class='rownum'>" + (i + 1) + "</td>"
        + "<td colspan='" + (N + 1) + "'><div class='invalbox'>"
        + "<div class='err'>第 " + (i + 1) + " 行不是有效 JSON：" + esc(row.error || "") + "</div>"
        + "<textarea data-inv='" + i + "'>" + esc(row.raw || "") + "</textarea>"
        + "</div></td></tr>";
      return;
    }
    let cells = "";
    S.columns.forEach((c, ci) => {
      const v = valueAt(row.obj, c);
      const undef = v === undefined;
      const raw = undef ? "" : JSON.stringify(v);
      cells += "<td class='cell" + (undef ? " empty" : "") + "' data-path='" + esc(JSON.stringify(c)) + "' data-raw='" + esc(raw) + "' data-ri='" + i + "' data-ci='" + ci + "' title='" + esc(undef ? "(空)" : displayVal(v)) + "'>" + (undef ? "" : esc(displayVal(v))) + "</td>";
    });
    body += "<tr><td class='rownum'>" + (i + 1) + "</td>" + cells
      + "<td class='actions'><button class='dup' data-i='" + i + "' title='复制该行'>⧉</button><button class='del' data-i='" + i + "' title='删除该行'>🗑</button></td></tr>";
  });

  $("tablewrap").innerHTML = "<table>" + head + body + "</table>";

  const validCount = S.rows.filter(r => r.valid).length;
  const badCount = S.rows.length - validCount;
  $("status").textContent = "共 " + S.rows.length + " 行" + (badCount ? "，其中 " + badCount + " 行格式错误" : "") + (S.fileName ? "；当前文件：" + S.fileName : "");
  scheduleDraft();
}

/* ---------- events (delegated) ---------- */
$("tablewrap").addEventListener("click", e => {
  const ex = e.target.closest("[data-expand]");
  if (ex) {
    const p = S.columns[+ex.dataset.expand];
    if (!hasPath(S.expanded, p)) S.expanded.push(p);
    render();
    return;
  }
  const co = e.target.closest("[data-collapse]");
  if (co) {
    const p = S.columns[+co.dataset.collapse].slice(0, -1);
    S.expanded = S.expanded.filter(x => !(pathsEqual(x, p) || isAncestor(p, x)));
    render();
    return;
  }
  const dup = e.target.closest(".dup");
  if (dup) {
    const i = +dup.dataset.i;
    const copy = JSON.parse(JSON.stringify(S.rows[i]));
    S.rows.splice(i + 1, 0, copy);
    render();
    return;
  }
  const del = e.target.closest(".del");
  if (del) {
    const i = +del.dataset.i;
    if (!confirm("确定删除第 " + (i + 1) + " 行？")) return;
    S.rows.splice(i, 1);
    render();
    return;
  }
  const cell = e.target.closest("td.cell");
  if (cell && !cell.classList.contains("editing")) {
    if (e.target.closest("textarea") || e.target.closest("input")) return;
    cell.classList.toggle("open");
  }
});
$("tablewrap").addEventListener("dblclick", e => {
  const cell = e.target.closest("td.cell");
  if (cell) startEdit(cell);
});
$("tablewrap").addEventListener("input", e => {
  const ta = e.target.closest("textarea[data-inv]");
  if (!ta) return;
  const i = +ta.dataset.inv;
  const text = ta.value;
  try {
    const obj = JSON.parse(text);
    S.rows[i] = { valid: true, obj: obj };
    render();
  } catch (err) {
    S.rows[i] = { valid: false, raw: text, error: err.message };
    let box = ta.closest(".invalbox");
    if (box) {
      let er = box.querySelector(".err");
      if (!er) { er = document.createElement("div"); er.className = "err"; box.insertBefore(er, ta); }
      er.textContent = "第 " + (i + 1) + " 行不是有效 JSON：" + err.message;
    }
  }
});

/* ---------- toolbar ---------- */
$("addBtn").addEventListener("click", () => {
  S.rows.push({ valid: true, obj: {} });
  render();
});
$("foldBtn").addEventListener("click", () => {
  S.expanded = [];
  render();
});

async function refreshFiles() {
  const res = await fetch("/api/files");
  const list = (await res.json()).files || [];
  const sel = $("fileSel");
  sel.innerHTML = "";
  list.forEach(f => {
    const o = document.createElement("option");
    o.value = f.path;
    o.textContent = f.name;
    sel.appendChild(o);
  });
  if (S.fileName) {
    const hit = list.find(f => f.path === S.fileName);
    if (hit) sel.value = hit.path;
  }
  if (list.length === 0) {
    const o = document.createElement("option");
    o.value = "";
    o.textContent = "（未找到 .jsonl 文件）";
    sel.appendChild(o);
  }
}
$("loadBtn").addEventListener("click", async () => {
  const path = $("fileSel").value;
  if (!path) return;
  await loadFile(path);
});

async function loadFile(path) {
  const res = await fetch("/api/load?path=" + encodeURIComponent(path));
  if (!res.ok) { alert("加载失败：" + (await res.text())); return; }
  const data = await res.json();
  S.rows = data.rows;
  S.fileName = data.path;
  autoExpand();
  $("savePath").value = data.path;
  render();
  checkDraft();
}
$("saveSrv").addEventListener("click", async () => {
  const path = $("savePath").value.trim();
  if (!path) { alert("请填写保存路径"); return; }
  if (!confirm("将覆盖服务器文件：" + path + "，继续？")) return;
  const res = await fetch("/api/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: path, rows: S.rows })
  });
  const data = await res.json();
  if (res.ok) {
    S.fileName = data.path;
    $("status").textContent = "已保存到服务器：" + data.path + "（" + data.count + " 行）";
    clearDraft();
    refreshFiles();
  } else {
    alert("保存失败：" + data.error);
  }
});
$("copyBtn").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(buildText());
    $("status").textContent = "已复制全部内容到剪贴板";
  } catch (e) {
    const ta = document.createElement("textarea");
    ta.value = buildText();
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
    $("status").textContent = "已复制全部内容到剪贴板";
  }
});
$("dlBtn").addEventListener("click", () => {
  const name = (S.fileName || "edited").replace(/\\/g, "/").split("/").pop() || "edited.jsonl";
  const blob = new Blob([buildText()], { type: "application/x-ndjson;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(a.href);
});

/* ---------- draft ---------- */
function scheduleDraft() {
  clearTimeout(scheduleDraft._t);
  scheduleDraft._t = setTimeout(() => {
    const d = { ts: Date.now(), fileName: S.fileName, rows: S.rows };
    try { localStorage.setItem(DRAFT_KEY, JSON.stringify(d)); } catch (e) {}
  }, 800);
}
function clearDraft() {
  try { localStorage.removeItem(DRAFT_KEY); } catch (e) {}
}
function checkDraft() {
  let d = null;
  try { d = JSON.parse(localStorage.getItem(DRAFT_KEY) || "null"); } catch (e) {}
  if (!d || !d.rows) return;
  const banner = $("banner");
  const t = new Date(d.ts);
  banner.innerHTML = "发现未保存草稿（保存于 " + t.toLocaleString() + (d.fileName ? "，文件：" + d.fileName : "") + "）。"
    + "<button id='draftRestore'>恢复草稿</button><button id='draftDiscard'>丢弃</button>";
  banner.hidden = false;
  $("draftRestore").onclick = () => {
    S.rows = d.rows;
    S.expanded = [];
    if (d.fileName) { S.fileName = d.fileName; $("savePath").value = d.fileName; }
    banner.hidden = true;
    recomputeColumns();
    render();
  };
  $("draftDiscard").onclick = () => { clearDraft(); banner.hidden = true; };
}

/* ---------- boot ---------- */
async function boot() {
  await refreshFiles();
  const sel = $("fileSel");
  if (sel.value) await loadFile(sel.value);
  else { render(); }
}
boot();
</script>
</body>
</html>
"""

# ---------------------------------------------------------------- server ---

def parse_jsonl(text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            rows.append({"valid": True, "obj": json.loads(line)})
        except Exception as exc:
            rows.append({"valid": False, "raw": line, "error": str(exc)})
    return rows


def build_jsonl(rows):
    parts = []
    for r in rows:
        if r.get("valid"):
            parts.append(json.dumps(r.get("obj", {}), ensure_ascii=False))
        else:
            parts.append(r.get("raw", ""))
    text = "\n".join(parts)
    return text + "\n" if text else ""


class Handler(BaseHTTPRequestHandler):
    base_dir = None

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _resolve(self, rel):
        if not rel:
            return None
        base = os.path.realpath(self.base_dir)
        p = os.path.realpath(os.path.join(base, rel))
        if not (p == base or p.startswith(base + os.sep)):
            return None
        return p

    def _list_files(self):
        found = []
        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for fn in files:
                if fn.lower().endswith(".jsonl"):
                    full = os.path.join(root, fn)
                    rel = os.path.relpath(full, self.base_dir)
                    found.append({"name": rel, "path": rel.replace(os.sep, "/")})
        found.sort(key=lambda x: x["path"])
        return found

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        qs = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        if path in ("/", "/index.html"):
            self._send(200, HTML, "text/html; charset=utf-8")
            return
        if path == "/api/files":
            self._send(200, {"files": self._list_files()})
            return
        if path == "/api/load":
            rel = qs.get("path", "")
            full = self._resolve(rel)
            if not full or not os.path.isfile(full):
                self._send(404, {"error": "文件不存在或路径越界"})
                return
            try:
                with open(full, "r", encoding="utf-8-sig") as f:
                    rows = parse_jsonl(f.read())
                self._send(200, {"rows": rows, "path": rel.replace(os.sep, "/")})
            except Exception as exc:
                self._send(500, {"error": str(exc)})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path != "/api/save":
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            rel = payload.get("path", "")
            rows = payload.get("rows", [])
            full = self._resolve(rel)
            if not full:
                self._send(400, {"error": "路径越界"})
                return
            os.makedirs(os.path.dirname(full), exist_ok=True)
            text = build_jsonl(rows)
            with open(full, "w", encoding="utf-8") as f:
                f.write(text)
            self._send(200, {"ok": True, "path": rel.replace(os.sep, "/"), "count": len(rows)})
        except Exception as exc:
            self._send(500, {"error": str(exc)})

    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser(description="JSONL 表格编辑器")
    ap.add_argument("file", nargs="?", default=None, help="初始打开的 .jsonl 文件路径")
    ap.add_argument("--port", type=int, default=8787, help="端口号（默认 8787）")
    args = ap.parse_args()

    if args.file:
        base = os.path.dirname(os.path.abspath(args.file)) or os.getcwd()
        if not os.path.isfile(args.file):
            print("警告：文件不存在 " + args.file)
    else:
        base = os.getcwd()
    Handler.base_dir = base

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    url = "http://127.0.0.1:%d" % args.port
    print("JSONL 表格编辑器已启动: %s" % url)
    print("数据目录: %s" % base)
    if args.file:
        print("初始文件: %s" % os.path.abspath(args.file))
    print("按 Ctrl+C 停止。")

    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
        server.server_close()


if __name__ == "__main__":
    sys.exit(main())
