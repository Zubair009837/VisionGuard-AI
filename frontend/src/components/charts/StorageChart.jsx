import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

function StorageChart() {

  const data = [
    { drive: "Disk-1", used: 70 },
    { drive: "Disk-2", used: 48 },
    { drive: "Disk-3", used: 83 },
    { drive: "Disk-4", used: 55 },
  ];

  return (
    <div
      className="card border-0 shadow-lg mt-4"
      style={{
        background: "#111827",
        borderRadius: "18px",
      }}
    >
      <div className="card-body">

        <h5
          className="fw-bold mb-3"
          style={{ color: "#fff" }}
        >
          💽 HDD Storage
        </h5>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>

            <XAxis
              dataKey="drive"
              stroke="#9ca3af"
            />

            <YAxis stroke="#9ca3af" />

            <Tooltip />

            <Bar
              dataKey="used"
              fill="#f59e0b"
              radius={[8, 8, 0, 0]}
            />

          </BarChart>
        </ResponsiveContainer>

      </div>
    </div>
  );
}

export default StorageChart;