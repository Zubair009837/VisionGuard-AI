import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaVideo,
  FaServer,
  FaBell,
  FaCog,
  FaChartBar,
  FaMapMarkedAlt,
  FaDatabase,
  FaUsers,
  FaFileAlt,
  FaBroadcastTower,
} from "react-icons/fa";
import "./Sidebar.css";

function Sidebar() {
  const menuItems = [
    { name: "Dashboard", icon: <FaHome />, path: "/" },
    { name: "Live View", icon: <FaBroadcastTower />, path: "/live" },
    { name: "Cameras", icon: <FaVideo />, path: "/cameras" },
    { name: "NVR", icon: <FaServer />, path: "/nvr" },
    { name: "Alerts", icon: <FaBell />, path: "/alerts" },
    { name: "Analytics", icon: <FaChartBar />, path: "/analytics" },
    { name: "Floor Map", icon: <FaMapMarkedAlt />, path: "/floor-map" },
    { name: "Storage", icon: <FaDatabase />, path: "/storage" },
    { name: "Users", icon: <FaUsers />, path: "/users" },
    { name: "Reports", icon: <FaFileAlt />, path: "/reports" },
    { name: "Settings", icon: <FaCog />, path: "/settings" },
  ];

  return (
    <aside className="sidebar">

      <div className="logo-section">
        <div className="logo-circle">🛡</div>

        <div>
          <h2>VisionGuard AI</h2>
          <span>Enterprise Monitoring</span>
        </div>
      </div>

      <nav className="menu">
        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "menu-item active" : "menu-item"
            }
          >
            <span className="icon">{item.icon}</span>
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="status-dot"></div>
        <span>System Online</span>
      </div>

    </aside>
  );
}

export default Sidebar;