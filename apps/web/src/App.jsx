import React, { useEffect, useMemo, useState } from "react";

import { api } from "./api";
import CreatePanel from "./components/CreatePanel";
import PracticePanel from "./components/PracticePanel";
import ProblemListPanel from "./components/ProblemListPanel";

const STORAGE_KEY = "practice.currentId";

const codeTemplates = {
  c: `#include <stdio.h>
int main(void){
    return 0;
}`,
  cpp: `#include <iostream>
int main(){
    return 0;
}`,
  java: `public class Main {
    public static void main(String[] args) {
    }
}`
};

const initialForm = {
  title: "delete min element",
  module: "linear-list",
  difficulty: "easy",
  language: "c",
  statement: "给定顺序表，删除最小元素。",
  thinking: "遍历找到最小元素位置，再覆盖删除。",
  code: codeTemplates.c,
  stdin: ""
};

function normalizeError(error) {
  if (error instanceof Error) {
    return { error: error.message };
  }
  return { error: String(error) };
}

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [currentId, setCurrentId] = useState(null);
  const [finished, setFinished] = useState(false);
  const [focusMode, setFocusMode] = useState(true);
  const [problems, setProblems] = useState([]);
  const [result, setResult] = useState({});
  const [reviewHistory, setReviewHistory] = useState([]);

  const canArchive = useMemo(() => currentId !== null && finished, [currentId, finished]);

  async function refreshList() {
    try {
      const items = await api.listProblems();
      setProblems(Array.isArray(items) ? items : []);
    } catch (error) {
      setResult(normalizeError(error));
    }
  }

  useEffect(() => {
    async function bootstrap() {
      await refreshList();

      const rawId = window.localStorage.getItem(STORAGE_KEY);
      if (!rawId) {
        return;
      }

      const restoredId = Number(rawId);
      if (!Number.isInteger(restoredId) || restoredId <= 0) {
        window.localStorage.removeItem(STORAGE_KEY);
        return;
      }

      try {
        const detail = await api.getProblem(restoredId);
        setCurrentId(restoredId);
        setFinished(["finished", "archiving", "archived"].includes(detail.state));
        setReviewHistory(Array.isArray(detail.review_history) ? detail.review_history : []);
        setForm((prev) => ({
          ...prev,
          title: detail.title ?? prev.title,
          module: detail.module ?? prev.module,
          difficulty: detail.difficulty ?? prev.difficulty,
          language: detail.language ?? prev.language,
          statement: detail.statement ?? prev.statement,
          thinking: detail.user_thinking ?? prev.thinking,
          code: detail.latest_code || codeTemplates[detail.language] || prev.code,
        }));
      } catch {
        window.localStorage.removeItem(STORAGE_KEY);
      }
    }

    bootstrap();
  }, []);

  function updateField(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function updateLanguage(language) {
    setForm((prev) => ({
      ...prev,
      language,
      code: codeTemplates[language] ?? prev.code
    }));
  }

  async function onCreate() {
    try {
      const payload = {
        title: form.title,
        module: form.module,
        difficulty: form.difficulty,
        language: form.language,
        statement: form.statement,
        user_thinking: form.thinking,
        c_topics: [],
        tags: []
      };
      const created = await api.createProblem(payload);
      setCurrentId(created.id);
      window.localStorage.setItem(STORAGE_KEY, String(created.id));
      setFinished(false);
      setResult(created);
      setReviewHistory([]);
      await refreshList();
    } catch (error) {
      setResult(normalizeError(error));
    }
  }

  async function onRun() {
    try {
      const execution = await api.execute({
        language: form.language,
        code: form.code,
        stdin: form.stdin
      });
      setResult(execution);
    } catch (error) {
      setResult(normalizeError(error));
    }
  }

  async function onSubmit() {
    if (currentId === null) {
      setResult({ error: "请先创建题目" });
      return;
    }
    try {
      const response = await api.submit(currentId, {
        code: form.code,
        user_thinking: form.thinking
      });
      setResult(response);
    } catch (error) {
      setResult(normalizeError(error));
    }
  }

  async function onFinish() {
    if (currentId === null) {
      setResult({ error: "请先创建题目" });
      return;
    }
    try {
      const response = await api.finish(currentId);
      setFinished(true);
      setResult(response);
      await refreshList();
    } catch (error) {
      setResult(normalizeError(error));
    }
  }

  async function onReview() {
    if (currentId === null) {
      setResult({ error: "请先创建题目" });
      return;
    }
    try {
      const response = await api.review(currentId);
      setResult(response);
      setReviewHistory((prev) => [
        ...prev,
        {
          attempt: prev.length + 1,
          status: response.review_status,
          total_score: response.total_score ?? 0,
        },
      ]);
    } catch (error) {
      setResult(normalizeError(error));
    }
  }

  async function onArchive() {
    if (!canArchive) {
      setResult({ error: "请先确认结束" });
      return;
    }
    try {
      const response = await api.archive(currentId);
      setResult(response);
      await refreshList();
    } catch (error) {
      setResult(normalizeError(error));
    }
  }

  function onToggleFocusMode() {
    setFocusMode((prev) => !prev);
  }

  return (
    <main className="layout">
      <CreatePanel
        form={form}
        onFieldChange={updateField}
        onLanguageChange={updateLanguage}
        onCreate={onCreate}
      />
      <PracticePanel
        form={form}
        currentId={currentId}
        canArchive={canArchive}
        result={result}
        reviewHistory={reviewHistory}
        focusMode={focusMode}
        onToggleFocusMode={onToggleFocusMode}
        onFieldChange={updateField}
        onRun={onRun}
        onSubmit={onSubmit}
        onFinish={onFinish}
        onReview={onReview}
        onArchive={onArchive}
      />
      <ProblemListPanel problems={problems} onRefresh={refreshList} />
    </main>
  );
}
