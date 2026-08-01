import Loader from "../components/Loader";
import { useEffect, useState } from "react";

function NVR() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <Loader text="Loading NVR..." />;
  }

  return (
    <div className="container-fluid px-4 py-4">
      <h2 className="mb-4">💾 NVR Management</h2>

      <div className="card shadow">
        <div className="card-header bg-dark text-white">
          <h5 className="mb-0">Network Video Recorders</h5>
        </div>

        <div className="card-body">
          <table className="table table-hover align-middle">
            <thead className="table-dark">
              <tr>
                <th>NVR Name</th>
                <th>IP Address</th>
                <th>Status</th>
                <th>Total Cameras</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td colSpan="4" className="text-center text-muted">
                  No NVR Found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default NVR;