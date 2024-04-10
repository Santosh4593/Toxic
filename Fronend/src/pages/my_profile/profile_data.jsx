import React, { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";



const MyProfile = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);

  const handleLogout = () => {
    Cookies.remove("bearerToken");
    navigate("/auth/Login");
  };

  useEffect(() => {
    const token = Cookies.get("bearerToken");

    if (!token) {
      navigate("/auth/Login");
      return;
    }

    fetch("http://127.0.0.1:8000/user_data", {
      method: "GET",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data && Array.isArray(data.data) && data.data.length > 0) {
          setUserData(data.data[0]);
        } else {
          console.error("Invalid data structure or empty data array");
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [navigate]);

  if (!userData) {
    return <p>Loading...</p>; // Or handle this as needed
  }


  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="bg-white shadow-2xl rounded-lg p-8 text-center mb-4">
        <div className="mb-4">
          <img
            src="profile_avtar.png"
            alt="Avatar"
            className="w-20 h-20 rounded-full mx-auto mb-2"
          />
          <span className="text-xl font-bold">{userData.username}</span>
          {userData.total_points && (
            <p>
              Total Points: <strong>{userData.total_points}</strong>
            </p>
          )}

        </div>
        <div className="text-left">
          <h2 className="text-lg font-semibold mt-6">Your History</h2>
          <div className="max-h-40 overflow-y-auto mt-4">
            {userData && (
              <div>
                <p>
                  Total Score: <strong>{userData.total_score}</strong>
                </p>
                <p>
                  Mental Health: <strong>{userData.mental_health}</strong>
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
      <button
        className="bg-cyan-500 hover:bg-cyan-500 text-black font-semibold py-2 px-4 rounded"
        onClick={handleLogout}
      >
        Logout
      </button>
    </div>
  );
};

export default MyProfile;
