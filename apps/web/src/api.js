const API_BASE = "http://127.0.0.1:8000";

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || response.statusText);
  }
  return payload;
}

export const api = {
  createProblem(payload) {
    return request("/api/problems", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  },
  listProblems() {
    return request("/api/problems");
  },
  getProblem(problemId) {
    return request(`/api/problems/${problemId}`);
  },
  execute(payload) {
    return request("/api/sandbox/execute", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  },
  submit(problemId, payload) {
    return request(`/api/problems/${problemId}/submit`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  },
  finish(problemId) {
    return request(`/api/problems/${problemId}/finish`, {
      method: "POST"
    });
  },
  review(problemId) {
    return request(`/api/problems/${problemId}/review`, {
      method: "POST"
    });
  },
  archive(problemId) {
    return request(`/api/problems/${problemId}/archive`, {
      method: "POST"
    });
  }
};
