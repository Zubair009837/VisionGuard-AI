import Loader from "../components/Loader";
import { useEffect, useState } from "react";
import api from "../services/api";

export default function Cameras() {
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCameras();
  }, []);

  async function loadCameras() {
    try {
      const response = await api.get("/cameras");
      setCameras(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <Loader text="Loading Cameras..." />;
  }

  return (
    <div className="container-fluid px-4 py-4">
      <h2 className="mb-4">📹 Camera Management</h2>

      <div className="card shadow">
        <div className="card-header bg-dark text-white">
          <h5 className="mb-0">Camera List</h5>
        </div>

        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover align-middle">
              <thead className="table-dark">
                <tr>
                  <th>ID</th>
                  <th>Camera Name</th>
                  <th>Status</th>
                  <th>NVR</th>
                  <th>IP Address</th>
                </tr>
              </thead>

              <tbody>
                {cameras.length > 0 ? (
                  cameras.map((camera) => (
                    <tr key={camera.id}>
                      <td>{camera.id}</td>
                      <td>{camera.name}</td>

                      <td>
                        <span
                          className={`badge ${
                            camera.status === "Online"
                              ? "bg-success"
                              : "bg-danger"
                          }`}
                        >
                          {camera.status}
                        </span>
                      </td>

                      <td>{camera.nvr}</td>
                      <td>{camera.ip}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="text-center text-muted">
                      No Cameras Found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}