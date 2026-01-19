"""
Cucumber-style Gherkin HTML Report Generator for pytest-bdd
Clean, simple design matching cucumber-js html-formatter style
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class GherkinReportGenerator:
    """Generate a cucumber-style HTML report from pytest-bdd test results."""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def add_result(self, feature: str, scenario: str, steps: list, status: str,
                   duration: float, error: str = None):
        """Add a test result."""
        self.results.append({
            'feature': feature,
            'scenario': scenario,
            'steps': steps,
            'status': status,
            'duration': duration,
            'error': error
        })
    
    def generate_html(self, output_path: str):
        """Generate the HTML report."""
        if self.start_time is None:
            self.start_time = datetime.now()
        if self.end_time is None:
            self.end_time = datetime.now()
        
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Group results by feature file
        features: Dict[str, List[Dict]] = {}
        for result in self.results:
            feature = result.get('feature', 'Unknown Feature')
            if feature not in features:
                features[feature] = []
            features[feature].append(result)
        
        # Calculate stats
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get('status') == 'passed')
        failed = sum(1 for r in self.results if r.get('status') == 'failed')
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html = self._generate_html_content(features, pass_rate, duration, passed, failed, total)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _generate_html_content(self, features: Dict, pass_rate: float, duration: float, 
                                passed: int, failed: int, total: int) -> str:
        """Generate the complete HTML document."""
        features_html = self._generate_features_html(features)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDD Test Report</title>
    <style>
        :root {{
            --passed: #22c55e;
            --failed: #ef4444;
            --keyword: #8b5cf6;
            --param: #0ea5e9;
            --bg: #ffffff;
            --bg-alt: #f8fafc;
            --text: #1e293b;
            --text-dim: #64748b;
            --border: #e2e8f0;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --keyword: #a78bfa;
                --param: #38bdf8;
                --bg: #0f172a;
                --bg-alt: #1e293b;
                --text: #f1f5f9;
                --text-dim: #94a3b8;
                --border: #334155;
            }}
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 24px; }}
        
        /* Header */
        header {{ display: flex; justify-content: space-between; align-items: center; padding: 20px; background: var(--bg-alt); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 20px; }}
        .title {{ font-size: 1.5rem; font-weight: 600; display: flex; align-items: center; gap: 10px; }}
        .meta {{ color: var(--text-dim); font-size: 0.875rem; }}
        .stats {{ display: flex; gap: 24px; }}
        .stat {{ text-align: center; }}
        .stat-val {{ font-size: 1.5rem; font-weight: 700; }}
        .stat-val.pass {{ color: var(--passed); }}
        .stat-val.fail {{ color: var(--failed); }}
        .stat-lbl {{ font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; }}
        
        /* Progress bar */
        .progress {{ height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; margin-bottom: 20px; }}
        .progress-fill {{ height: 100%; background: var(--passed); }}
        
        /* Feature */
        .feature {{ border: 1px solid var(--border); border-radius: 8px; margin-bottom: 12px; overflow: hidden; }}
        .feature-head {{ display: flex; align-items: center; padding: 12px 16px; background: var(--bg-alt); cursor: pointer; gap: 8px; }}
        .feature-head:hover {{ filter: brightness(0.95); }}
        .arrow {{ color: var(--text-dim); transition: transform 0.2s; font-size: 0.75rem; }}
        .feature.open .arrow {{ transform: rotate(90deg); }}
        .feature-name {{ flex: 1; font-weight: 500; }}
        .badge {{ padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; }}
        .badge.pass {{ background: rgba(34,197,94,0.15); color: var(--passed); }}
        .badge.fail {{ background: rgba(239,68,68,0.15); color: var(--failed); }}
        .feature-body {{ display: none; padding: 12px; }}
        .feature.open .feature-body {{ display: block; }}
        
        /* Scenario */
        .scenario {{ border: 1px solid var(--border); border-radius: 6px; margin-bottom: 8px; }}
        .scenario:last-child {{ margin-bottom: 0; }}
        .scenario-head {{ display: flex; align-items: center; padding: 10px 12px; cursor: pointer; gap: 8px; }}
        .scenario-head:hover {{ background: var(--bg-alt); }}
        .icon {{ width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; color: #fff; }}
        .icon.pass {{ background: var(--passed); }}
        .icon.fail {{ background: var(--failed); }}
        .scenario-name {{ flex: 1; }}
        .kw {{ color: var(--keyword); font-weight: 600; }}
        .dur {{ color: var(--text-dim); font-size: 0.8rem; }}
        .scenario-body {{ display: none; padding: 8px 12px; border-top: 1px solid var(--border); }}
        .scenario.open .scenario-body {{ display: block; }}
        
        /* Steps */
        .step {{ display: flex; align-items: flex-start; padding: 6px 0; gap: 10px; }}
        .step + .step {{ border-top: 1px solid var(--border); }}
        .step-icon {{ width: 16px; height: 16px; border-radius: 50%; font-size: 0.55rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 3px; }}
        .step-icon.pass {{ background: rgba(34,197,94,0.15); color: var(--passed); }}
        .step-icon.fail {{ background: rgba(239,68,68,0.15); color: var(--failed); }}
        .step-content {{ flex: 1; }}
        .step-kw {{ color: var(--keyword); font-weight: 600; }}
        .step-param {{ color: var(--param); }}
        .step-dur {{ color: var(--text-dim); font-size: 0.75rem; margin-left: 8px; }}
        
        /* Error */
        .error {{ margin-top: 8px; padding: 10px; background: rgba(239,68,68,0.08); border-left: 3px solid var(--failed); border-radius: 4px; font-family: monospace; font-size: 0.8rem; white-space: pre-wrap; color: var(--failed); max-height: 200px; overflow-y: auto; }}
        
        footer {{ text-align: center; padding: 20px; color: var(--text-dim); font-size: 0.8rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <div class="title">🥒 BDD Test Report</div>
                <div class="meta">pytest-bdd + Playwright • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
            <div class="stats">
                <div class="stat"><div class="stat-val pass">{pass_rate:.0f}%</div><div class="stat-lbl">Pass Rate</div></div>
                <div class="stat"><div class="stat-val">{duration:.1f}s</div><div class="stat-lbl">Duration</div></div>
                <div class="stat"><div class="stat-val pass">{passed}</div><div class="stat-lbl">Passed</div></div>
                <div class="stat"><div class="stat-val fail">{failed}</div><div class="stat-lbl">Failed</div></div>
            </div>
        </header>
        
        <div class="progress"><div class="progress-fill" style="width:{pass_rate}%"></div></div>
        
        {features_html}
        
        <footer>Generated by pytest-bdd Gherkin Reporter</footer>
    </div>
    <script>
        document.querySelectorAll('.feature-head').forEach(h => h.onclick = () => h.parentElement.classList.toggle('open'));
        document.querySelectorAll('.scenario-head').forEach(h => h.onclick = e => {{ e.stopPropagation(); h.parentElement.classList.toggle('open'); }});
        document.querySelectorAll('.feature').forEach(f => {{ if(f.querySelector('.badge.fail')) f.classList.add('open'); }});
        document.querySelectorAll('.scenario').forEach(s => {{ if(s.querySelector('.icon.fail')) s.classList.add('open'); }});
    </script>
</body>
</html>'''
    
    def _generate_features_html(self, features: Dict[str, List[Dict]]) -> str:
        """Generate HTML for all features."""
        parts = []
        for name, scenarios in features.items():
            p = sum(1 for s in scenarios if s.get('status') == 'passed')
            f = sum(1 for s in scenarios if s.get('status') == 'failed')
            scenarios_html = ''.join(self._scenario_html(s) for s in scenarios)
            badges = f'{"<span class=badge pass>✓ "+str(p)+"</span>" if p else ""}{"<span class=badge fail>✗ "+str(f)+"</span>" if f else ""}'
            parts.append(f'''<div class="feature"><div class="feature-head"><span class="arrow">▶</span><span class="feature-name">{self._esc(name)}</span>{badges}</div><div class="feature-body">{scenarios_html}</div></div>''')
        return '\n'.join(parts)
    
    def _scenario_html(self, s: Dict) -> str:
        """Generate HTML for a scenario."""
        status = s.get('status', 'unknown')
        name = s.get('scenario', '')
        dur = s.get('duration', 0)
        steps = ''.join(self._step_html(st) for st in s.get('steps', []))
        icon = '✓' if status == 'passed' else '✗'
        cls = 'pass' if status == 'passed' else 'fail'
        return f'''<div class="scenario"><div class="scenario-head"><span class="icon {cls}">{icon}</span><span class="scenario-name"><span class="kw">Scenario:</span> {self._esc(name)}</span><span class="dur">{dur:.2f}s</span></div><div class="scenario-body">{steps}</div></div>'''
    
    def _step_html(self, st: Dict) -> str:
        """Generate HTML for a step."""
        kw = st.get('keyword', '')
        name = st.get('name', '')
        status = st.get('status', 'passed')
        dur = st.get('duration', 0)
        err = st.get('error', '')
        cls = 'pass' if status == 'passed' else 'fail'
        icon = '✓' if status == 'passed' else '✗'
        formatted = re.sub(r'"([^"]*)"', r'<span class="step-param">"\1"</span>', self._esc(name))
        error_html = f'<div class="error">{self._esc(err)}</div>' if err else ''
        return f'''<div class="step"><span class="step-icon {cls}">{icon}</span><div class="step-content"><span class="step-kw">{self._esc(kw)}</span> {formatted}<span class="step-dur">{dur:.3f}s</span>{error_html}</div></div>'''
    
    def _esc(self, t: str) -> str:
        """Escape HTML."""
        return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;') if t else ''
