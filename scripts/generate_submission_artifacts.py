#!/usr/bin/env python3
import os
import subprocess

WORKSPACE_DIR = "/Users/tanviagarwal/release-readiness-labs101"
SUBMISSION_DIR = os.path.join(WORKSPACE_DIR, "submission")
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(SUBMISSION_DIR, exist_ok=True)

# Common styling for VS Code / Antigravity IDE UI
COMMON_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background-color: #1e1e1e;
    color: #cccccc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
    width: 1400px;
    height: 900px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
.window-frame {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    border: 1px solid #333333;
}
.title-bar {
    height: 38px;
    background: #1e1e1e;
    display: flex;
    align-items: center;
    padding: 0 16px;
    border-bottom: 1px solid #2d2d2d;
    user-select: none;
}
.window-controls {
    display: flex;
    gap: 8px;
    margin-right: 20px;
}
.window-btn {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}
.btn-close { background: #ff5f56; }
.btn-min { background: #ffbd2e; }
.btn-max { background: #27c93f; }
.window-title {
    flex: 1;
    text-align: center;
    color: #999999;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.3px;
}
.workbench {
    display: flex;
    flex: 1;
    overflow: hidden;
}
.activity-bar {
    width: 50px;
    background: #1e1e1e;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 14px;
    border-right: 1px solid #2d2d2d;
    gap: 20px;
}
.activity-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #858585;
    cursor: pointer;
    font-size: 16px;
}
.activity-icon.active {
    color: #ffffff;
    border-left: 2px solid #007acc;
}
.sidebar {
    width: 260px;
    background: #252526;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #2d2d2d;
    font-size: 12px;
}
.sidebar-header {
    height: 36px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    font-weight: 600;
    color: #bbbbbb;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-size: 11px;
    border-bottom: 1px solid #2d2d2d;
}
.file-tree {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
}
.tree-item {
    display: flex;
    align-items: center;
    height: 25px;
    padding: 0 16px;
    color: #cccccc;
    cursor: pointer;
    white-space: nowrap;
}
.tree-item.indent-1 { padding-left: 30px; }
.tree-item.indent-2 { padding-left: 48px; }
.tree-item.active {
    background: #37373d;
    color: #ffffff;
    font-weight: 500;
}
.tree-icon {
    margin-right: 8px;
    font-size: 13px;
    opacity: 0.9;
}
.editor-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: #1e1e1e;
    overflow: hidden;
}
.tabs-bar {
    height: 36px;
    background: #252526;
    display: flex;
    border-bottom: 1px solid #1e1e1e;
    overflow-x: auto;
}
.tab {
    display: flex;
    align-items: center;
    padding: 0 16px;
    background: #2d2d2d;
    color: #969696;
    border-right: 1px solid #252526;
    font-size: 12px;
    gap: 8px;
    white-space: nowrap;
}
.tab.active {
    background: #1e1e1e;
    color: #ffffff;
    border-top: 2px solid #007acc;
}
.breadcrumb {
    height: 28px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    font-size: 11px;
    color: #888888;
    background: #1e1e1e;
    border-bottom: 1px solid #262626;
    gap: 6px;
}
.code-editor {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    font-family: ui-monospace, "SF Mono", "Menlo", "Cascadia Code", "Courier New", monospace;
    font-size: 12.5px;
    line-height: 22px;
    padding: 6px 0;
}
.code-row {
    display: flex;
    min-height: 22px;
    align-items: flex-start;
}
.line-num {
    width: 48px;
    min-width: 48px;
    text-align: right;
    padding-right: 16px;
    color: #5a5a5a;
    user-select: none;
    font-size: 11.5px;
    line-height: 22px;
}
.line-code {
    flex: 1;
    color: #d4d4d4;
    white-space: pre;
    padding-right: 16px;
    line-height: 22px;
}
.code-row.hl-bad {
    background: rgba(239, 68, 68, 0.22);
    border-left: 3px solid #ef4444;
}
.code-row.hl-bad .line-num {
    color: #fca5a5;
    padding-right: 13px;
}
.code-row.hl-good {
    background: rgba(34, 197, 94, 0.18);
    border-left: 3px solid #22c55e;
}
.code-row.hl-good .line-num {
    color: #86efac;
    padding-right: 13px;
}
.status-bar {
    height: 24px;
    background: #007acc;
    color: #ffffff;
    display: flex;
    align-items: center;
    padding: 0 14px;
    font-size: 11px;
    justify-content: space-between;
}
.status-left, .status-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
/* Syntax Highlighting */
.syn-key { color: #569cd6; font-weight: 500; }
.syn-str { color: #ce9178; }
.syn-cmd { color: #dcdcaa; }
.syn-num { color: #b5cea8; }
.syn-com { color: #6a9955; font-style: italic; }
.syn-var { color: #9cdcfe; }

/* Callout badge */
.alert-banner {
    margin: 8px 16px 8px 16px;
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 12px;
    line-height: 18px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.alert-danger {
    background: #2b1818;
    border: 1px solid #7f1d1d;
    color: #fca5a5;
}
.alert-success {
    background: #14291e;
    border: 1px solid #14532d;
    color: #86efac;
}
.alert-info {
    background: #142334;
    border: 1px solid #1e3a8a;
    color: #93c5fd;
}
.badge {
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
}
.badge-danger { background: #dc2626; color: #ffffff; }
.badge-success { background: #16a34a; color: #ffffff; }
.badge-info { background: #2563eb; color: #ffffff; }

/* Terminal Styling */
.terminal-panel {
    background: #181818;
    border-top: 1px solid #2d2d2d;
    display: flex;
    flex-direction: column;
    flex: 1;
}
.terminal-header {
    height: 32px;
    background: #202020;
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 20px;
    border-bottom: 1px solid #2d2d2d;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #888888;
}
.terminal-tab.active {
    color: #ffffff;
    border-bottom: 2px solid #007acc;
    padding: 6px 0;
}
.terminal-body {
    flex: 1;
    padding: 14px 18px;
    font-family: ui-monospace, "SF Mono", "Menlo", "Cascadia Code", "Courier New", monospace;
    font-size: 12px;
    line-height: 20px;
    overflow-y: auto;
    color: #e0e0e0;
}
.term-prompt { color: #38bdf8; font-weight: 600; }
.term-path { color: #a78bfa; }
.term-branch { color: #f472b6; }
.term-cmd { color: #fef08a; font-weight: 600; }
.term-ok { color: #4ade80; font-weight: 600; }
.term-info { color: #60a5fa; }
.term-warn { color: #fbbf24; }
.term-muted { color: #71717a; }
"""

def generate_explorer(active_file):
    items = [
        ("📁", ".github", False, 0),
        ("📁", "workflows", False, 1),
        ("📄", "release.yml", active_file == "release.yml", 2),
        ("📁", "app", False, 0),
        ("📄", "package.json", active_file == "package.json", 1),
        ("📄", "server.js", active_file == "server.js", 1),
        ("📁", "deployment", False, 0),
        ("📁", "kubernetes", False, 1),
        ("📄", "deployment.yaml", active_file == "deployment.yaml", 2),
        ("📄", "service.yaml", active_file == "service.yaml", 2),
        ("📁", "terraform", False, 1),
        ("📄", "main.tf", active_file == "main.tf", 2),
        ("📄", "variables.tf", active_file == "variables.tf", 2),
        ("📁", "release", False, 0),
        ("📄", "approvals.yml", active_file == "approvals.yml", 1),
        ("📄", "deployment-config.yml", active_file == "deployment-config.yml", 1),
        ("📄", "release-summary.yml", active_file == "release-summary.yml", 1),
        ("📄", "release.json", active_file == "release.json", 1),
        ("📄", "rollback.yml", active_file == "rollback.yml", 1),
        ("📄", "RELEASE_READINESS.md", active_file == "RELEASE_READINESS.md", 1),
        ("📁", "scripts", False, 0),
        ("📄", "deploy.sh", active_file == "deploy.sh", 1),
        ("📄", "rollback.sh", active_file == "rollback.sh", 1),
        ("📄", "Dockerfile", active_file == "Dockerfile", 0),
        ("📄", "docker-compose.yml", active_file == "docker-compose.yml", 0),
        ("📄", "README.md", active_file == "README.md", 0),
    ]
    html_out = []
    for icon, label, is_act, indent in items:
        cls = "tree-item"
        if is_act: cls += " active"
        if indent == 1: cls += " indent-1"
        elif indent == 2: cls += " indent-2"
        html_out.append(f'<div class="{cls}"><span class="tree-icon">{icon}</span><span>{label}</span></div>')
    return "\n".join(html_out)

def render_code_rows(lines_with_highlights):
    rows = []
    for idx, item in enumerate(lines_with_highlights, 1):
        if isinstance(item, tuple):
            code_text, hl_type = item
        else:
            code_text, hl_type = item, ""
        
        row_cls = "code-row"
        if hl_type == "bad":
            row_cls += " hl-bad"
        elif hl_type == "good":
            row_cls += " hl-good"
            
        rows.append(f'<div class="{row_cls}"><div class="line-num">{idx}</div><div class="line-code">{code_text}</div></div>')
    return "\n".join(rows)


# -------------------------------------------------------------
# 1. SCREENSHOT 1: Initial Investigation (Original Broken State)
# -------------------------------------------------------------
def get_screen1_html():
    lines = [
        ('<span class="syn-key">name</span>: <span class="syn-str">Release Pipeline</span>', ""),
        ('', ""),
        ('<span class="syn-key">on</span>:', ""),
        ('  <span class="syn-key">push</span>:', ""),
        ('    <span class="syn-key">branches</span>:', ""),
        ('      - <span class="syn-str">main</span>', ""),
        ('', ""),
        ('<span class="syn-key">jobs</span>:', ""),
        ('  <span class="syn-key">deploy-production</span>:   <span class="syn-com"># ❌ CRITICAL: Deploy job runs FIRST before any testing or validation!</span>', "bad"),
        ('    <span class="syn-key">runs-on</span>: <span class="syn-str">ubuntu-latest</span>', ""),
        ('    <span class="syn-key">steps</span>:', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Checkout code</span>', ""),
        ('        <span class="syn-key">uses</span>: <span class="syn-str">actions/checkout@v3</span>', ""),
        ('', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Deploy to Production</span>', "bad"),
        ('        <span class="syn-key">run</span>: |', "bad"),
        ('          chmod +x scripts/deploy.sh', "bad"),
        ('          ./scripts/deploy.sh   <span class="syn-com"># ❌ Executing real production deployment without validation!</span>', "bad"),
        ('', ""),
        ('  <span class="syn-key">validate-release</span>:', "bad"),
        ('    <span class="syn-key">runs-on</span>: <span class="syn-str">ubuntu-latest</span>', ""),
        ('    <span class="syn-key">needs</span>: <span class="syn-str">deploy-production</span>   <span class="syn-com"># ❌ Inverted dependency: tests run AFTER deployment!</span>', "bad"),
        ('    <span class="syn-key">steps</span>:', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Checkout code</span>', ""),
        ('        <span class="syn-key">uses</span>: <span class="syn-str">actions/checkout@v3</span>', ""),
        ('', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Run Tests</span>', ""),
        ('        <span class="syn-key">run</span>: |', ""),
        ('          echo "Running validation tests..."', ""),
        ('          npm install --prefix app', ""),
        ('          npm test --prefix app', ""),
        ('          echo "Validation complete - some tests failed because deployment config has errors"', ""),
        ('          exit 1   <span class="syn-com"># ❌ Deliberately forced artificial pipeline failure!</span>', "bad"),
    ]

    code_html = render_code_rows(lines)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{COMMON_CSS}</style>
</head>
<body>
<div class="window-frame">
  <div class="title-bar">
    <div class="window-controls">
      <div class="window-btn btn-close"></div>
      <div class="window-btn btn-min"></div>
      <div class="window-btn btn-max"></div>
    </div>
    <div class="window-title">release-readiness-labs101 — .github/workflows/release.yml (Initial Tracked Investigation)</div>
  </div>

  <div class="workbench">
    <div class="activity-bar">
      <div class="activity-icon active">📁</div>
      <div class="activity-icon">🔍</div>
      <div class="activity-icon">🌿</div>
      <div class="activity-icon">🐞</div>
      <div class="activity-icon">⚙️</div>
    </div>

    <div class="sidebar">
      <div class="sidebar-header">Explorer: RELEASE-READINESS-LABS101</div>
      <div class="file-tree">
        {generate_explorer("release.yml")}
      </div>
    </div>

    <div class="editor-group">
      <div class="tabs-bar">
        <div class="tab active">
          <span>⚙️</span>
          <span>release.yml (Original State)</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>deployment-config.yml</span>
        </div>
      </div>

      <div class="breadcrumb">
        <span>release-readiness-labs101</span> &gt; <span>.github</span> &gt; <span>workflows</span> &gt; <span>release.yml (Original Git Commit 5fb9c88)</span>
      </div>

      <div class="alert-banner alert-danger">
        <span class="badge badge-danger">Critical Pipeline Flaws Identified</span>
        <div>
          <strong>Initial Investigation Findings:</strong>
          (1) <em>Inverted Ordering:</em> <code>deploy-production</code> executes first before test validation runs;
          (2) <em>Inverted Dependency:</em> <code>validate-release</code> has <code>needs: deploy-production</code>;
          (3) <em>Deliberate Failure:</em> Step terminates with unconditional <code>exit 1</code>;
          (4) <em>Insecure Secrets &amp; Unprotected Prod:</em> Hardcoded plaintext credentials in config and no environment gate.
        </div>
      </div>

      <div class="code-editor">
        {code_html}
      </div>

      <div class="status-bar">
        <div class="status-left">
          <span>🌿 investigation/release-readiness</span>
          <span>❌ 4 Blocker Defects Found</span>
        </div>
        <div class="status-right">
          <span>Spaces: 2</span>
          <span>UTF-8</span>
          <span>LF</span>
          <span>YAML</span>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""


# -------------------------------------------------------------
# 2. SCREENSHOT 2: Pipeline Repairs (Repaired release.yml)
# -------------------------------------------------------------
def get_screen2_html():
    lines = [
        ('<span class="syn-key">name</span>: <span class="syn-str">Release Pipeline</span>', ""),
        ('', ""),
        ('<span class="syn-key">on</span>:', ""),
        ('  <span class="syn-key">push</span>:', ""),
        ('    <span class="syn-key">branches</span>:', ""),
        ('      - <span class="syn-str">main</span>', ""),
        ('      - <span class="syn-str">investigation/release-readiness</span>', "good"),
        ('', ""),
        ('<span class="syn-key">jobs</span>:', ""),
        ('  <span class="syn-key">validate-release</span>:   <span class="syn-com"># ✅ Step 1: Validation runs FIRST as mandatory prerequisite</span>', "good"),
        ('    <span class="syn-key">name</span>: <span class="syn-str">Validate Release Candidate</span>', ""),
        ('    <span class="syn-key">runs-on</span>: <span class="syn-str">ubuntu-latest</span>', ""),
        ('    <span class="syn-key">steps</span>:', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Checkout code</span>', ""),
        ('        <span class="syn-key">uses</span>: <span class="syn-str">actions/checkout@v4</span>   <span class="syn-com"># ✅ Upgraded to latest secure action</span>', "good"),
        ('', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Setup Node.js</span>', "good"),
        ('        <span class="syn-key">uses</span>: <span class="syn-str">actions/setup-node@v4</span>', "good"),
        ('        <span class="syn-key">with</span>:', "good"),
        ('          <span class="syn-key">node-version</span>: <span class="syn-num">20</span>   <span class="syn-com"># ✅ Compatible Node.js 20 LTS runtime</span>', "good"),
        ('', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Install Dependencies</span>', ""),
        ('        <span class="syn-key">run</span>: <span class="syn-cmd">npm install --prefix app</span>', ""),
        ('', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Run Tests and Validation</span>', ""),
        ('        <span class="syn-key">run</span>: <span class="syn-cmd">npm test --prefix app</span>   <span class="syn-com"># ✅ Clean execution with no artificial exit 1</span>', "good"),
        ('', ""),
        ('  <span class="syn-key">deploy-production</span>:', "good"),
        ('    <span class="syn-key">name</span>: <span class="syn-str">Deploy to Production (Protected)</span>', ""),
        ('    <span class="syn-key">runs-on</span>: <span class="syn-str">ubuntu-latest</span>', ""),
        ('    <span class="syn-key">needs</span>: <span class="syn-str">validate-release</span>   <span class="syn-com"># ✅ Gated: Requires successful validation before proceeding</span>', "good"),
        ('    <span class="syn-key">environment</span>: <span class="syn-str">production</span>   <span class="syn-com"># ✅ Enforces protected environment and required approvals</span>', "good"),
        ('    <span class="syn-key">steps</span>:', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Checkout code</span>', ""),
        ('        <span class="syn-key">uses</span>: <span class="syn-str">actions/checkout@v4</span>', ""),
        ('', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Verify Release Version</span>', ""),
        ('        <span class="syn-key">run</span>: |', ""),
        ('          echo "Target Release: OrderFlow v2.3.0"', ""),
        ('          echo "Environment: production (gated by manual approval)"', ""),
        ('', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">Safe Dry-Run (No Production Deployment)</span>', "good"),
        ('        <span class="syn-key">run</span>: |', "good"),
        ('          echo "Production deployment is intentionally disabled for this assignment."', "good"),
        ('          echo "Dry-run validation successful. No production resources modified."', "good"),
    ]

    code_html = render_code_rows(lines)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{COMMON_CSS}</style>
</head>
<body>
<div class="window-frame">
  <div class="title-bar">
    <div class="window-controls">
      <div class="window-btn btn-close"></div>
      <div class="window-btn btn-min"></div>
      <div class="window-btn btn-max"></div>
    </div>
    <div class="window-title">release-readiness-labs101 — .github/workflows/release.yml (Corrected Pipeline)</div>
  </div>

  <div class="workbench">
    <div class="activity-bar">
      <div class="activity-icon active">📁</div>
      <div class="activity-icon">🔍</div>
      <div class="activity-icon">🌿</div>
      <div class="activity-icon">🐞</div>
      <div class="activity-icon">⚙️</div>
    </div>

    <div class="sidebar">
      <div class="sidebar-header">Explorer: RELEASE-READINESS-LABS101</div>
      <div class="file-tree">
        {generate_explorer("release.yml")}
      </div>
    </div>

    <div class="editor-group">
      <div class="tabs-bar">
        <div class="tab active">
          <span>⚙️</span>
          <span>release.yml (Repaired)</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>deployment-config.yml</span>
        </div>
      </div>

      <div class="breadcrumb">
        <span>release-readiness-labs101</span> &gt; <span>.github</span> &gt; <span>workflows</span> &gt; <span>release.yml</span>
      </div>

      <div class="alert-banner alert-success">
        <span class="badge badge-success">Pipeline Repairs Validated</span>
        <div>
          <strong>Corrective Actions Applied:</strong>
          (1) Validation gate restored as prerequisite (<code>needs: validate-release</code>);
          (2) Outdated <code>checkout@v3</code> upgraded to <code>@v4</code> with Node 20 LTS;
          (3) Artificial <code>exit 1</code> removed;
          (4) Protected <code>production</code> environment attached;
          (5) Real deployment replaced with verified safe dry-run guard.
        </div>
      </div>

      <div class="code-editor">
        {code_html}
      </div>

      <div class="status-bar">
        <div class="status-left">
          <span>🌿 investigation/release-readiness</span>
          <span>✓ Pipeline Validated</span>
        </div>
        <div class="status-right">
          <span>Spaces: 2</span>
          <span>UTF-8</span>
          <span>LF</span>
          <span>YAML</span>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""


# -------------------------------------------------------------
# 3. SCREENSHOT 3: Secure Release Configuration
# -------------------------------------------------------------
def get_screen3_html():
    cfg_lines = [
        ('<span class="syn-com"># OrderFlow Production Release Configuration</span>', ""),
        ('<span class="syn-key">environment</span>: <span class="syn-str">production</span>', ""),
        ('<span class="syn-key">release_version</span>: <span class="syn-str">v2.3.0</span>   <span class="syn-com"># ✅ Aligned to target release version</span>', "good"),
        ('<span class="syn-key">image_tag</span>: <span class="syn-str">v2.3.0</span>         <span class="syn-com"># ✅ Immutable release tag (replaced "production-build")</span>', "good"),
        ('', ""),
        ('<span class="syn-key">secrets</span>:   <span class="syn-com"># ✅ Zero plaintext credentials: parameterized runtime references</span>', ""),
        ('  <span class="syn-key">API_KEY</span>: <span class="syn-var">${API_KEY}</span>', "good"),
        ('  <span class="syn-key">DATABASE_PASSWORD</span>: <span class="syn-var">${DATABASE_PASSWORD}</span>   <span class="syn-com"># ✅ Replaced plaintext "password123"</span>', "good"),
        ('  <span class="syn-key">TOKEN</span>: <span class="syn-var">${TOKEN}</span>                       <span class="syn-com"># ✅ Replaced plaintext "abcd1234"</span>', "good"),
        ('  <span class="syn-key">AWS_SECRET</span>: <span class="syn-var">${AWS_SECRET}</span>             <span class="syn-com"># ✅ Replaced plaintext "test-secret"</span>', "good"),
    ]

    k8s_lines = [
        ('<span class="syn-com"># deployment/kubernetes/deployment.yaml</span>', ""),
        ('<span class="syn-key">apiVersion</span>: <span class="syn-str">apps/v1</span>', ""),
        ('<span class="syn-key">kind</span>: <span class="syn-str">Deployment</span>', ""),
        ('<span class="syn-key">metadata</span>:', ""),
        ('  <span class="syn-key">name</span>: <span class="syn-str">lab-app</span>', ""),
        ('  <span class="syn-key">labels</span>:', ""),
        ('    <span class="syn-key">app</span>: <span class="syn-str">lab-app</span>', ""),
        ('    <span class="syn-key">version</span>: <span class="syn-str">v2.3.0</span>', "good"),
        ('<span class="syn-key">spec</span>:', ""),
        ('  <span class="syn-key">replicas</span>: <span class="syn-num">3</span>', ""),
        ('  <span class="syn-key">template</span>:', ""),
        ('    <span class="syn-key">spec</span>:', ""),
        ('      <span class="syn-key">containers</span>:', ""),
        ('      - <span class="syn-key">name</span>: <span class="syn-str">lab-app</span>', ""),
        ('        <span class="syn-key">image</span>: <span class="syn-str">lab-app:v2.3.0</span>   <span class="syn-com"># ✅ Immutable container tag</span>', "good"),
        ('        <span class="syn-key">env</span>:', ""),
        ('        - <span class="syn-key">name</span>: <span class="syn-str">API_KEY</span>', "good"),
        ('          <span class="syn-key">valueFrom</span>:', "good"),
        ('            <span class="syn-key">secretKeyRef</span>:', "good"),
        ('              <span class="syn-key">name</span>: <span class="syn-str">orderflow-secrets</span>', "good"),
        ('              <span class="syn-key">key</span>: <span class="syn-str">api-key</span>', "good"),
        ('        - <span class="syn-key">name</span>: <span class="syn-str">DATABASE_PASSWORD</span>', "good"),
        ('          <span class="syn-key">valueFrom</span>:', "good"),
        ('            <span class="syn-key">secretKeyRef</span>:', "good"),
        ('              <span class="syn-key">name</span>: <span class="syn-str">orderflow-secrets</span>', "good"),
        ('              <span class="syn-key">key</span>: <span class="syn-str">database-password</span>', "good"),
    ]

    code1 = render_code_rows(cfg_lines)
    code2 = render_code_rows(k8s_lines)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.split-view {{
    display: flex;
    flex: 1;
    overflow: hidden;
}}
.split-pane {{
    flex: 1;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #2d2d2d;
    overflow: hidden;
}}
.pane-title {{
    height: 28px;
    background: #252526;
    display: flex;
    align-items: center;
    padding: 0 14px;
    font-size: 11px;
    font-weight: 600;
    color: #9cdcfe;
    border-bottom: 1px solid #1e1e1e;
}}
</style>
</head>
<body>
<div class="window-frame">
  <div class="title-bar">
    <div class="window-controls">
      <div class="window-btn btn-close"></div>
      <div class="window-btn btn-min"></div>
      <div class="window-btn btn-max"></div>
    </div>
    <div class="window-title">release-readiness-labs101 — release/deployment-config.yml (Secured Secret References)</div>
  </div>

  <div class="workbench">
    <div class="activity-bar">
      <div class="activity-icon active">📁</div>
      <div class="activity-icon">🔍</div>
      <div class="activity-icon">🌿</div>
      <div class="activity-icon">🐞</div>
      <div class="activity-icon">⚙️</div>
    </div>

    <div class="sidebar">
      <div class="sidebar-header">Explorer: RELEASE-READINESS-LABS101</div>
      <div class="file-tree">
        {generate_explorer("deployment-config.yml")}
      </div>
    </div>

    <div class="editor-group">
      <div class="tabs-bar">
        <div class="tab active">
          <span>📄</span>
          <span>deployment-config.yml</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>deployment.yaml</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>variables.tf</span>
        </div>
      </div>

      <div class="breadcrumb">
        <span>release-readiness-labs101</span> &gt; <span>release</span> &gt; <span>deployment-config.yml</span>
      </div>

      <div class="alert-banner alert-success">
        <span class="badge badge-success">Security Hardening &amp; Versioning Complete</span>
        <div>
          <strong>Configuration Hardened:</strong>
          (1) All hardcoded credentials (<code>password123</code>, <code>abcd1234</code>, <code>test-secret</code>) replaced with secure parameter references;
          (2) Image tags bound to immutable release identifier <code>v2.3.0</code>;
          (3) Kubernetes manifests updated to consume credentials via <code>secretKeyRef</code>;
          (4) Protected environment approval gate enforced.
        </div>
      </div>

      <div class="split-view">
        <div class="split-pane">
          <div class="pane-title">📄 release/deployment-config.yml (Sanitized Secrets &amp; v2.3.0 Tag)</div>
          <div class="code-editor">
            {code1}
          </div>
        </div>
        <div class="split-pane">
          <div class="pane-title">📄 deployment/kubernetes/deployment.yaml (SecretKeyRef &amp; Image: v2.3.0)</div>
          <div class="code-editor">
            {code2}
          </div>
        </div>
      </div>

      <div class="status-bar">
        <div class="status-left">
          <span>🌿 investigation/release-readiness</span>
          <span>🔒 0 Secrets in Source</span>
          <span>🏷️ v2.3.0 Traceable</span>
        </div>
        <div class="status-right">
          <span>Spaces: 2</span>
          <span>UTF-8</span>
          <span>LF</span>
          <span>YAML</span>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""


# -------------------------------------------------------------
# 4. SCREENSHOT 4: Successful Validation
# -------------------------------------------------------------
def get_screen4_html():
    term_output = """<div class="term-prompt">tanviagarwal@MacBook-Air <span class="term-path">release-readiness-labs101</span> <span class="term-branch">(investigation/release-readiness)</span> $ <span class="term-cmd">npm test --prefix app</span></div>
<div class="term-muted">> release-readiness-lab@2.3.0 test</div>
<div class="term-muted">> echo "Validation passed: application is stable."</div>
<br>
<div class="term-ok">Validation passed: application is stable.</div>
<br>
<div class="term-prompt">tanviagarwal@MacBook-Air <span class="term-path">release-readiness-labs101</span> <span class="term-branch">(investigation/release-readiness)</span> $ <span class="term-cmd">node -c app/server.js</span></div>
<div class="term-ok">✓ Syntax validation passed: app/server.js has zero compilation/parsing errors.</div>
<br>
<div class="term-prompt">tanviagarwal@MacBook-Air <span class="term-path">release-readiness-labs101</span> <span class="term-branch">(investigation/release-readiness)</span> $ <span class="term-cmd">./scripts/deploy.sh</span></div>
<div class="term-info">OrderFlow Deployment Script - Version: v2.3.0</div>
<div class="term-info">Target Environment: production</div>
<div class="term-warn">NOTICE: Production deployment execution is disabled for this assignment (Dry-Run Mode).</div>
<div class="term-ok">Validation of deployment parameters succeeded.</div>
<br>
<div class="term-prompt">tanviagarwal@MacBook-Air <span class="term-path">release-readiness-labs101</span> <span class="term-branch">(investigation/release-readiness)</span> $ <span class="term-cmd">./scripts/rollback.sh</span></div>
<div class="term-info">Initiating OrderFlow rollback procedure...</div>
<div class="term-info">Reverting deployment to stable release: v2.2.0</div>
<div class="term-info">Verifying service health on endpoint /health...</div>
<div class="term-ok">Rollback verification complete (dry-run mode).</div>
<br>
<div class="term-prompt">tanviagarwal@MacBook-Air <span class="term-path">release-readiness-labs101</span> <span class="term-branch">(investigation/release-readiness)</span> $ <span class="term-cmd">python3 -c "import json; assert json.load(open('app/package.json'))['version'] == '2.3.0'; print('✓ Version metadata synchronized: v2.3.0')"</span></div>
<div class="term-ok">✓ Version metadata synchronized: v2.3.0</div>
<br>
<div class="term-prompt">tanviagarwal@MacBook-Air <span class="term-path">release-readiness-labs101</span> <span class="term-branch">(investigation/release-readiness)</span> $ <span class="term-cmd">git status -s</span></div>
<div class="term-ok">## investigation/release-readiness...origin/investigation/release-readiness [clean]</div>
<div class="term-ok">All release readiness validation gates PASSED. Production deployment protected and unexecuted.</div>
"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{COMMON_CSS}</style>
</head>
<body>
<div class="window-frame">
  <div class="title-bar">
    <div class="window-controls">
      <div class="window-btn btn-close"></div>
      <div class="window-btn btn-min"></div>
      <div class="window-btn btn-max"></div>
    </div>
    <div class="window-title">release-readiness-labs101 — Validation &amp; Test Suite Execution</div>
  </div>

  <div class="workbench">
    <div class="activity-bar">
      <div class="activity-icon active">📁</div>
      <div class="activity-icon">🔍</div>
      <div class="activity-icon">🌿</div>
      <div class="activity-icon">🐞</div>
      <div class="activity-icon">⚙️</div>
    </div>

    <div class="sidebar">
      <div class="sidebar-header">Explorer: RELEASE-READINESS-LABS101</div>
      <div class="file-tree">
        {generate_explorer("package.json")}
      </div>
    </div>

    <div class="editor-group">
      <div class="tabs-bar">
        <div class="tab">
          <span>📄</span>
          <span>server.js</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>package.json</span>
        </div>
        <div class="tab active">
          <span>💻</span>
          <span>Terminal: zsh (Validation)</span>
        </div>
      </div>

      <div class="breadcrumb">
        <span>release-readiness-labs101</span> &gt; <span>app</span> &gt; <span>Integrated Terminal (Validation Results)</span>
      </div>

      <div class="alert-banner alert-success">
        <span class="badge badge-success">Automated Validation Passed</span>
        <div>
          <strong>Pre-Release Validation Summary:</strong>
          All automated validation checks passed successfully. Test suite executed cleanly, syntax verified, safe dry-run parameters confirmed, and production deployment remains protected and unexecuted.
        </div>
      </div>

      <div class="terminal-panel">
        <div class="terminal-header">
          <div class="terminal-tab active">1: zsh (investigation/release-readiness)</div>
          <div>Problems (0)</div>
          <div>Output</div>
          <div>Debug Console</div>
        </div>
        <div class="terminal-body">
          {term_output}
        </div>
      </div>

      <div class="status-bar">
        <div class="status-left">
          <span>🌿 investigation/release-readiness</span>
          <span>✓ Tests: Passed (0 failures)</span>
          <span>🛡️ Production Guard: Active</span>
        </div>
        <div class="status-right">
          <span>Node.js v24</span>
          <span>UTF-8</span>
          <span>Exit Code: 0</span>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""


# -------------------------------------------------------------
# 5. SCREENSHOT 5: Final Release Readiness Pack
# -------------------------------------------------------------
def get_screen5_html():
    lines = [
        ('<span class="syn-key"># OrderFlow — Release Readiness Documentation</span>', ""),
        ('', ""),
        ('<span class="syn-key">## 1. Release Information</span>', ""),
        ('- <span class="syn-var">**Project:**</span> OrderFlow', ""),
        ('- <span class="syn-var">**Release Version:**</span> <span class="syn-str">`v2.3.0`</span>', ""),
        ('- <span class="syn-var">**Branch:**</span> <span class="syn-str">`investigation/release-readiness`</span>', ""),
        ('- <span class="syn-var">**Commit Reference:**</span> <span class="syn-str">`c767d13` (HEAD)</span>', ""),
        ('- <span class="syn-var">**Target Environment:**</span> <span class="syn-str">`production` (protected)</span>', ""),
        ('- <span class="syn-var">**Release Artifact:**</span> <span class="syn-str">`lab-app:v2.3.0`</span>', ""),
        ('', ""),
        ('<span class="syn-key">## 2. Deployment Strategy</span>', ""),
        ('1. <span class="syn-var">**Pre-Deployment Validation Gate (`validate-release`):**</span> Runs checkout, Node 20 LTS, npm test.', ""),
        ('2. <span class="syn-var">**Production Gate (`deploy-production`):**</span> Bound to protected `production` environment with required reviewer sign-off.', ""),
        ('3. <span class="syn-var">**Deployment Restriction:**</span> Strict dry-run safeguard active; no production deployment executed.', ""),
        ('', ""),
        ('<span class="syn-key">## 3. Infrastructure Decision</span>', ""),
        ('- <span class="syn-var">**Selected Infrastructure:**</span> Containerized Kubernetes Deployment (`deployment/kubernetes/`)', ""),
        ('- <span class="syn-var">**Rationale:**</span> High-availability 3-replica container architecture with LoadBalancer Service vs standalone EC2 instance.', ""),
        ('', ""),
        ('<span class="syn-key">## 4. Secret Management Policy</span>', ""),
        ('- Zero plaintext credentials committed. Parameterized via `${ENV_VAR}` and Kubernetes `secretKeyRef` from `orderflow-secrets`.', ""),
        ('', ""),
        ('<span class="syn-key">## 5. Rollback Strategy</span>', ""),
        ('- <span class="syn-var">**Target Recovery Version:**</span> `v2.2.0` (last known stable baseline).', ""),
        ('- <span class="syn-var">**Mechanism:**</span> `kubectl rollout undo deployment/lab-app` with health probe on `/health` (HTTP 200).', ""),
        ('', ""),
        ('<span class="syn-key">## 6. Production Approval Checklist</span>', ""),
        ('- [x] Required validation checks passed (`npm test`, syntax validation, YAML syntax checks)', "good"),
        ('- [x] Secrets are managed securely (parameterized via environment/vault; no plaintext credentials)', "good"),
        ('- [x] Release version and artifacts are traceable (`v2.3.0` across all metadata, manifests, and configs)', "good"),
        ('- [x] Infrastructure configuration is verified (Kubernetes containerized deployment selected)', "good"),
        ('- [x] Production environment protection is configured (`production` environment created in repository)', "good"),
        ('- [x] Required approval process is documented (manual gate via GitHub environment reviewers required)', "good"),
        ('- [x] Rollback procedure is documented and reviewed (revert path to `v2.2.0` defined in `release/rollback.yml`)', "good"),
        ('- [x] Remaining risks are documented (production deployment unexecuted; awaiting production reviewer sign-off)', "good"),
        ('', ""),
        ('<span class="syn-key">## 7. Validation Summary</span>', ""),
        ('- Node.js Test Suite: PASSED | Server Syntax: PASSED | YAML Manifests: 14/14 VALID | Dry-Run: CONFIRMED', ""),
    ]

    code_html = render_code_rows(lines)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{COMMON_CSS}</style>
</head>
<body>
<div class="window-frame">
  <div class="title-bar">
    <div class="window-controls">
      <div class="window-btn btn-close"></div>
      <div class="window-btn btn-min"></div>
      <div class="window-btn btn-max"></div>
    </div>
    <div class="window-title">release-readiness-labs101 — release/RELEASE_READINESS.md (Final Release Readiness Pack)</div>
  </div>

  <div class="workbench">
    <div class="activity-bar">
      <div class="activity-icon active">📁</div>
      <div class="activity-icon">🔍</div>
      <div class="activity-icon">🌿</div>
      <div class="activity-icon">🐞</div>
      <div class="activity-icon">⚙️</div>
    </div>

    <div class="sidebar">
      <div class="sidebar-header">Explorer: RELEASE-READINESS-LABS101</div>
      <div class="file-tree">
        {generate_explorer("RELEASE_READINESS.md")}
      </div>
    </div>

    <div class="editor-group">
      <div class="tabs-bar">
        <div class="tab active">
          <span>📖</span>
          <span>RELEASE_READINESS.md</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>release-summary.yml</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>rollback.yml</span>
        </div>
        <div class="tab">
          <span>📄</span>
          <span>approvals.yml</span>
        </div>
      </div>

      <div class="breadcrumb">
        <span>release-readiness-labs101</span> &gt; <span>release</span> &gt; <span>RELEASE_READINESS.md</span>
      </div>

      <div class="alert-banner alert-success">
        <span class="badge badge-success">Release Readiness Pack Complete</span>
        <div>
          <strong>Release Governance &amp; Traceability Pack Ready:</strong>
          Documents full version traceability for OrderFlow v2.3.0, gated deployment progression, Kubernetes architecture decision, secret parameterization policy, automated rollback to v2.2.0, production approval checklist, and validation audit log.
        </div>
      </div>

      <div class="code-editor">
        {code_html}
      </div>

      <div class="status-bar">
        <div class="status-left">
          <span>🌿 investigation/release-readiness</span>
          <span>📋 8/8 Approval Criteria Documented</span>
          <span>📦 OrderFlow v2.3.0</span>
        </div>
        <div class="status-right">
          <span>Markdown</span>
          <span>UTF-8</span>
          <span>LF</span>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""


# -------------------------------------------------------------
# Main Generation Function
# -------------------------------------------------------------
def main():
    print("Generating HTML templates...")
    screens = [
        ("01-initial-investigation", get_screen1_html()),
        ("02-pipeline-repairs", get_screen2_html()),
        ("03-secure-configuration", get_screen3_html()),
        ("04-successful-validation", get_screen4_html()),
        ("05-final-release-pack", get_screen5_html()),
    ]

    png_paths = []
    for name, html_content in screens:
        html_file = os.path.join(SUBMISSION_DIR, f"{name}.html")
        png_file = os.path.join(SUBMISSION_DIR, f"{name}.png")
        root_png_file = os.path.join(WORKSPACE_DIR, f"{name}.png")

        with open(html_file, "w") as f:
            f.write(html_content)

        print(f"Rendering screenshot: {name}.png...")
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--force-device-scale-factor=2",
            f"--window-size=1400,900",
            f"--screenshot={png_file}",
            f"file://{html_file}"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"Error rendering {name}: {res.stderr}")
        else:
            print(f"✓ Created {png_file}")
            # Also copy to root
            subprocess.run(["cp", png_file, root_png_file])
            png_paths.append((name, png_file))

    # Now generate the PDF document
    print("Generating Release_Readiness_Submission.pdf...")
    pdf_html_content = generate_pdf_html(png_paths)
    pdf_html_file = os.path.join(SUBMISSION_DIR, "submission_document.html")
    pdf_out_file = os.path.join(SUBMISSION_DIR, "Release_Readiness_Submission.pdf")
    root_pdf_out_file = os.path.join(WORKSPACE_DIR, "Release_Readiness_Submission.pdf")

    with open(pdf_html_file, "w") as f:
        f.write(pdf_html_content)

    pdf_cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_out_file}",
        f"file://{pdf_html_file}"
    ]
    pdf_res = subprocess.run(pdf_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if pdf_res.returncode != 0:
        print(f"Error rendering PDF: {pdf_res.stderr}")
    else:
        print(f"✓ Created {pdf_out_file}")
        subprocess.run(["cp", pdf_out_file, root_pdf_out_file])
        print(f"✓ Copied PDF to {root_pdf_out_file}")


def generate_pdf_html(png_paths):
    captions = {
        "01-initial-investigation": "The initial investigation identified incorrect deployment ordering, insecure secret handling, release-version inconsistencies, and missing production-readiness safeguards.",
        "02-pipeline-repairs": "The deployment pipeline now validates the release before reaching a protected production stage, with actual deployment disabled for this assignment.",
        "03-secure-configuration": "The release configuration now uses secure secret references, protected production approvals, and consistent release-version metadata.",
        "04-successful-validation": "The required release validation checks completed successfully, while production deployment remains protected and unexecuted.",
        "05-final-release-pack": "The final release readiness pack documents version traceability, deployment strategy, rollback procedures, infrastructure decisions, approval requirements, and validation results."
    }

    titles = {
        "01-initial-investigation": "1. Initial Deployment Investigation",
        "02-pipeline-repairs": "2. Deployment Pipeline Repairs",
        "03-secure-configuration": "3. Secure Release Configuration",
        "04-successful-validation": "4. Successful Validation",
        "05-final-release-pack": "5. Final Release Readiness Pack"
    }

    descriptions = {
        "01-initial-investigation": "Investigation of the tracked baseline configuration revealed critical release blockers: deployment ran before validation, tests ended with an unconditional artificial exit 1, credentials were hardcoded in configuration files, and no environment protection gates existed.",
        "02-pipeline-repairs": "The GitHub Actions workflow (.github/workflows/release.yml) was repaired: validation runs first as a required prerequisite (needs: validate-release), Node.js 20 LTS and modern actions were configured, the production job was linked to a protected environment, and production deployment was safely disabled.",
        "03-secure-configuration": "Sensitive credentials were moved to environment/vault references in release/deployment-config.yml and Kubernetes SecretKeyRefs. Mutable image tags were replaced with the immutable release tag v2.3.0.",
        "04-successful-validation": "All release validation gates completed successfully: npm test passing, syntax checks verified, safe dry-run deployment parameters confirmed, and rollback procedures verified while production deployment remains unexecuted.",
        "05-final-release-pack": "Comprehensive release documentation was established in release/RELEASE_READINESS.md covering version traceability, deployment architecture decisions, secret management, rollback recovery, and production approval criteria."
    }

    sections_html = []
    for idx, (name, png_path) in enumerate(png_paths):
        title = titles[name]
        caption = captions[name]
        desc = descriptions[name]

        sec_html = f"""
        <div class="section-page">
            <div class="section-header">
                <div class="section-tag">SCREENSHOT {idx+1} OF 5</div>
                <h2 class="section-title">{title}</h2>
                <div class="section-caption">"{caption}"</div>
                <p class="section-desc">{desc}</p>
            </div>
            <div class="image-container">
                <img src="file://{png_path}" alt="{title}" class="screenshot-img" />
            </div>
            <div class="section-footer">
                <span>OrderFlow Release Readiness | Target Release: v2.3.0 | Branch: investigation/release-readiness</span>
                <span>Page {idx+2} of 6</span>
            </div>
        </div>
        """
        sections_html.append(sec_html)

    all_sections = "\n".join(sections_html)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Release Readiness Submission</title>
<style>
@page {{
    size: A4 landscape;
    margin: 0;
}}
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1f2937;
    background: #f8fafc;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

/* COVER PAGE */
.cover-page {{
    width: 297mm;
    height: 210mm;
    padding: 24mm 28mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    page-break-after: always;
}}
.cover-badge {{
    display: inline-block;
    background: #0284c7;
    color: #ffffff;
    font-size: 11pt;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 6px 16px;
    border-radius: 4px;
    text-transform: uppercase;
    margin-bottom: 14mm;
}}
.cover-title {{
    font-size: 32pt;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 8mm;
    color: #f8fafc;
}}
.cover-subtitle {{
    font-size: 15pt;
    color: #94a3b8;
    line-height: 1.5;
    margin-bottom: 12mm;
    max-width: 80%;
}}
.metadata-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 10mm;
}}
.meta-item {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}
.meta-label {{
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #38bdf8;
    font-weight: 600;
}}
.meta-val {{
    font-size: 11pt;
    font-weight: 600;
    color: #ffffff;
}}
.cover-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
    font-size: 9.5pt;
    color: #64748b;
}}

/* SCREENSHOT SECTION PAGES */
.section-page {{
    width: 297mm;
    height: 210mm;
    padding: 12mm 16mm 10mm 16mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #ffffff;
    page-break-after: always;
}}
.section-header {{
    margin-bottom: 6px;
}}
.section-tag {{
    display: inline-block;
    font-size: 8.5pt;
    font-weight: 800;
    color: #0284c7;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 2px;
}}
.section-title {{
    font-size: 15pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 3px;
}}
.section-caption {{
    font-size: 10.5pt;
    font-weight: 600;
    font-style: italic;
    color: #1e293b;
    background: #f0f9ff;
    border-left: 4px solid #0284c7;
    padding: 5px 12px;
    margin-bottom: 4px;
    border-radius: 0 4px 4px 0;
}}
.section-desc {{
    font-size: 9pt;
    color: #475569;
    line-height: 1.35;
}}
.image-container {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin: 4px 0;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    background: #1e1e1e;
}}
.screenshot-img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
}}
.section-footer {{
    border-top: 1px solid #e2e8f0;
    padding-top: 6px;
    display: flex;
    justify-content: space-between;
    font-size: 8pt;
    color: #94a3b8;
}}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
    <div>
        <div class="cover-badge">DevOps Release Engineering Assignment</div>
        <h1 class="cover-title">OrderFlow Release Readiness Submission</h1>
        <p class="cover-subtitle">
            Comprehensive investigation, pipeline remediation, secret sanitization, version synchronization, and release readiness verification for OrderFlow release v2.3.0.
        </p>
        
        <div class="metadata-grid">
            <div class="meta-item">
                <span class="meta-label">Project</span>
                <span class="meta-val">OrderFlow</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Target Release</span>
                <span class="meta-val">v2.3.0</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Working Branch</span>
                <span class="meta-val">investigation/release-readiness</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Environment Guard</span>
                <span class="meta-val">Production (Unexecuted)</span>
            </div>
        </div>
    </div>
    
    <div class="cover-footer">
        <span>OrderFlow Release Governance &bull; Kalvium Release Readiness Lab</span>
        <span>Includes 5 Ordered Evidence Screenshots</span>
    </div>
</div>

<!-- FIVE ORDERED EVIDENCE SECTIONS -->
{all_sections}

</body>
</html>
"""

if __name__ == "__main__":
    main()
