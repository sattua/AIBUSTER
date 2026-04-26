import React from "react";

export default function Pagination({ currentPage, totalPages, onPageChange }) {
  return (
    <nav className="d-flex justify-content-center mt-4">
      <ul className="pagination">
        <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
          <button
            className="page-link"
            onClick={() => onPageChange(currentPage - 1)}
          >
            Previous
          </button>
        </li>

        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <li
            key={page}
            className={`page-item ${currentPage === page ? "active" : ""}`}
          >
            <button
              className="page-link"
              onClick={() => onPageChange(page)}
            >
              {page}
            </button>
          </li>
        ))}

        <li className={`page-item ${currentPage === totalPages ? "disabled" : ""}`}>
          <button
            className="page-link"
            onClick={() => onPageChange(currentPage + 1)}
          >
            Next
          </button>
        </li>
      </ul>
    </nav>
  );
}