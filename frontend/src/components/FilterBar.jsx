import React from 'react';

export default function FilterBar({ onFilter }) {
  const [q, setQ] = React.useState('');
  return (
    <div className="filter-bar">
      <input
        placeholder="Search"
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />
      <button onClick={() => onFilter && onFilter(q)}>Apply</button>
    </div>
  );
}
