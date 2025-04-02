// src/components/InfoCard.js

import React from "react";

const InfoCard = ({ title, children }) => {
  return (
    <div className="bg-white rounded-lg shadow p-4 w-full max-w-md mb-4">
      <h2 className="text-lg font-bold mb-2">{title}</h2>
      <div>{children}</div>
    </div>
  );
};

export default InfoCard;
