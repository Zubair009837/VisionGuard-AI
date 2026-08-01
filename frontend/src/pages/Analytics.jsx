import Loader from "../components/Loader";
import { useEffect, useState } from "react";

function Analytics() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <Loader text="Loading Analytics..." />;
  }

  return (
    <div className="container-fluid px-4 py-4">

      <h2 className="mb-4">📊 Analytics Dashboard</h2>

      <div className="row">

        <div className="col-md-3 mb-4">
          <div className="card shadow text-center">
            <div className="card-body">
              <h6>Total Alerts</h6>
              <h2 className="text-primary">0</h2>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-4">
          <div className="card shadow text-center">
            <div className="card-body">
              <h6>Online Cameras</h6>
              <h2 className="text-success">0</h2>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-4">
          <div className="card shadow text-center">
            <div className="card-body">
              <h6>Offline Cameras</h6>
              <h2 className="text-danger">0</h2>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-4">
          <div className="card shadow text-center">
            <div className="card-body">
              <h6>Total NVRs</h6>
              <h2 className="text-warning">0</h2>
            </div>
          </div>
        </div>

      </div>

      <div className="card shadow">
        <div className="card-header bg-dark text-white">
          <h5 className="mb-0">Analytics Overview</h5>
        </div>

        <div className="card-body text-center py-5">
          <h5 className="text-muted">
            📈 Charts & Reports Coming Soon
          </h5>

          <p className="text-secondary">
            Camera Health, Storage Usage, Recording Statistics,
            Motion Detection Analytics and Performance Reports
            will be displayed here.
          </p>
        </div>
      </div>

    </div>
  );
}

export default Analytics;