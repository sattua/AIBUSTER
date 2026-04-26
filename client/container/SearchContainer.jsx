import React, { useState } from "react";
import { gql } from "@apollo/client";
import { useQuery } from "@apollo/client/react";
import ResultCard from "../component/ResultCard";
import Pagination from "../component/Pagination";

export const GET_SEARCHES = gql`
  query GetSearches {
    searches {
      id
      query
      createdAt
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

const ITEMS_PER_PAGE = 10;

export default function SearchContainer() {
  const { loading, error, data } = useQuery(GET_SEARCHES);
  const [currentPage, setCurrentPage] = useState(1);

  if (loading) return <p className="text-center mt-4">Loading searches...</p>;
  if (error) return <p className="text-danger text-center">Error 😢 {error.message}</p>;

  const searches = data?.searches || [];
console.dir("container",searches);
  const totalPages = Math.ceil(searches.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const currentItems = searches.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  return (
    <div className="container mt-4">
      <h2 className="mb-4 text-center">Search History</h2>

      <div className="row">
        {currentItems.map((s) => (
          <div key={s.id} className="col-md-6">
            <div className="mb-4">
              {/* Header adicional del search */}
              <div className="mb-2">
                <h6 className="fw-bold">{s.query}</h6>
                <small className="text-muted">
                  {new Date(s.createdAt).toLocaleString()}
                </small>
              </div>

              <ResultCard result={s.result} />
            </div>
          </div>
        ))}
      </div>

      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
      />
    </div>
  );
}