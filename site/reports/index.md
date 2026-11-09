---
layout: default
title: Example reports
permalink: /reports/
---

<article class="doc-wrap">
  <div class="kicker">What the team gets back</div>
  <h1>Example reports</h1>
  <p class="lede">These reports come from mcp-sauna’s fictional local reference servers. They show the shape of the findings and how the reviewer marks incomplete coverage.</p>
  <div class="doc-callout">The reports below are archived v0.1 examples, generated before the stable v1 release. They demonstrate the report format; they are not claims about the compatibility of the current v1 skill in every agent host.</div>
  <div class="report-grid">
    <article class="report-card"><span class="tag">Synthetic · seeded issues</span><h3>Naive reference server</h3><p>High and critical findings in a deliberately weak tool design. Safety is correctly marked incomplete where probes were skipped.</p><a href="{{ '/reports/naive-v0-1/' | relative_url }}">Read the full report</a></article>
    <article class="report-card"><span class="tag">Synthetic · improved design</span><h3>Good reference server</h3><p>No high or critical findings, one medium annotation issue, and incomplete checks called out.</p><a href="{{ '/reports/good-v0-1/' | relative_url }}">Read the full report</a></article>
  </div>
  <p>Want to run your own? <a href="https://github.com/prspktvs/mcp-sauna#try-it">Install the skill from GitHub</a> and connect it to a non-production MCP server.</p>
</article>
