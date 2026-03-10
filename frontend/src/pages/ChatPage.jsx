import { useState } from "react";

function ChatPage({ department }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      sender: "user",
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      const res = await fetch(
        "http://localhost:5000/api/chat/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            query: userMessage.text,
            department: department,
          }),
        }
      );

      const data = await res.json();

      const aiMessage = {
        sender: "ai",
        text: data.answer || "No response available.",
        classification: data.classification,
        escalation: data.escalation,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "Server connection error.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="h-full flex flex-col">
      {/* Context */}
      <div className="mb-2 text-sm text-gray-600">
        Active Department:
        <span className="font-semibold ml-2">
          {department}
        </span>
      </div>

      {/* Messages */}
      <div className="flex-1 bg-white rounded shadow p-4 mb-4 overflow-y-auto space-y-3">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded max-w-lg ${
              msg.sender === "user"
                ? "bg-blue-500 text-white ml-auto"
                : "bg-gray-200 text-gray-800"
            }`}
          >
            <p>{msg.text}</p>

            {/* Classification Badge */}
            {msg.classification && (
              <span className="text-xs block mt-2 font-semibold">
                Classification: {msg.classification}
              </span>
            )}

            {/* Escalation Info */}
            {msg.escalation && (
              <div className="mt-3 text-sm bg-red-50 p-3 rounded border border-red-200 text-black">
                <p className="font-semibold text-red-700 mb-2">{msg.escalation.message}</p>

                {msg.escalation.contact && (
                  <div className="bg-white p-2 rounded mb-2 shadow-sm">
                    <p className="font-medium text-gray-800">Contact: {msg.escalation.contact.name}</p>
                    <p className="text-gray-600">Email: {msg.escalation.contact.email}</p>
                    <p className="text-gray-600">Phone: {msg.escalation.contact.phone}</p>
                  </div>
                )}
                
                {msg.classification && msg.classification !== "PUBLIC" && msg.classification !== "INTERNAL" && (
                    <button className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-1.5 px-3 rounded transition-colors mt-2">
                        Ask Access
                    </button>
                )}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <p className="text-gray-400 text-sm">
            SecureDesk is thinking...
          </p>
        )}
      </div>

      {/* Input */}
      <div className="bg-white p-3 rounded shadow flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border rounded px-3 py-2"
          placeholder="Ask SecureDesk..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatPage;