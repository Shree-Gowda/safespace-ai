import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [inputText, setInputText] = useState("");
    const [logs, setLogs] = useState([]);

    // Function to send a new post to the Agents
    const handleModerate = async () => {
        await axios.post('http://localhost:8000/moderate', { text: inputText });
        setInputText("");
        fetchLogs(); // Refresh the list
    };

    // Function to fetch history from MySQL (via your API)
    const fetchLogs = async () => {
        const res = await axios.get('http://localhost:8000/logs');
        setLogs(res.data);
    };

    useEffect(() => { fetchLogs(); }, []);

    return (
        <div style={{ padding: '40px', backgroundColor: '#f4f7f6', minHeight: '100vh' }}>
            <h1>🛡️ SafeSpace Admin Dashboard</h1>

            <div style={{ marginBottom: '30px' }}>
                <input
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Enter user post..."
                    style={{ padding: '10px', width: '300px' }}
                />
                <button onClick={handleModerate} style={{ padding: '10px 20px', marginLeft: '10px' }}>
                    Run AI Agents
                </button>
            </div>

            <h3>Recent Moderation Logs</h3>
            <table border="1" cellPadding="10" style={{ width: '100%', backgroundColor: 'white' }}>
                <thead>
                    <tr>
                        <th>Post</th>
                        <th>Sentiment</th>
                        <th>Verdict</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.map(log => (
                        <tr key={log.id}>
                            <td>{log.post_text}</td>
                            <td style={{ color: log.sentiment === 'AGGRESSIVE' ? 'red' : 'green' }}>{log.sentiment}</td>
                            <td>{log.verdict}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;