import Loader from "../components/Loader";
import { useEffect, useState } from "react";

function Alerts() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <Loader text="Loading Alerts..." />;
  }

  return (
    <div className="container-fluid px-4 py-4">
      <h2 className="mb-4">🚨 Alert Management</h2>

      <div className="card shadow">
        <div className="card-header bg-danger text-white">
          <h5 className="mb-0">Recent Alerts</h5>
        </div>

        <div className="card-body">
          <table className="table table-hover align-middle">
            <thead className="table-dark">
              <tr>
                <th>Time</th>
                <th>Camera</th>
                <th>Alert Type</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td colSpan="4" className="text-center text-muted">
                  No Alerts Found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Alerts;