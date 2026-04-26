import React from "react";
import { gql, useQuery } from "@apollo/client";

const GET_SEARCHES = gql`
  query GetSearches {
    searches {
      id
      query
      result {
        riskScore
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

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error 😢</p>;

  return (
    <ul>
      {data.searches.map((s) => (
        <li key={s.id}>
          <strong>{s.query}</strong>
          <p>Risk: {s.result?.riskScore}</p>

          <ul>
            {s.result?.findings?.map((f, i) => (
              <li key={i}>
                {f.type} → {f.sentence}
              </li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
}