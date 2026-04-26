import React from "react";

const getRiskColor = (score = 0) => {
  if (score >= 0.7) return "danger";
  if (score >= 0.4) return "warning";
  return "success";
};

function highlightText(sentence, start, end) {
  if (
    typeof start !== "number" ||
    typeof end !== "number" ||
    start < 0 ||
    end > sentence.length
  ) {
    return sentence;
  }

  const before = sentence.slice(0, start);
  const match = sentence.slice(start, end);
  const after = sentence.slice(end);

  return (
    <>
      {before}
      <span className="text-danger fw-bold">{match}</span>
      {after}
    </>
  );
}

export default function ResultCard({ result }) {
  if (!result) return null;

console.dir(result);

  const score = result?.riskScore ?? 0;

  return (
    <div className="card shadow-sm mb-5">
      <div className="card-body">
        <h5 className="card-title">Result</h5>

        <p>
          <strong>Risk Score: </strong>
          <span className={`badge bg-${getRiskColor(score)}`}>
            {score}
          </span>
        </p>

        <ul className="list-group list-group-flush">
          {result?.findings?.map((f, i) => (
            <li key={i} className="list-group-item">
              <strong>{f.type}</strong>:{" "}
              {highlightText(f.sentence, f.start, f.end)}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}