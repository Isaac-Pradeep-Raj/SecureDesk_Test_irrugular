import { useState, useEffect } from "react";

function Approvals() {
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchRequests = async () => {
        setLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem("token");
            const res = await fetch("http://localhost:5000/api/access/requests", {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            if (!res.ok) throw new Error("Failed to fetch requests");
            const data = await res.json();
            setRequests(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRequests();
    }, []);

    const handleApprove = async (id) => {
        try {
            const token = localStorage.getItem("token");
            const res = await fetch("http://localhost:5000/api/access/approve", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ request_id: id })
            });
            if (res.ok) {
                alert("Request approved for 1 minute.");
                fetchRequests(); // Refresh the list
            } else {
                const data = await res.json();
                alert(data.msg || "Failed to approve");
            }
        } catch (err) {
            alert("Error approving request: " + err.message);
        }
    };

    if (loading) return <div className="p-4">Loading requests...</div>;
    if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

    return (
        <div className="p-6 bg-white rounded shadow min-h-full">
            <h2 className="text-2xl font-bold mb-4">Pending Access Requests</h2>
            {requests.length === 0 ? (
                <p className="text-gray-500">No pending requests at this time.</p>
            ) : (
                <div className="space-y-4">
                    {requests.map(req => (
                        <div key={req.id} className="border p-4 rounded bg-gray-50 flex justify-between items-center">
                            <div>
                                <p className="text-lg font-semibold text-gray-800">Department: <span className="text-blue-600">{req.requester_role}</span></p>
                                <p className="text-sm text-gray-600">Asking for: {req.classification} access to {req.target_domain}</p>
                                <p className="text-xs text-gray-400 mt-1">Requested at: {req.created_at}</p>
                            </div>
                            <button
                                onClick={() => handleApprove(req.id)}
                                className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded transition-colors"
                            >
                                Grant Permission
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Approvals;
