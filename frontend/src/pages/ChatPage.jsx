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
              <div className="mt-2 text-xs bg-white p-2 rounded text-black">
                <p>{msg.escalation.message}</p>

                {msg.escalation.contact && (
                  <>
                    <p>
                      Contact: {msg.escalation.contact.name}
                    </p>
                    <p>
                      Email: {msg.escalation.contact.email}
                    </p>
                    <p>
                      Phone: {msg.escalation.contact.phone}
                    </p>
                  </>
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