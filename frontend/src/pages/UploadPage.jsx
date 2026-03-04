import { useState } from "react";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [domain, setDomain] = useState("HR");
  const [classification, setClassification] = useState("PUBLIC");
  const [message, setMessage] = useState("");

  const uploadFile = async () => {
    setMessage("");

    if (!file) {
      setMessage("Please choose a file to upload.");
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      setMessage("You are not authenticated.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("domain", domain);
    formData.append("classification", classification);

    try {
      const res = await fetch("http://localhost:5000/api/docs/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.msg || "Upload failed.");
        return;
      }

      setFile(null);
      setMessage("Upload successful.");
    } catch (error) {
      setMessage("Server connection failed.");
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow max-w-md">
      <h2 className="text-lg font-bold mb-4">
        Upload Document
      </h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-3"
      />

      <select
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
        className="border p-2 mb-3 w-full"
      >
        <option>HR</option>
        <option>DEV</option>
        <option>IT</option>
        <option>Security</option>
      </select>

      <select
        value={classification}
        onChange={(e) => setClassification(e.target.value)}
        className="border p-2 mb-3 w-full"
      >
        <option>PUBLIC</option>
        <option>INTERNAL</option>
        <option>RESTRICTED</option>
        <option>CONFIDENTIAL</option>
      </select>

      {message && (
        <p className="text-sm text-gray-700 mb-3">{message}</p>
      )}

      <button
        onClick={uploadFile}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
    </div>
  );
}

export default UploadPage;
