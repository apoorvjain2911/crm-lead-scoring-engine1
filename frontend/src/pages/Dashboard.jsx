import { useEffect, useState } from "react";
import {
  getAllLeads,
  getStats,
  getHotLeads,
  getWarmLeads,
  getColdLeads,
} from "../api/leads";

import StatsCard from "../components/StatsCard";
import LeadsTable from "../components/LeadsTable";

export default function Dashboard() {
  const [leads, setLeads] = useState([]);
  const [stats, setStats] = useState({});
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const res = await getAllLeads();
    const statsRes = await getStats();

    setLeads(res.data.leads);
    setStats(statsRes.data);
  };

  const handleFilter = async (type) => {
    setFilter(type);

    let res;
    if (type === "hot") res = await getHotLeads();
    else if (type === "warm") res = await getWarmLeads();
    else if (type === "cold") res = await getColdLeads();
    else res = await getAllLeads();

    setLeads(res.data.leads);
  };

  return (
    <div style={{ padding: "20px" }}>

      {/* STATS */}
      <div style={{ display: "flex", gap: "20px" }}>
        <StatsCard title="Total" value={stats.total_leads} />
        <StatsCard title="Hot" value={stats.hot_leads} />
        <StatsCard title="Warm" value={stats.warm_leads} />
        <StatsCard title="Cold" value={stats.cold_leads} />
      </div>

      <br />

      {/* FILTERS */}
      <div>
        <button onClick={() => handleFilter("all")}>All</button>
        <button onClick={() => handleFilter("hot")}>Hot</button>
        <button onClick={() => handleFilter("warm")}>Warm</button>
        <button onClick={() => handleFilter("cold")}>Cold</button>
      </div>

      <br />

      {/* TABLE */}
      <LeadsTable leads={leads} />

    </div>
  );
}
