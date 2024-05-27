import React from "react";

const LoadingGrow = () => {
  return (
    <div className="d-flex justify-content-center vh-100 align-items-center">
      <div className="spinner-grow text-light" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
};

export default LoadingGrow;
