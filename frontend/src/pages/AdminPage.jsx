// src/pages/AdminPage.js

import React from "react";
import PinForm from "../components/PinForm";
import PinnedItems from "../components/PinnedItems";
import { Link } from "react-router-dom";

const AdminPage = () => {
    return (
        <div className="container mx-auto p-4">
                <h1 className="text-2xl font-bold mb-4">Admin Console</h1>
                <Link to="/" className="px-4 py-2 bg-gray-300 text-black rounded hover:bg-gray-400">
                    Back to Chat
                </Link>
            <PinForm onRefresh={() => window.location.reload()} />
            <PinnedItems isAdmin={true} />
        </div>
    );
};

export default AdminPage;
