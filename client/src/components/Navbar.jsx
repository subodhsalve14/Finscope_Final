import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const baseUrl = import.meta.env.VITE_API_BASE_URL

  const handleLogout = async () => {
    const response = await fetch(`${baseUrl}/api/auth/logout`, {
        credentials: 'include'
    })
    const data = await response.json()
    if(data.status){
        navigate("/register");
    }
  };

  return (
    <nav className="bg-gray-800 p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-lg font-bold">
          <Link to="/dashboard">Dashboard</Link>
        </div>
        <div>
          <Link to="/about" className="mr-4">
            About
          </Link>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
