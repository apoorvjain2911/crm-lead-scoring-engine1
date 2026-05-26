import React from 'react';

export default function StatsCard({ title, value }) {
  return (
    <div style={{
      padding: "20px",
      border: "1px solid #ddd",
      borderRadius: "10px",
      width: "200px"
    }}>
      <h3>{title}</h3>
      <h1>{value}</h1>
    </div>
  );
}
