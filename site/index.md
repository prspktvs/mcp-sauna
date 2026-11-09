---
layout: default
title: Rehearse your MCP server
description: Find the rough edges in the tools your AI agent actually sees, before your users do.
---

<section class="hero">
  <div class="hero-inner">
    <div class="eyebrow">An open source review skill for MCP servers · v1.0.0</div>
    <h1>Give your MCP server a <em>rehearsal</em> before the audience arrives.</h1>
    <p class="hero-copy">Your API can be healthy while an agent still guesses the wrong tool, gets stuck on an ID, or mistakes a failure for an empty result. mcp-sauna helps you catch those contract problems before real users become the testers.</p>
    <div class="hero-actions">
      <a class="button" href="https://github.com/prspktvs/mcp-sauna#try-it">Try mcp-sauna <span aria-hidden="true">↗</span></a>
      <a class="button secondary" href="{{ '/reports/' | relative_url }}">Read example reports</a>
    </div>
    <div class="hero-note"><strong>Built for development and test servers.</strong> The review never calls destructive tools.</div>
  </div>
</section>

<section class="section">
  <div class="section-heading">
    <div class="kicker">The interface your agent sees</div>
    <h2>Working endpoints don’t guarantee a working agent experience.</h2>
    <p>An agent makes choices from tool descriptions, schemas, annotations, and responses. Small gaps in that contract turn into extra calls, dead ends, oversized answers, and unsafe guesses.</p>
  </div>
  <div class="problem-grid">
    <article class="problem-card"><div class="card-number">01 / CHOICE</div><h3>“Which tool do I use?”</h3><p>Overlapping tools leave the model guessing about the intended path and its boundaries.</p></article>
    <article class="problem-card"><div class="card-number">02 / INPUTS</div><h3>“What does this ID mean?”</h3><p>Required fields without examples or a lookup path lead to retries and dead ends.</p></article>
    <article class="problem-card"><div class="card-number">03 / RESULTS</div><h3>“Did that actually work?”</h3><p>Unbounded results and vague errors make it hard to tell what happened or what to do next.</p></article>
  </div>
</section>

<section class="section">
  <div class="section-heading">
    <div class="kicker">A practical rehearsal</div>
    <h2>From tool catalog to a fix list your team can use.</h2>
    <p>mcp-sauna gives your connected agent a repeatable way to inspect the contract and check a few confirmed, safe tasks.</p>
  </div>
  <div class="steps-grid">
    <article class="step-card"><div class="step-number">1</div><h3>Connect a test server</h3><p>Tell the agent which non-production MCP server to review.</p></article>
    <article class="step-card"><div class="step-number">2</div><h3>Review the contract</h3><p>Check tool purpose, inputs, boundaries, result size, errors, and safety hints.</p></article>
    <article class="step-card"><div class="step-number">3</div><h3>Try bounded tasks</h3><p>Use confirmed tasks and safe read calls. Skipped checks stay visible as incomplete.</p></article>
    <article class="step-card"><div class="step-number">4</div><h3>Fix what matters</h3><p>Get a scorecard with stable rule IDs, evidence, and prioritized changes.</p></article>
  </div>
</section>

<section class="section">
  <div class="quote-band">
    <blockquote>“The point is not another protocol ping. It’s finding where a capable agent has to guess.”</blockquote>
    <div><p>mcp-sauna turns an agent’s view of your MCP tools into a review you can act on. Your agent interprets evidence; the bundled grader handles the score arithmetic. The rules are public, and the report shows what was checked and what could not be checked safely.</p><p><a href="{{ '/rules/v1/' | relative_url }}">Read mcp-sauna rules v1 →</a></p></div>
  </div>
</section>

<section class="section">
  <div class="section-heading">
    <div class="kicker">See the output</div>
    <h2>A report is more than a grade.</h2>
    <p>Every finding points to a tool and compact evidence, explains the user impact, and suggests a concrete fix. Examples use fictional data from the included reference servers.</p>
  </div>
  <div class="report-grid">
    <article class="report-card"><span class="tag">Reference · seeded issues</span><h3>Naive server</h3><p>See how ambiguous tools, unbounded lists, weak errors, and missing identity boundaries appear in a report.</p><a href="{{ '/reports/naive-v0-1/' | relative_url }}">Open the report</a></article>
    <article class="report-card"><span class="tag">Reference · stronger design</span><h3>Good server</h3><p>See a cleaner tool contract, including how a remaining medium finding and skipped checks are handled.</p><a href="{{ '/reports/good-v0-1/' | relative_url }}">Open the report</a></article>
  </div>
</section>

<section class="section">
  <div class="section-heading">
    <div class="kicker">Evidence, clearly labeled</div>
    <h2>A stable standard. Host coverage stated plainly.</h2>
    <p>The v1 rules are stable and public. The recorded portability runs are historical v0.1 evaluations; this release has not had a fresh cross-host evaluation.</p>
  </div>
  <div class="problem-grid">
    <article class="problem-card"><div class="card-number">RECORDED · V0.1</div><h3>Codex</h3><p>Passed the naive reference checks twice with stable High/Critical findings and no High/Critical findings on the good reference.</p></article>
    <article class="problem-card"><div class="card-number">RECORDED · V0.1</div><h3>Claude Code</h3><p>Passed the same recorded reference checks. The saved runs used the final v0.1 skill revision.</p></article>
    <article class="problem-card"><div class="card-number">NOT TESTED</div><h3>GitHub Copilot</h3><p>No compatibility claim is made. Exact parity across hosts remains unverified.</p></article>
  </div>
  <p><a href="https://github.com/prspktvs/mcp-sauna/blob/main/eval/agent-matrix.md">Read the evaluation record and limitations →</a></p>
</section>

<section class="section">
  <div class="cta-panel"><div><h2>Make the next failure a rehearsal.</h2><p>Install the skill into the agent you already use and point it at a test server.</p></div><a class="button" href="https://github.com/prspktvs/mcp-sauna#try-it">Get started on GitHub <span aria-hidden="true">↗</span></a></div>
</section>
