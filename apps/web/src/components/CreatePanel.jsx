import React from "react";

export default function CreatePanel({ form, onFieldChange, onLanguageChange, onCreate }) {
  return (
    <section className="panel">
      <h1>新建题目</h1>
      <label>
        标题
        <input value={form.title} onChange={(e) => onFieldChange("title", e.target.value)} />
      </label>
      <label>
        模块
        <input value={form.module} onChange={(e) => onFieldChange("module", e.target.value)} />
      </label>
      <label>
        难度
        <select value={form.difficulty} onChange={(e) => onFieldChange("difficulty", e.target.value)}>
          <option value="easy">easy</option>
          <option value="medium">medium</option>
          <option value="hard">hard</option>
        </select>
      </label>
      <label>
        语言
        <select value={form.language} onChange={(e) => onLanguageChange(e.target.value)}>
          <option value="c">C</option>
          <option value="cpp">C++</option>
          <option value="java">Java</option>
        </select>
      </label>
      <label>
        题目描述
        <textarea value={form.statement} onChange={(e) => onFieldChange("statement", e.target.value)} />
      </label>
      <label>
        思路说明
        <textarea value={form.thinking} onChange={(e) => onFieldChange("thinking", e.target.value)} />
      </label>
      <button onClick={onCreate}>创建并进入练习</button>
    </section>
  );
}
