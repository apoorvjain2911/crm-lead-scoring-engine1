import React from 'react';

export default function LeadsTable({ leads = [] }) {
  return (
    <table border="1" width="100%">
      <thead>
        <tr>
          <th>ID</th>
          <th>Industry</th>
          <th>Score</th>
          <th>Category</th>
        </tr>
      </thead>

      <tbody>
        {leads.map((lead, index) => (
          <tr key={index}>
            <td>{lead.id}</td>
            <td>{lead.industry}</td>
            <td>{lead.score}</td>
            <td>{lead.category}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
