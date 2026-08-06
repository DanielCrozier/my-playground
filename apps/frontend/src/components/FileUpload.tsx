import { useState, useRef, type ChangeEvent, type FormEvent } from "react";
import type { JSX } from "react";
import { uploadFile, type UploadResult } from "../api/upload";

type UploadState =
  | { status: "idle" }
  | { status: "uploading" }
  | { status: "success"; result: UploadResult }
  | { status: "error"; message: string };

export function FileUpload(): JSX.Element {
  const [file, setFile] = useState<File | null>(null);
  const [state, setState] = useState<UploadState>({ status: "idle" });
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFileChange(e: ChangeEvent<HTMLInputElement>): void {
    const selected = e.target.files?.[0] ?? null;
    setFile(selected);
    setState({ status: "idle" });
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();
    if (!file) return;

    setState({ status: "uploading" });
    try {
      const result = await uploadFile(file);
      setState({ status: "success", result });
      setFile(null);
      if (inputRef.current) {
        inputRef.current.value = "";
      }
    } catch (err) {
      setState({
        status: "error",
        message: err instanceof Error ? err.message : "Unknown error",
      });
    }
  }

  return (
    <section aria-labelledby="upload-heading">
      <h1 id="upload-heading">Upload a file</h1>

      <form onSubmit={handleSubmit} noValidate>
        <label htmlFor="file-input">Choose file</label>
        <input
          id="file-input"
          ref={inputRef}
          type="file"
          onChange={handleFileChange}
          aria-describedby={state.status === "error" ? "upload-error" : undefined}
        />

        <button type="submit" disabled={!file || state.status === "uploading"}>
          {state.status === "uploading" ? "Uploading…" : "Upload"}
        </button>
      </form>

      {state.status === "success" && (
        <p role="status" aria-live="polite">
          ✅ Uploaded as <code>{state.result.blob_name}</code>
        </p>
      )}

      {state.status === "error" && (
        <p id="upload-error" role="alert" aria-live="assertive">
          ❌ {state.message}
        </p>
      )}
    </section>
  );
}
