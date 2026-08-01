import Loader from "../components/Loader";
import { useEffect, useState } from "react";

function Settings() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <Loader text="Loading Settings..." />;
  }

  return (
    <div className="container-fluid px-4 py-4">
      <h2 className="mb-4">⚙ System Settings</h2>

      <div className="card shadow">
        <div className="card-header bg-dark text-white">
          <h5 className="mb-0">Configuration</h5>
        </div>

        <div className="card-body">
          <div className="mb-3">
            <label className="form-label">Application Name</label>
            <input
              type="text"
              className="form-control"
              value="VisionGuard AI"
              readOnly
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Backend Status</label>
            <input
              type="text"
              className="form-control"
              value="Connected"
              readOnly
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Refresh Interval</label>
            <input
              type="text"
              className="form-control"
              value="30 Seconds"
              readOnly
            />
          </div>

          <button className="btn btn-primary">
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}

export default Settings;