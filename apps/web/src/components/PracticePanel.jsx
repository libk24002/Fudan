import React from "react";
import ReviewScoreCards from "./ReviewScoreCards";

export default function PracticePanel({
  form,
  currentId,
  canArchive,
  result,
  reviewHistory,
  focusMode,
  onToggleFocusMode,
  onFieldChange,
  onRun,
  onSubmit,
  onFinish,
  onReview,
  onArchive,
}) {
  const chartWidth = 320;
  const chartHeight = 90;
  const maxScore = 25;
  const points = reviewHistory.map((item, index) => {
    const x = reviewHistory.length === 1 ? chartWidth / 2 : (index / (reviewHistory.length - 1)) * chartWidth;
    const y = chartHeight - (Math.max(0, Math.min(maxScore, item.total_score || 0)) / maxScore) * chartHeight;
    return { x, y };
  });
  const polylinePoints = points.map((p) => `${p.x},${p.y}`).join(" ");
  const hasAiFeedback =
    typeof result?.review_status === "string" ||
    (Array.isArray(result?.issues) && result.issues.length > 0) ||
    (Array.isArray(result?.suggestions) && result.suggestions.length > 0);

  return (
    <section className="panel">
      <h2>练题</h2>
      <p>
        当前题目 ID: <strong>{currentId ?? "-"}</strong>
      </p>
      <label>
        代码
        <textarea value={form.code} onChange={(e) => onFieldChange("code", e.target.value)} />
      </label>
      <label>
        输入
        <textarea value={form.stdin} onChange={(e) => onFieldChange("stdin", e.target.value)} />
      </label>
      <div className="row">
        <button onClick={onRun}>运行</button>
        <button onClick={onSubmit}>提交解法</button>
        <button onClick={onFinish}>确认结束</button>
        <button onClick={onReview}>AI评审</button>
        <button onClick={onArchive} disabled={!canArchive}>
          归档入库
        </button>
        <button onClick={onToggleFocusMode}>{focusMode ? "关闭专注模式" : "开启专注模式"}</button>
      </div>
      {hasAiFeedback ? (
        <section className="feedback-panel">
          <h3>AI点评</h3>
          <p>{`结果: ${result.review_status ?? "N/A"}`}</p>
          {Array.isArray(result.issues) && result.issues.length > 0 ? (
            <>
              <strong>问题</strong>
              <ul>
                {result.issues.map((item, index) => (
                  <li key={`issue-${index}`}>{item}</li>
                ))}
              </ul>
            </>
          ) : null}
          {Array.isArray(result.suggestions) && result.suggestions.length > 0 ? (
            <>
              <strong>建议</strong>
              <ul>
                {result.suggestions.map((item, index) => (
                  <li key={`sug-${index}`}>{item}</li>
                ))}
              </ul>
            </>
          ) : null}
        </section>
      ) : null}
      {!focusMode ? <ReviewScoreCards result={result} /> : null}
      {!focusMode && reviewHistory.length > 0 ? (
        <section className="history-panel">
          <h3>历史评分</h3>
          <svg className="history-chart" viewBox={`0 0 ${chartWidth} ${chartHeight}`} aria-label="review-history-chart">
            <line x1="0" y1={chartHeight} x2={chartWidth} y2={chartHeight} className="history-axis" />
            {points.length > 1 ? <polyline className="history-line" points={polylinePoints} /> : null}
            {points.map((point, index) => (
              <circle
                key={`${reviewHistory[index].attempt}-${reviewHistory[index].total_score}`}
                cx={point.x}
                cy={point.y}
                r="4"
                data-testid="history-point"
                className="history-point"
              >
                <title>{`趋势点: 第 ${reviewHistory[index].attempt} 次 ${reviewHistory[index].status} ${reviewHistory[index].total_score}/25`}</title>
              </circle>
            ))}
          </svg>
          <ul>
            {reviewHistory.map((item) => (
              <li key={item.attempt}>{`第 ${item.attempt} 次: ${item.status} - ${item.total_score} / 25`}</li>
            ))}
          </ul>
        </section>
      ) : null}
      <pre className="result">{JSON.stringify(result, null, 2)}</pre>
    </section>
  );
}
