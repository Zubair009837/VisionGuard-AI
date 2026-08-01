import { Link } from "react-router-dom";
import {
  FaHome,
  FaVideo,
  FaServer,
  FaBell,
  FaCog,
  FaChartBar,
} from "react-icons/fa";
import "./Sidebar.css";

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>🛡 VisionGuard AI</h2>

      <Link to="/">
        <FaHome /> Dashboard
      </Link>

      <Link to="/cameras">
        <FaVideo /> Cameras
      </Link>

      <Link to="/nvr">
        <FaServer /> NVR
      </Link>

      <Link to="/alerts">
        <FaBell /> Alerts
      </Link>

      <Link to="/analytics">
        <FaChartBar /> Analytics
      </Link>

      <Link to="/settings">
        <FaCog /> Settings
      </Link>
    </div>
  );
}

export default Sidebar;