(function () {
  "use strict";

  const config = window.CW_PAPER_CONFIG || {};
  const papers = Array.isArray(window.CW_PAPERS) ? window.CW_PAPERS : [];
  const target = document.querySelector(config.target || "[data-paper-list]");

  if (!target) return;

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function normalizeTextList(value) {
    if (Array.isArray(value)) {
      return value.map((item) => String(item || "").trim()).filter(Boolean);
    }

    if (typeof value === "string" && value.trim()) {
      return value.split(/\n\s*\n/).map((item) => item.trim()).filter(Boolean);
    }

    return [];
  }

  function paperHref(paper) {
    const pdf = String(paper.pdf || "").trim();
    if (!pdf) return "";
    if (/^https?:\/\//i.test(pdf) || pdf.startsWith("/") || pdf.startsWith("#")) {
      return pdf;
    }
    return `${config.basePath || ""}${pdf}`;
  }

  function renderTags(paper) {
    const tags = [paper.status].concat(Array.isArray(paper.tags) ? paper.tags : []);
    return tags
      .map((tag, index) => String(tag || "").trim() ? `<span class="tag${index === 0 ? " coral" : ""}">${escapeHtml(tag)}</span>` : "")
      .join("");
  }

  function renderPaper(paper, isFeatured) {
    const title = escapeHtml(paper.title || "Untitled paper");
    const href = escapeHtml(paperHref(paper));
    const summary = String(paper.summary || "").trim();
    const abstracts = normalizeTextList(paper.abstract);
    const tags = renderTags(paper);

    const summaryHtml = summary ? `<p class="abstract">${escapeHtml(summary)}</p>` : "";
    const abstractHtml = !isFeatured && abstracts.length
      ? abstracts.map((paragraph) => `<p class="abstract">${escapeHtml(paragraph)}</p>`).join("")
      : "";
    const paperLink = href ? `<a href="${href}">Read paper</a>` : "";
    const researchLink = isFeatured && config.researchHref
      ? `<a href="${escapeHtml(config.researchHref)}">Research page</a>`
      : "";

    return `
<article class="paper-card solo-paper">
<div class="paper-topline">${tags}</div>
<div class="paper-body">
<h2>${title}</h2>
${summaryHtml}
${abstractHtml}
<div class="paper-links">
${paperLink}
${researchLink}
</div>
</div>
</article>`;
  }

  function renderEmpty() {
    target.innerHTML = '<p class="section-lede">No papers listed yet.</p>';
  }

  if (!papers.length) {
    renderEmpty();
    return;
  }

  if (config.mode === "featured") {
    target.innerHTML = renderPaper(papers[0], true);
    return;
  }

  target.innerHTML = papers.map((paper) => renderPaper(paper, false)).join("");
})();
