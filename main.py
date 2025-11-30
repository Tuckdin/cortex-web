"""
The Cortex Web Interface
A simple server to host the search interface
"""

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="The Cortex Web Interface")

# Read the HTML file
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Cortex | ATLAS Knowledge Base</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #e0e0e0;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            padding: 30px 0;
        }

        .logo {
            font-size: 3rem;
            margin-bottom: 10px;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 300;
            color: #00d4ff;
            margin-bottom: 5px;
        }

        .subtitle {
            color: #888;
            font-size: 1rem;
            font-style: italic;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .stat {
            text-align: center;
            padding: 15px 25px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            border: 1px solid rgba(0,212,255,0.2);
        }

        .stat-number {
            font-size: 1.8rem;
            font-weight: bold;
            color: #00d4ff;
        }

        .stat-label {
            font-size: 0.8rem;
            color: #888;
            margin-top: 5px;
        }

        .search-section {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid rgba(0,212,255,0.1);
        }

        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }

        input[type="text"] {
            flex: 1;
            padding: 15px 20px;
            font-size: 1.1rem;
            border: 2px solid rgba(0,212,255,0.3);
            border-radius: 10px;
            background: rgba(0,0,0,0.3);
            color: #fff;
            outline: none;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus {
            border-color: #00d4ff;
        }

        input[type="text"]::placeholder {
            color: #666;
        }

        button {
            padding: 15px 30px;
            font-size: 1.1rem;
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            border: none;
            border-radius: 10px;
            color: #fff;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,212,255,0.4);
        }

        button:active {
            transform: translateY(0);
        }

        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 8px 20px;
            font-size: 0.9rem;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            color: #ccc;
            cursor: pointer;
            transition: all 0.3s;
        }

        .filter-btn:hover {
            background: rgba(0,212,255,0.2);
            border-color: #00d4ff;
        }

        .filter-btn.active {
            background: rgba(0,212,255,0.3);
            border-color: #00d4ff;
            color: #00d4ff;
        }

        .results {
            margin-top: 30px;
        }

        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .results-count {
            color: #888;
        }

        .result-card {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #00d4ff;
            transition: transform 0.2s, background 0.2s;
        }

        .result-card:hover {
            transform: translateX(5px);
            background: rgba(255,255,255,0.08);
        }

        .result-source {
            font-size: 0.85rem;
            color: #00d4ff;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .similarity-badge {
            background: rgba(0,212,255,0.2);
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.8rem;
        }

        .result-content {
            line-height: 1.6;
            color: #d0d0d0;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #888;
        }

        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 3px solid rgba(0,212,255,0.2);
            border-top-color: #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }

        .empty-state .icon {
            font-size: 4rem;
            margin-bottom: 20px;
        }

        .error {
            background: rgba(255,0,0,0.1);
            border: 1px solid rgba(255,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            color: #ff6b6b;
            text-align: center;
        }

        footer {
            text-align: center;
            padding: 30px;
            color: #555;
            font-size: 0.9rem;
        }

        footer a {
            color: #00d4ff;
            text-decoration: none;
        }

        @media (max-width: 600px) {
            h1 {
                font-size: 1.8rem;
            }

            .search-box {
                flex-direction: column;
            }

            button {
                width: 100%;
            }

            .stats {
                gap: 15px;
            }

            .stat {
                padding: 10px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">🧠</div>
            <h1>The Cortex</h1>
            <p class="subtitle">ATLAS Knowledge Base — Semantic Search</p>
        </header>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">776</div>
                <div class="stat-label">ICT Transcripts</div>
            </div>
            <div class="stat">
                <div class="stat-number">20,829</div>
                <div class="stat-label">Searchable Chunks</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="status-indicator">●</div>
                <div class="stat-label">Server Status</div>
            </div>
        </div>

        <div class="search-section">
            <div class="search-box">
                <input type="text" id="search-input" placeholder="Search ICT concepts... (e.g., order blocks, liquidity, FOMO)" autofocus>
                <button onclick="search()">Search</button>
            </div>
            <div class="filters">
                <button class="filter-btn active" data-filter="all" onclick="setFilter('all')">All Sources</button>
                <button class="filter-btn" data-filter="ict" onclick="setFilter('ict')">ICT Only</button>
                <button class="filter-btn" data-filter="vanessa" onclick="setFilter('vanessa')">Social Skills</button>
            </div>
        </div>

        <div class="results" id="results">
            <div class="empty-state">
                <div class="icon">🔍</div>
                <p>Search The Cortex for ICT trading wisdom</p>
                <p style="margin-top: 10px; font-size: 0.9rem;">Try: "order blocks", "liquidity sweep", "dealing with FOMO"</p>
            </div>
        </div>

        <footer>
            <p>The Cortex — Built for ATLAS by Mr. Pak</p>
        </footer>
    </div>

    <script>
        const API_BASE = 'https://web-production-2845d.up.railway.app';
        let currentFilter = 'all';

        async function checkStatus() {
            const indicator = document.getElementById('status-indicator');
            try {
                const response = await fetch(API_BASE);
                const data = await response.json();
                if (data.status === 'healthy') {
                    indicator.style.color = '#00ff88';
                    indicator.textContent = '● Online';
                } else {
                    indicator.style.color = '#ffaa00';
                    indicator.textContent = '● Degraded';
                }
            } catch (e) {
                indicator.style.color = '#ff4444';
                indicator.textContent = '● Offline';
            }
        }

        function setFilter(filter) {
            currentFilter = filter;
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.filter === filter);
            });
        }

        async function search() {
            const query = document.getElementById('search-input').value.trim();
            if (!query) return;

            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<div class="loading"><div class="loading-spinner"></div><p>Searching The Cortex...</p></div>';

            try {
                let url;
                if (currentFilter === 'ict') {
                    url = `${API_BASE}/search/ict?query=${encodeURIComponent(query)}&limit=10`;
                } else if (currentFilter === 'vanessa') {
                    url = `${API_BASE}/search/vanessa?query=${encodeURIComponent(query)}&limit=10`;
                } else {
                    url = `${API_BASE}/search/ict?query=${encodeURIComponent(query)}&limit=10`;
                }

                const response = await fetch(url);
                const data = await response.json();
                displayResults(data.results || [], query);

            } catch (error) {
                resultsDiv.innerHTML = '<div class="error"><p>⚠️ Error connecting to The Cortex</p><p style="font-size: 0.9rem; margin-top: 10px;">' + error.message + '</p></div>';
            }
        }

        function displayResults(results, query) {
            const resultsDiv = document.getElementById('results');

            if (results.length === 0) {
                resultsDiv.innerHTML = '<div class="empty-state"><div class="icon">🤔</div><p>No results found for "' + query + '"</p><p style="margin-top: 10px; font-size: 0.9rem;">Try different keywords or broader terms</p></div>';
                return;
            }

            let html = '<div class="results-header"><h3>Results for "' + query + '"</h3><span class="results-count">' + results.length + ' matches</span></div>';

            results.forEach(result => {
                const source = result.source_transcript || result.source || 'Unknown';
                const similarity = result.similarity ? (result.similarity * 100).toFixed(1) : '?';
                const content = result.content || '';

                html += '<div class="result-card"><div class="result-source"><span>📄 ' + source + '</span><span class="similarity-badge">' + similarity + '% match</span></div><div class="result-content">' + content + '</div></div>';
            });

            resultsDiv.innerHTML = html;
        }

        document.getElementById('search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') search();
        });

        checkStatus();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_CONTENT

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
