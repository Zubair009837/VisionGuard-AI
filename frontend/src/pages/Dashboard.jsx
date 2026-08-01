import AIInsights from "../components/ai/AIInsights";
import Loader from "../components/Loader";
import { useEffect, useState } from "react";
import api from "../services/api";
import StatusCard from "../components/StatusCard";
import CameraPieChart from "../components/charts/CameraPieChart";
import PerformanceChart from "../components/charts/PerformanceChart";
import StorageChart from "../components/charts/StorageChart";

function Dashboard() {
  const [dashboard, setDashboard] = useState({
    total: 0,
    online: 0,
    offline: 0,
    nvr: 0,
  });

  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState("");
  const [error, setError] = useState(false);

  async function loadDashboard() {
    try {
      const response = await api.get("/dashboard");

      setDashboard(response.data);
      setLastUpdated(new Date().toLocaleTimeString());
      setError(false);
    } catch (err) {
      console.log(err);
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(loadDashboard, 30000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <Loader text="Loading Mission Control..." />;
  }

  return (
    <div className="container-fluid px-4 py-4">

      {/* Dashboard Header */}

      <div className="d-flex justify-content-between align-items-center mb-4">

        <div>
          <h2 className="fw-bold text-white">
            🛡 🛡 Tata 1mg NVR Security Operations Center
          </h2>

          <p className="text-secondary mb-0">
            Enterprise CCTV & NVR Monitoring Dashboard
          </p>
        </div>

        <div className="text-end">

          <small className="text-secondary">
            Last Updated
          </small>

          <br />

          <span className="badge bg-primary fs-6">
            {lastUpdated}
          </span>

          <br />

          <button
            className="btn btn-outline-info btn-sm mt-2"
            onClick={loadDashboard}
          >
            🔄 Refresh Dashboard
          </button>

        </div>

      </div>

      {/* Backend Alert */}

      {error && (
        <div className="alert alert-danger shadow-lg border-0 rounded-4">
          <strong>⚠ Unable to connect to Backend</strong>

          <br />

          Dashboard is running in Offline Mode.
        </div>
      )}

      {/* Status Cards */}

      <div className="row g-4">

        <div className="col-lg-3 col-md-6 animate-card card1">
          <StatusCard
            title="Total Cameras"
            value={dashboard.total}
            icon="📹"
            color="#2563eb"
          />
        </div>

        <div className="col-lg-3 col-md-6 animate-card card2">
          <StatusCard
            title="Online Cameras"
            value={dashboard.online}
            icon="🟢"
            color="#16a34a"
          />
        </div>

        <div className="col-lg-3 col-md-6 animate-card card3">
          <StatusCard
            title="Offline Cameras"
            value={dashboard.offline}
            icon="🔴"
            color="#dc2626"
          />
        </div>

        <div className="col-lg-3 col-md-6 animate-card card4">
          <StatusCard
            title="Connected NVR"
            value={dashboard.nvr}
            icon="💾"
            color="#f59e0b"
          />
        </div>

      </div>

      {/* AI Insights + Quick Stats */}
      <div className="row mt-4">

        <div className="col-lg-4">
          <AIInsights />
        </div>

        <div className="col-lg-8">
          <div className="card shadow-lg border-0 h-100">
            <div className="card-body">
              <h4 className="fw-bold mb-3">📊 System Overview</h4>

              <div className="row">
                <div className="col-md-6 mb-3">
                  <div className="alert alert-success">
                    ✅ All Critical Services Running
                  </div>
                </div>

                <div className="col-md-6 mb-3">
                  <div className="alert alert-info">
                    📡 Network Stable
                  </div>
                </div>

                <div className="col-md-6 mb-3">
                  <div className="alert alert-warning">
                    💽 HDD Usage : 61%
                  </div>
                </div>

                <div className="col-md-6 mb-3">
                  <div className="alert alert-primary">
                    🤖 AI Monitoring Active
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
      {/* Charts */}

      <div className="row mt-4">

        <div className="col-lg-6 mb-4">
          <CameraPieChart />
        </div>

        <div className="col-lg-6 mb-4">
          <PerformanceChart />
        </div>

      </div>

      <div className="row">

        <div className="col-12">
          <StorageChart />
        </div>

      </div>      

    </div>
  );
}

export default Dashboard;