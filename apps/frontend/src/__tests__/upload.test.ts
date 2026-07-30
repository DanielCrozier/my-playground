import { uploadFile } from "../api/upload";

// Mock fetch globally
const mockFetch = jest.fn();
globalThis.fetch = mockFetch as typeof globalThis.fetch;

beforeEach(() => {
  mockFetch.mockReset();
});

describe("uploadFile", () => {
  it("returns blob_name on success", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ blob_name: "uuid-test.txt" }),
    });

    const file = new File(["hello"], "test.txt", { type: "text/plain" });
    const result = await uploadFile(file);

    expect(result.blob_name).toBe("uuid-test.txt");
    expect(mockFetch).toHaveBeenCalledTimes(1);

    const [url, init] = mockFetch.mock.calls[0] as [string, RequestInit];
    expect(url).toContain("/upload");
    expect(init.method).toBe("POST");
    expect(init.body).toBeInstanceOf(FormData);
  });

  it("throws an error when the response is not ok", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 415,
      text: async () => "Unsupported media type",
    });

    const file = new File(["data"], "bad.exe", {
      type: "application/x-executable",
    });

    await expect(uploadFile(file)).rejects.toThrow("Upload failed (415)");
  });
});
