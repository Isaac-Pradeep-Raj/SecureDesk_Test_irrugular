function Topbar({
  role,
  department,
  onLogout,
  page,
  setPage,
  isAdmin,
}) {
  return (
    <div className="h-14 bg-white shadow flex items-center justify-between px-6">
      <div>
        <h2 className="font-semibold text-gray-700">
          SecureDesk Assistant
        </h2>

        <p className="text-xs text-gray-500">
          Active Domain: {department || "General"}
        </p>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={() => setPage("chat")}
          className={`px-3 py-1 rounded ${
            page === "chat"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
        >
          Chat
        </button>

        {isAdmin && (
          <button
            onClick={() => setPage("upload")}
            className={`px-3 py-1 rounded ${
              page === "upload"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            Upload
          </button>
        )}

        <span className="text-sm text-gray-600">
          Role: {role}
        </span>

        <button
          onClick={onLogout}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Topbar;
