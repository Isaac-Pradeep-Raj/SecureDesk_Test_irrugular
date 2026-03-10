import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function MainLayout({
  children,
  role,
  department,
  setDepartment,
  onLogout,
  page,
  setPage,
  isAdmin,
}) {
  return (
    <div className="flex">
      <Sidebar
        role={role}
        setDepartment={setDepartment}
        setPage={setPage}
      />

      <div className="flex-1 flex flex-col h-screen">
        <Topbar
          role={role}
          department={department}
          onLogout={onLogout}
          page={page}
          setPage={setPage}
          isAdmin={isAdmin}
        />

        <main className="flex-1 bg-gray-100 p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}

export default MainLayout;
