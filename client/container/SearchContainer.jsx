import React from "react";
import { gql } from "@apollo/client";
import { useQuery } from "@apollo/client/react";

export const GET_SEARCHES = gql`
  query GetSearches {
    searches {
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

export default function SearchContainer() {
  const { loading, error, data } = useQuery(GET_SEARCHES);

  if (loading) return <p>Loading searches...</p>;
  if (error) return <p>Error 😢 {error.message}</p>;

  return (
    <div>
      <h2>Search History</h2>

      <ul>
        {data?.searches?.map((s) => (
          <li key={s.id}>
            <strong>{s.query}</strong>
            <p>Risk: {s.result?.risk_score}</p>

            <ul>
              {s.result?.findings?.map((f, i) => (
                <li key={i}>
                  {f.type} → {f.sentence}
                </li>
              ))}
            </ul>

            <small>{s.createdAt}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}