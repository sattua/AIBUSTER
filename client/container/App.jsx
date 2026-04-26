import React, { useState, useCallback } from "react";
import { gql } from "@apollo/client";
import { useMutation } from "@apollo/client/react";

import AnalyzeInput from "../component/AnalyzeInput";
import ResultCard from "../component/ResultCard";
import SearchContainer from "./SearchContainer";

const ANALYZE = gql`
  mutation($content: String!) {
    analyzeDocument(content: $content) {
      id
      query
      result {
        riskScore
        findings {
          type
          sentence
          match
          start
          end
        }
      }
    }
  }
`;

export default function App() {
  const [text, setText] = useState("");

  const [analyze, { data, loading, error }] = useMutation(ANALYZE, {
    update(cache, { data }) {
      if (!data?.analyzeDocument) return;

      cache.modify({
        fields: {
          searches(existing = []) {
            return [data.analyzeDocument, ...existing];
          },
        },
      });
    },
  });

  const handleAnalyze = useCallback(() => {
    if (!text.trim()) return;
    analyze({ variables: { content: text } });
  }, [text, analyze]);

  return (
    <div className="container py-5">

      <div className="text-center mb-5">
        <h1 className="fw-bold">🚨 AI BUSTER</h1>
        <p className="text-muted">
          Analyze prompts for sensitive data exposure
        </p>
      </div>

      <AnalyzeInput
        text={text}
        setText={setText}
        onSubmit={handleAnalyze}
        loading={loading}
      />

      {error && (
        <div className="alert alert-danger">
          {error.message}
        </div>
      )}

      <ResultCard result={data?.analyzeDocument?.result} />

      <SearchContainer />
    </div>
  );
}