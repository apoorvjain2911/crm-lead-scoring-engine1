import './App.css';
import { useEffect, useRef, useState } from 'react';
import {
  getAllLeads,
  getStats,
  getHotLeads,
  getWarmLeads,
  getColdLeads,
  uploadLeadsCsv,
} from './api/leads';

export default function App() {
  const [stats, setStats] = useState(null);
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState(null);
  const [uploadTone, setUploadTone] = useState('success');
  const fileInputRef = useRef(null);

  const statsCards = [
    {
      title: 'Total Leads',
      value: stats?.total_leads ?? '-',
      hint: 'All records in CRM',
      tone: 'neutral',
    },
    {
      title: 'Hot Leads',
      value: stats?.hot_leads ?? '-',
      hint: 'Ready for outreach',
      tone: 'hot',
    },
    {
      title: 'Warm Leads',
      value: stats?.warm_leads ?? '-',
      hint: 'Need nurturing',
      tone: 'warm',
    },
    {
      title: 'Cold Leads',
      value: stats?.cold_leads ?? '-',
      hint: 'Low engagement',
      tone: 'cold',
    },
  ];

  const categoryCounts = leads.reduce(
    (acc, lead) => {
      const category = lead.category || 'Unknown';
      acc[category] = (acc[category] || 0) + 1;
      return acc;
    },
    { Hot: 0, Warm: 0, Cold: 0 },
  );

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [leadsRes, statsRes] = await Promise.all([getAllLeads(), getStats()]);
      setLeads(leadsRes.data.leads || []);
      setStats(statsRes.data || {});
    } catch (err) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = async (type) => {
    setFilter(type);
    setLoading(true);
    setError(null);
    try {
      let res;
      if (type === 'hot') res = await getHotLeads();
      else if (type === 'warm') res = await getWarmLeads();
      else if (type === 'cold') res = await getColdLeads();
      else res = await getAllLeads();

      setLeads(res.data.leads || []);
    } catch (err) {
      setError('Failed to load filtered leads');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (!file.name.toLowerCase().endsWith('.csv')) {
      setUploadMessage('Please choose a .csv file.');
      setUploadTone('error');
      event.target.value = '';
      return;
    }

    setUploading(true);
    setError(null);
    setUploadMessage(null);
    setUploadTone('success');

    try {
      const response = await uploadLeadsCsv(file);
      const totalLeads = response.data?.total_leads ?? 0;
      const savedLeads = response.data?.saved_leads ?? 0;
      const duplicateLeads = response.data?.duplicate_leads ?? 0;

      if (duplicateLeads > 0) {
        setUploadTone('warning');
      }

      setUploadMessage(
        `Uploaded successfully. Processed ${totalLeads} leads: ${savedLeads} saved, ${duplicateLeads} duplicate${duplicateLeads === 1 ? '' : 's'} skipped.`,
      );
      await loadData();
      setFilter('all');
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(detail || 'Failed to upload CSV');
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const getBadgeColor = (category) => {
    if (category === 'Hot') return 'bg-red-100 text-red-600';
    if (category === 'Warm') return 'bg-yellow-100 text-yellow-700';
    return 'bg-blue-100 text-blue-700';
  };

  return (
    <div className="dashboard-shell">
      <div className="dashboard-bg" />

      <main className="dashboard-app">
        <header className="dashboard-hero">
          <div className="hero-copy">
            <div className="eyebrow">Lead scoring studio</div>
            <h1>AI CRM Dashboard</h1>
            <p>
              A cleaner command center for reviewing lead quality, filtering audiences,
              and uploading new CSV batches.
            </p>

            <div className="hero-metrics">
              <div>
                <span>{stats?.avg_score ?? '-'}</span>
                <label>Average score</label>
              </div>
              <div>
                <span>{stats?.hot_percentage ?? '-'}%</span>
                <label>Hot share</label>
              </div>
              <div>
                <span>{leads.length}</span>
                <label>Visible rows</label>
              </div>
            </div>
          </div>

          <section className="hero-panel">
            <div className="hero-panel-top">
              <div>
                <p>Current filter</p>
                <strong>{filter.charAt(0).toUpperCase() + filter.slice(1)}</strong>
              </div>
              <button
                type="button"
                onClick={handleUploadClick}
                disabled={uploading}
                className="upload-button"
              >
                {uploading ? 'Uploading...' : 'Upload CSV'}
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv,text/csv"
                className="sr-only-input"
                onChange={handleFileChange}
              />
            </div>

            <div className="hero-panel-grid">
              <div>
                <span>Hot</span>
                <strong>{categoryCounts.Hot}</strong>
              </div>
              <div>
                <span>Warm</span>
                <strong>{categoryCounts.Warm}</strong>
              </div>
              <div>
                <span>Cold</span>
                <strong>{categoryCounts.Cold}</strong>
              </div>
              <div>
                <span>Status</span>
                <strong>{loading ? 'Syncing' : 'Live'}</strong>
              </div>
            </div>

            {uploadMessage ? <div className={`status-banner ${uploadTone}`}>{uploadMessage}</div> : null}
            {error ? <div className="status-banner error">{error}</div> : null}
          </section>
        </header>

        <section className="stats-grid">
          {statsCards.map((card) => (
            <article key={card.title} className={`stat-card tone-${card.tone}`}>
              <div className="stat-card-head">
                <p>{card.title}</p>
                <span>{card.hint}</span>
              </div>
              <h2>{card.value}</h2>
            </article>
          ))}
        </section>

        <section className="toolbar">
          <div>
            <h3>Lead segments</h3>
            <p>Switch between lead pools without losing the overview.</p>
          </div>

          <div className="filter-group">
            <button onClick={() => handleFilter('all')} className={filter === 'all' ? 'filter-chip active' : 'filter-chip'}>All</button>
            <button onClick={() => handleFilter('hot')} className={filter === 'hot' ? 'filter-chip active hot' : 'filter-chip hot'}>Hot</button>
            <button onClick={() => handleFilter('warm')} className={filter === 'warm' ? 'filter-chip active warm' : 'filter-chip warm'}>Warm</button>
            <button onClick={() => handleFilter('cold')} className={filter === 'cold' ? 'filter-chip active cold' : 'filter-chip cold'}>Cold</button>
          </div>
        </section>

        <section className="table-card">
          <div className="table-card-head">
            <div>
              <h2>Leads Table</h2>
              <p>Showing the latest loaded records from the CRM backend.</p>
            </div>
            <div className="table-badge">{loading ? 'Refreshing' : `${leads.length} rows`}</div>
          </div>

          <div className="table-wrap">
            {loading ? (
              <div className="empty-state">Loading leads...</div>
            ) : error ? (
              <div className="empty-state error-state">{error}</div>
            ) : leads.length === 0 ? (
              <div className="empty-state">No leads available yet. Upload a CSV to populate the table.</div>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Industry</th>
                    <th>Score</th>
                    <th>Category</th>
                  </tr>
                </thead>

                <tbody>
                  {leads.map((lead) => (
                    <tr key={lead.id}>
                      <td>#{lead.id}</td>
                      <td>{lead.industry}</td>
                      <td className="score-cell">{lead.score}</td>
                      <td>
                        <span className={`category-pill ${getBadgeColor(lead.category)}`}>
                          {lead.category}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
