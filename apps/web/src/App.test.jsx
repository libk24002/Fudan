import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";

import App from "./App";

test("archive button is disabled before finish and enabled after finish", async () => {
  const user = userEvent.setup();

  const fetchMock = vi.fn()
    .mockResolvedValueOnce({
      ok: true,
      json: async () => []
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, state: "practicing", title: "delete min", module: "linear-list", difficulty: "easy", language: "c" })
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => []
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, state: "finished", title: "delete min", module: "linear-list", difficulty: "easy", language: "c" })
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => []
    });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);

  const archiveBtn = screen.getByRole("button", { name: "归档入库" });
  expect(archiveBtn).toBeDisabled();

  await user.click(screen.getByRole("button", { name: "创建并进入练习" }));
  await user.click(screen.getByRole("button", { name: "确认结束" }));
  expect(archiveBtn).toBeEnabled();

  vi.unstubAllGlobals();
});

test("switching language updates starter code template", async () => {
  const user = userEvent.setup();

  const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => [] });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);

  const codeBox = screen.getByLabelText("代码");
  expect(codeBox.value).toContain("#include <stdio.h>");

  await user.selectOptions(screen.getByLabelText("语言"), "java");
  expect(codeBox.value).toContain("public class Main");

  await user.selectOptions(screen.getByLabelText("语言"), "cpp");
  expect(codeBox.value).toContain("#include <iostream>");

  vi.unstubAllGlobals();
});

test("shows review score cards after AI review result", async () => {
  const user = userEvent.setup();

  const fetchMock = vi.fn()
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 3, state: "practicing", title: "delete range", module: "linear-list", difficulty: "easy", language: "c" })
    })
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        review_status: "PASS",
        issues: [],
        suggestions: ["边界处理完整"],
        rubric: {
          correctness: 5,
          complexity: 4,
          edge_cases: 4,
          code_quality: 4,
          thinking_clarity: 5
        },
        total_score: 22
      })
    });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);
  await user.click(screen.getByRole("button", { name: "创建并进入练习" }));
  await user.click(screen.getByRole("button", { name: "AI评审" }));

  expect(screen.queryByText("评审评分")).not.toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: "关闭专注模式" }));

  expect(screen.getByText("评审评分")).toBeInTheDocument();
  expect(screen.getByText("总分 22 / 25")).toBeInTheDocument();
  expect(screen.getByText("正确性")).toBeInTheDocument();
  expect(screen.getByText("PASS")).toBeInTheDocument();

  const correctnessCard = screen.getByText("正确性").closest("article");
  expect(correctnessCard).toHaveClass("score-card-high");

  vi.unstubAllGlobals();
});

test("shows low score style and fail badge", async () => {
  const user = userEvent.setup();

  const fetchMock = vi.fn()
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 4, state: "practicing", title: "delete range", module: "linear-list", difficulty: "easy", language: "c" })
    })
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        review_status: "FAIL",
        issues: ["边界条件未覆盖"],
        suggestions: ["补充空表和单元素情况"],
        rubric: {
          correctness: 1,
          complexity: 2,
          edge_cases: 1,
          code_quality: 2,
          thinking_clarity: 1
        },
        total_score: 7
      })
    });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);
  await user.click(screen.getByRole("button", { name: "创建并进入练习" }));
  await user.click(screen.getByRole("button", { name: "AI评审" }));
  await user.click(screen.getByRole("button", { name: "关闭专注模式" }));

  expect(screen.getByText("FAIL")).toBeInTheDocument();
  const edgeCard = screen.getByText("边界条件").closest("article");
  expect(edgeCard).toHaveClass("score-card-low");

  vi.unstubAllGlobals();
});

