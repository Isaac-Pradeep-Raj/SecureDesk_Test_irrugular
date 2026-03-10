import { useState, useEffect } from "react";
import MainLayout from "./layout/MainLayout";
import ChatPage from "./pages/ChatPage";
import LoginPage from "./pages/LoginPage";
import UploadPage from "./pages/UploadPage";
import Approvals from "./pages/Approvals";

function App() {
  const [role, setRole] = useState(
    localStorage.getItem("role")
  );
  const isAdmin = role === "SuperAdmin";

  const [department, setDepartment] = useState(null);

  // simple page switch (temporary routing)
  const [page, setPage] = useState("chat");

  // Auto-select department after login
  useEffect(() => {
    if (role && !department) {
      if (role === "SuperAdmin") {
        setDepartment("HR");
      } else {
        setDepartment(role);
      }
    }
  }, [role, department]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setRole(null);
    setDepartment(null);
    setPage("chat");
  };

  if (!role) {
    return <LoginPage onLogin={setRole} />;
  }

  return (
    <MainLayout
      role={role}
      department={department}
      setDepartment={setDepartment}
      onLogout={handleLogout}
      page={page}
      setPage={setPage}
      isAdmin={isAdmin}
    >
      {page === "chat" && (
        <ChatPage department={department} />
      )}

      {page === "upload" && isAdmin && <UploadPage />}

      {page === "approvals" && <Approvals />}
    </MainLayout>
  );
}

export default App;
