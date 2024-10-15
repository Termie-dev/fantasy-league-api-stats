import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState(null);
  const [leagueId, setLeagueId] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`/api/leaguestats?league_id=${leagueId}`)
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error('Error fetching data:', error));
  };

  return (
    <div>
      <h1>Fantasy Football Stats</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter League ID"
          value={leagueId}
          onChange={(e) => setLeagueId(e.target.value)}
        />
        <button type="submit">Get Stats</button>
      </form>
      
      {data && (
        <div>
          <h2>Stats for League {leagueId}</h2>
          {/* Display wins/losses, average points, etc. */}
          <p>Wins: {data.wins}</p>
          <p>Losses: {data.losses}</p>
          <p>Average Points: {data.avg_points}</p>
        </div>
      )}
    </div>
  );
}

export default App;
