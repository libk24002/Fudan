import React from "react";

const LABELS = {
  correctness: "正确性",
  complexity: "复杂度",
  edge_cases: "边界条件",
  code_quality: "代码质量",
  thinking_clarity: "思路清晰度",
};

function scoreClass(value) {
  if (value >= 4) {
    return "score-card-high";
  }
  if (value >= 2) {
    return "score-card-medium";
  }
  return "score-card-low";
}

function statusClass(status) {
  return status === "PASS" ? "review-status-pass" : "review-status-fail";
}

export default function ReviewScoreCards({ result }) {
  const rubric = result?.rubric;
  if (!rubric || typeof rubric !== "object") {
    return null;
  }

  const total = Number.isFinite(result?.total_score) ? result.total_score : 0;
  const entries = Object.entries(LABELS).map(([key, label]) => ({
    key,
    label,
    value: Number.isFinite(rubric[key]) ? rubric[key] : 0,
  }));
  const status = result?.review_status === "PASS" ? "PASS" : "FAIL";

  return (
    <section className="score-panel" aria-label="review-score-panel">
      <div className="score-header">
        <h3>评审评分</h3>
        <div className="score-header-meta">
          <span className={`review-status-badge ${statusClass(status)}`}>{status}</span>
          <strong>{`总分 ${total} / 25`}</strong>
        </div>
      </div>
      <div className="score-grid">
        {entries.map((item) => (
          <article key={item.key} className={`score-card ${scoreClass(item.value)}`}>
            <span>{item.label}</span>
            <strong>{`${item.value} / 5`}</strong>
          </article>
        ))}
      </div>
    </section>
  );
}
