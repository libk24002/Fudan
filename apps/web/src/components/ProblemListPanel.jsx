import React from "react";

export default function ProblemListPanel({ problems, onRefresh }) {
  return (
    <section className="panel">
      <h2>题库</h2>
      <button onClick={onRefresh}>刷新题目列表</button>
      <ul>
        {problems.map((item) => (
          <li key={item.id}>{`#${item.id} ${item.title} [${item.state}]`}</li>
        ))}
      </ul>
    </section>
  );
}
