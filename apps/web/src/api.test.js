import { beforeEach, describe, expect, it, vi } from "vitest";

describe("api request base url", () => {
  beforeEach(() => {
    vi.resetModules();
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("uses fallback base url when env is absent", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) }));

    const { request } = await import("./api.js");
    await request("/health");

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/health",
      expect.objectContaining({ headers: { "Content-Type": "application/json" } })
    );
  });

  it("uses env base url when VITE_API_BASE_URL is set", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "https://api.example.com");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) }));

    const { request } = await import("./api.js");
    await request("/health");

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "https://api.example.com/health",
      expect.objectContaining({ headers: { "Content-Type": "application/json" } })
    );
  });

  it("normalizes URL join when env base ends with slash", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "https://api.example.com/");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) }));

    const { request } = await import("./api.js");
    await request("/health");

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "https://api.example.com/health",
      expect.objectContaining({ headers: { "Content-Type": "application/json" } })
    );
  });
});
