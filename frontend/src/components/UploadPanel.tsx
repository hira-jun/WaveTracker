import { useState } from "react";

interface UploadPanelProps {
  disabled: boolean;
  selectedPoint: { xNorm: number; yNorm: number } | null;
  onUpload: (file: File, location: { xNorm: number; yNorm: number }) => Promise<void>;
}

export function UploadPanel({ disabled, selectedPoint, onUpload }: UploadPanelProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <section style={{ display: "grid", gap: "0.5rem" }}>
      <h2 style={{ margin: 0, fontSize: "1.1rem" }}>Upload Survey ZIP</h2>
      <p style={{ margin: 0, color: "#555" }}>
        Upload location: {selectedPoint ? `${selectedPoint.xNorm.toFixed(3)}, ${selectedPoint.yNorm.toFixed(3)}` : "select a point on the map"}
      </p>
      <input
        type="file"
        accept=".zip"
        disabled={disabled || uploading}
        onChange={(event) => {
          setError(null);
          setSelectedFile(event.target.files?.[0] ?? null);
        }}
      />
      <button
        type="button"
        disabled={disabled || uploading || selectedFile == null || selectedPoint == null}
        onClick={async () => {
          if (selectedFile == null || selectedPoint == null) {
            return;
          }
          setUploading(true);
          setError(null);
          try {
            await onUpload(selectedFile, selectedPoint);
            setSelectedFile(null);
          } catch (uploadError) {
            setError(uploadError instanceof Error ? uploadError.message : "Upload failed");
          } finally {
            setUploading(false);
          }
        }}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>
      {error && <p style={{ margin: 0, color: "#b42318" }}>{error}</p>}
    </section>
  );
}
