const API_BASE_URL: string =
  // process.env.VITE_API_BASE_URL is statically replaced by Vite at build
  // time (via define in vite.config.ts) and is naturally available in Node/Jest.
  process.env["VITE_API_BASE_URL"] ?? "http://localhost:8000";

export interface UploadResult {
  blob_name: string;
}

export async function uploadFile(file: File): Promise<UploadResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Upload failed (${response.status}): ${text}`);
  }

  return response.json() as Promise<UploadResult>;
}
