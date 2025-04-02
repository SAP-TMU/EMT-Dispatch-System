// src/components/Sidebar.js

import React from "react";

const Sidebar = ({ title, items }) => {
  return (
    <aside className="bg-gray-100 p-4 w-64 h-full shadow">
      <h2 className="text-xl font-bold mb-4">{title}</h2>
      <ul className="space-y-2 text-sm">
        {items.map((item, index) => (
          <li key={index} className="p-2 bg-white rounded shadow">
            {item}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
