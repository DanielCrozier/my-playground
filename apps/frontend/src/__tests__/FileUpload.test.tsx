import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FileUpload } from "../components/FileUpload";
import * as uploadApi from "../api/upload";

jest.mock("../api/upload");
const mockUploadFile = uploadApi.uploadFile as jest.MockedFunction<
  typeof uploadApi.uploadFile
>;

describe("FileUpload component", () => {
  beforeEach(() => {
    mockUploadFile.mockReset();
  });

  it("renders heading and file input", () => {
    render(<FileUpload />);
    expect(screen.getByRole("heading", { name: /upload a file/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/choose file/i)).toBeInTheDocument();
  });

  it("upload button is disabled when no file is selected", () => {
    render(<FileUpload />);
    expect(screen.getByRole("button", { name: /upload/i })).toBeDisabled();
  });

  it("upload button is enabled after a file is chosen", async () => {
    render(<FileUpload />);
    const input = screen.getByLabelText(/choose file/i);
    const file = new File(["content"], "photo.png", { type: "image/png" });

    await userEvent.upload(input, file);

    expect(screen.getByRole("button", { name: /upload/i })).toBeEnabled();
  });

  it("shows success message after successful upload", async () => {
    mockUploadFile.mockResolvedValueOnce({ blob_name: "abc-photo.png" });
    render(<FileUpload />);

    const input = screen.getByLabelText(/choose file/i);
    const file = new File(["content"], "photo.png", { type: "image/png" });
    await userEvent.upload(input, file);
    await userEvent.click(screen.getByRole("button", { name: /upload/i }));

    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent("abc-photo.png");
    });
  });

  it("shows error message when upload fails", async () => {
    mockUploadFile.mockRejectedValueOnce(new Error("Upload failed (415): bad type"));
    render(<FileUpload />);

    const input = screen.getByLabelText(/choose file/i);
    const file = new File(["content"], "bad.exe", {
      type: "application/x-executable",
    });
    await userEvent.upload(input, file);
    await userEvent.click(screen.getByRole("button", { name: /upload/i }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Upload failed (415)");
    });
  });

  it("shows uploading state during submission", async () => {
    let resolve: (value: uploadApi.UploadResult) => void;
    mockUploadFile.mockImplementationOnce(
      () =>
        new Promise<uploadApi.UploadResult>((res) => {
          resolve = res;
        }),
    );

    render(<FileUpload />);
    const input = screen.getByLabelText(/choose file/i);
    await userEvent.upload(input, new File(["x"], "x.png", { type: "image/png" }));
    await userEvent.click(screen.getByRole("button", { name: /upload/i }));

    expect(await screen.findByRole("button", { name: /uploading/i })).toBeDisabled();

    resolve!({ blob_name: "done.png" });
    await waitFor(() => {
      expect(screen.getByRole("status")).toBeInTheDocument();
    });
  });
});
