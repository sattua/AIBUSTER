import React, { useState } from "react";
import SearchContainer from "./SearchContainer";
import { GET_SEARCHES } from "./SearchContainer";
import { gql } from "@apollo/client";
import { useQuery, useMutation } from "@apollo/client/react";

const ANALYZE = gql`
  mutation($content: String!) {
    analyzeDocument(content: $content) {
      id
      query
      result {
        risk_score
        findings {
          type
          sentence
        }
      }
    }
  }
`;

export default function App() {
  const [text, setText] = useState("");
  const [analyze, { data, loading, error }] = useMutation(ANALYZE, {
  refetchQueries: [
    {
      query: GET_SEARCHES,
    },
  ],
});

  const handleAnalyze = () => {
    analyze({ variables: { content: text } });
  };

  return (
    <div>
      <h1>AI BUSTER</h1>

      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Write a prompt..."
      />

      <button onClick={handleAnalyze}>Analyze</button>

      {loading && <p>Analyzing...</p>}
      {error && <pre>{error.message}</pre>}

      {data && (
        <div>
          <p>Risk Score: {data.analyzeDocument.result?.risk_score}</p>

          <ul>
            {data.analyzeDocument.result?.findings?.map((f, i) => (
              <li key={i}>
                {f.type} → {f.sentence}
              </li>
            ))}
          </ul>
        </div>
      )}

      <hr />

      <SearchContainer />
    </div>
  );
}