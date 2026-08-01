import "../styles/layout.css";
import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

function Layout({ children }) {
  const location = useLocation();
  const [time, setTime] = useState("");

  useEffect(() => {
    const updateClock = () => {
      setTime(
        new Date().toLocaleTimeString("en-IN", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
    };

    updateClock();

    const interval = setInterval(updateClock, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="layout">

      <aside className="sidebar">

        <div className="logo">
          <h2>🛡 VisionGuard AI</h2>
          <p>TATA 1MG NVR Monitoring</p>
        </div>

        <nav>

          <Link className={location.pathname === "/" ? "active" : ""} to="/">
            🏠 Dashboard
          </Link>

          <Link
            className={location.pathname === "/cameras" ? "active" : ""}
            to="/cameras"
          >
            📹 Cameras
          </Link>

          <Link
            className={location.pathname === "/nvr" ? "active" : ""}
            to="/nvr"
          >
            💾 NVR
          </Link>

          <Link
            className={location.pathname === "/alerts" ? "active" : ""}
            to="/alerts"
          >
            🚨 Alerts
          </Link>

          <Link
            className={location.pathname === "/analytics" ? "active" : ""}
            to="/analytics"
          >
            📊 Analytics
          </Link>

          <Link
            className={location.pathname === "/settings" ? "active" : ""}
            to="/settings"
          >
            ⚙ Settings
          </Link>

        </nav>

      </aside>

      <div className="content">

        <header className="header">

          <h3>VisionGuard AI Dashboard</h3>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "18px",
            }}
          >

            <div
              style={{
                background: "#16a34a",
                padding: "8px 14px",
                borderRadius: "20px",
                fontSize: "13px",
                fontWeight: "600",
              }}
            >
              🟢 Live Monitering
            </div>

            <div
              style={{
                background: "#1e293b",
                padding: "8px 14px",
                borderRadius: "10px",
              }}
            >
              🕒 {time}
            </div>

            <div
              style={{
                position: "relative",
                fontSize: "22px",
                cursor: "pointer",
              }}
            >
              🔔

              <span
                style={{
                  position: "absolute",
                  top: "-8px",
                  right: "-8px",
                  background: "red",
                  color: "#fff",
                  width: "18px",
                  height: "18px",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "11px",
                }}
              >
                3
              </span>

            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                background: "#1e293b",
                padding: "8px 14px",
                borderRadius: "12px",
              }}
            >
              <div
                style={{
                  width: "38px",
                  height: "38px",
                  borderRadius: "50%",
                  background: "#2563eb",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  fontWeight: "bold",
                }}
              >
                A
              </div>

              <div>
                <div style={{ fontWeight: "600" }}>Admin</div>
                <small style={{ color: "#94a3b8" }}>
                  System Administrator
                </small>
              </div>

            </div>

          </div>

        </header>

        <main className="main">
          {children}
        </main>

      </div>

    </div>
  );
}

export default Layout;