test("renders review history after multiple reviews", async () => {
  const user = userEvent.setup();

  const fetchMock = vi.fn()
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 5, state: "practicing", title: "history", module: "linear-list", difficulty: "easy", language: "c" })
    })
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        review_status: "PASS",
        issues: [],
        suggestions: [],
        rubric: {
          correctness: 5,
          complexity: 4,
          edge_cases: 4,
          code_quality: 4,
          thinking_clarity: 5
        },
        total_score: 22
      })
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        review_status: "FAIL",
        issues: ["边界条件不足"],
        suggestions: ["补充边界情况"],
        rubric: {
          correctness: 2,
          complexity: 3,
          edge_cases: 1,
          code_quality: 3,
          thinking_clarity: 2
        },
        total_score: 11
      })
    });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);
  await user.click(screen.getByRole("button", { name: "创建并进入练习" }));
  await user.click(screen.getByRole("button", { name: "AI评审" }));
  await user.click(screen.getByRole("button", { name: "AI评审" }));
  await user.click(screen.getByRole("button", { name: "关闭专注模式" }));

  expect(screen.getByText("历史评分")).toBeInTheDocument();
  expect(screen.getByText("第 1 次: PASS - 22 / 25")).toBeInTheDocument();
  expect(screen.getByText("第 2 次: FAIL - 11 / 25")).toBeInTheDocument();
  expect(screen.getByLabelText("review-history-chart")).toBeInTheDocument();
  expect(screen.getAllByTestId("history-point")).toHaveLength(2);
  expect(screen.getByText("趋势点: 第 1 次 PASS 22/25")).toBeInTheDocument();
  expect(screen.getByText("趋势点: 第 2 次 FAIL 11/25")).toBeInTheDocument();

  vi.unstubAllGlobals();
});

test("restores current problem and review history from backend detail on reload", async () => {
  window.localStorage.setItem("practice.currentId", "9");

  const fetchMock = vi.fn()
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: 9,
        title: "restore-demo",
        module: "linear-list",
        difficulty: "easy",
        language: "c",
        state: "finished",
        statement: "删除最小值",
        user_thinking: "先找最小再覆盖",
        latest_code: "#include <stdio.h>\nint main(void){return 0;}",
        review_history: [
          { attempt: 1, status: "PASS", total_score: 20 },
          { attempt: 2, status: "FAIL", total_score: 11 }
        ]
      })
    });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);

  expect(await screen.findByText("当前题目 ID:")).toBeInTheDocument();
  expect(screen.getByText("9")).toBeInTheDocument();
  await userEvent.setup().click(screen.getByRole("button", { name: "关闭专注模式" }));
  expect(screen.getByText("历史评分")).toBeInTheDocument();
  expect(screen.getByText("第 1 次: PASS - 20 / 25")).toBeInTheDocument();
  expect(screen.getByText("第 2 次: FAIL - 11 / 25")).toBeInTheDocument();

  window.localStorage.removeItem("practice.currentId");
  vi.unstubAllGlobals();
});

test("focus mode keeps textual AI feedback visible", async () => {
  const user = userEvent.setup();

  const fetchMock = vi.fn()
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 6, state: "practicing", title: "focus", module: "linear-list", difficulty: "easy", language: "c" })
    })
    .mockResolvedValueOnce({ ok: true, json: async () => [] })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        review_status: "FAIL",
        issues: ["边界条件不足"],
        suggestions: ["补充空表和单元素情况"],
        rubric: {
          correctness: 2,
          complexity: 3,
          edge_cases: 1,
          code_quality: 3,
          thinking_clarity: 2
        },
        total_score: 11
      })
    });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);
  await user.click(screen.getByRole("button", { name: "创建并进入练习" }));
  await user.click(screen.getByRole("button", { name: "AI评审" }));

  expect(screen.getByText("AI点评")).toBeInTheDocument();
  expect(screen.getByText("边界条件不足")).toBeInTheDocument();
  expect(screen.getByText("补充空表和单元素情况")).toBeInTheDocument();
  expect(screen.queryByText("评审评分")).not.toBeInTheDocument();

  vi.unstubAllGlobals();
});
