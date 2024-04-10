import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboardData, setLeaderboardData] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/leaderboard')
      .then((response) => response.json())
      .then((data) => setLeaderboardData(data.message))
      .catch((error) => console.error('Error fetching leaderboard:', error));
  }, []);

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="bg-white shadow-md rounded-lg p-8 text-center w-3/4">
        <h1 className="text-3xl font-bold mb-4">Leaderboard</h1>
        <div className="text-left">
          <div className="grid grid-cols-4 gap-6">
            <div className="font-semibold">No</div>
            <div className="font-semibold">Username</div>
            <div className="font-semibold">Total Point</div>
            <div className="font-semibold">Language</div>
            {leaderboardData.map((user, index) => (
              <React.Fragment key={index}>
                <div>{index + 1}</div>
                <div>{user.username}</div>
                <div>{user.total_points}</div>
                <div>English</div>
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
