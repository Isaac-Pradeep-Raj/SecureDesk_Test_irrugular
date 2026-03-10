function Sidebar({ role, setDepartment, setPage }) {

  const menuByRole = {
    HR: [
      { name: "HR Policies", dept: "HR" },
      { name: "Employee Records", dept: "HR" },
    ],
    DEV: [
      { name: "Dev Docs", dept: "DEV" },
      { name: "Deployment Guide", dept: "DEV" },
    ],
    IT: [
      { name: "Infrastructure", dept: "IT" },
      { name: "Network SOP", dept: "IT" },
    ],
    Security: [
      { name: "Security Policies", dept: "Security" },
    ],
    SuperAdmin: [
      { name: "HR Policies", dept: "HR" },
      { name: "Dev Docs", dept: "DEV" },
      { name: "Infrastructure", dept: "IT" },
      { name: "Security Policies", dept: "Security" },
    ],
  };

  const menuItems = menuByRole[role] || [];

  return (
    <div className="w-64 bg-gray-900 text-white h-screen p-4 flex flex-col justify-between">
      <div>
        <h1 className="text-xl font-bold mb-6">SecureDesk</h1>

        <p className="text-xs text-gray-400 mb-4">
          Logged as: {role}
        </p>

        <ul className="space-y-3">
          {menuItems.map((item) => (
            <li
              key={item.name}
              onClick={() => {
                setDepartment(item.dept);
                setPage("chat");
              }}
              className="p-2 rounded hover:bg-gray-700 cursor-pointer"
            >
              {item.name}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <ul className="space-y-3 border-t border-gray-700 pt-4">
          <li
            onClick={() => setPage("approvals")}
            className="p-2 rounded bg-blue-600 hover:bg-blue-700 cursor-pointer text-center font-semibold"
          >
            Approvals
          </li>
        </ul>
      </div>
    </div>
  );
}

export default Sidebar;