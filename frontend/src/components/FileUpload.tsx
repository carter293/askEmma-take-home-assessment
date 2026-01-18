import { useMemo, useState } from "react";
import { useDropzone } from "react-dropzone";

const MAX_BYTES = 1_000_000;

function getExt(name: string) {
  const i = name.lastIndexOf(".");
  return i >= 0 ? name.slice(i + 1).toLowerCase() : "";
}

interface FileUploadProps {
  onFileChange?: (file: File | null) => void;
  file?: File | null;
}

export function FileUpload({ onFileChange, file: externalFile }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Sync internal state with external file prop
  if (externalFile !== file && externalFile === null) {
    setFile(null);
    setError(null);
  }

  const accept = useMemo(
    () => ({
      "text/plain": [".txt"],
      "text/markdown": [".md"],
      "text/x-markdown": [".md"],
    }),
    []
  );

  const { getRootProps, getInputProps, isDragActive, isDragReject } =
    useDropzone({
      multiple: false,
      accept,
      maxSize: MAX_BYTES,
      onDrop: (accepted, rejected) => {
        setError(null);

        const f = accepted?.[0] ?? null;
        if (f) {
          const ext = getExt(f.name);
          if (ext !== "txt" && ext !== "md") {
            setFile(null);
            setError("Only .txt or .md files are allowed.");
            onFileChange?.(null);
            return;
          }
          setFile(f);
          onFileChange?.(f);
          return;
        }

        const r = rejected?.[0];
        if (r) {
          const msg = r.errors.map(e => e.message).join("; ");
          setFile(null);
          setError(msg);
          onFileChange?.(null);
        }
      },
    });


  return (
    <div>
      <div
        {...getRootProps()}
        className={`p-6 border-2 rounded-xl cursor-pointer select-none transition-all ${
          isDragActive
            ? 'border-purple-500 bg-purple-50'
            : isDragReject
            ? 'border-red-300 bg-red-50'
            : 'border-gray-200 bg-gray-50 hover:border-purple-300 hover:bg-purple-50'
        }`}
        style={{
          borderStyle: "dashed",
        }}
      >
        <input {...getInputProps()} />
        <div className="text-center">
          <div className="mb-2">
            <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <p className="text-sm font-semibold text-gray-700">
            {file
              ? `Selected: ${file.name}`
              : isDragReject
              ? "File not accepted"
              : isDragActive
              ? "Drop the file here"
              : "Drag & drop a .txt or .md file"}
          </p>
          <p className="text-xs text-gray-500 mt-1">or click to browse</p>
        </div>
      </div>

      {file && (
        <div className="mt-3 text-sm text-gray-600 bg-purple-50 px-4 py-2 rounded-lg">
          <span className="font-medium">{file.name}</span> — {file.size.toLocaleString()} bytes
          {file.type && <span> — {file.type}</span>}
        </div>
      )}

      {error && (
        <div className="mt-3 text-sm text-red-600 bg-red-50 px-4 py-2 rounded-lg border border-red-200">
          {error}
        </div>
      )}
    </div>
  );
}
