// src/components/AdminToggle.js

import React, { useState } from "react";

const AdminToggle = ({ onToggle }) => {
  const [isAdmin, setIsAdmin] = useState(false);

  const toggleAdminMode = () => {
    setIsAdmin(!isAdmin);
    onToggle(!isAdmin);
  };

  return (
    <div className="text-center my-4">
      <button
        onClick={toggleAdminMode}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        {isAdmin ? "Exit Admin Mode" : "Enter Admin Mode"}
      </button>
    </div>
  );
};

export default AdminToggle;
