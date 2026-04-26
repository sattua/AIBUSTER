import React from "react";

export default function AnalyzeInput({ text, setText, onSubmit, loading }) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-body">
        <div className="mb-3">
          <textarea
            id="analyzeInputId"
            className="form-control"
            rows={4}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type or paste a prompt... (Shift+Enter for new line)"
          />
        </div>

        <div className="d-flex justify-content-end">
          <button
            className="btn btn-primary px-4"
            onClick={onSubmit}
            disabled={loading || !text.trim()}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
      </div>
    </div>
  );
}