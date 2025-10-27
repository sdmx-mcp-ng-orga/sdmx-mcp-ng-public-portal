# 💬 SDMX-MCP-NG Chat Interface

A simple, beautiful web-based chat interface for querying Luxembourg statistical data with natural language.

![Chat Interface](https://img.shields.io/badge/Status-Ready-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🚀 Quick Start

### Step 1: Ensure SDMX-MCP-NG Services are Running

Make sure the SDMX-MCP-NG services are running:

```bash
cd ../../../sdmx-mcp-ng
./deploy.sh status
```

All services should be healthy, especially:
- ✅ MCP Gateway (port 8811)
- ✅ Neo4j MCP (port 8081)
- ✅ SDMX Fetcher MCP (port 8082)

### Step 2: Start the Backend Bridge Server

**Terminal 1** - Start the Python backend that bridges HTTP to MCP protocol:

```bash
cd StatecHackathon2025/YaSchat
uv run python backend.py
```

You should see:
```
✅ Backend server running on http://localhost:8000
✅ Bridging to MCP Gateway at http://localhost:8811/mcp
```

### Step 3: Start the Frontend Server

**Terminal 2** - Start the web server for the chat interface:

```bash
cd StatecHackathon2025/YaSchat
python3 serve_chat.py
```

You should see:
```
✅ Server running on http://localhost:8080
```

### Step 4: Open in Browser

Navigate to: **http://localhost:8080/chat.html**

---

## 🎯 Features

### ✨ Modern Chat Interface
- Clean, gradient-styled UI
- Real-time message display
- Typing indicators
- Responsive design

### 🤖 Natural Language Queries
- Ask questions in plain English
- AI-powered workflow planning
- Multi-step query execution

### 📊 Rich Response Display
- Formatted execution results
- Success/failure indicators
- Performance metrics (duration, steps)
- Raw JSON viewer with copy function

### 💡 Example Prompts
- Pre-loaded example queries
- Click to use instantly
- Covers common use cases

---

## 📝 How to Use

### Basic Usage

1. Type your question in the input box
2. Press Enter or click "Send"
3. Wait for the AI to process (3-10 seconds)
4. View formatted results

### Example Queries

**Simple:**
```
Get unemployment statistics for 2024
```

**Specific:**
```
Show me employment data for the last 12 months
```

**Discovery:**
```
Find all dataflows related to labor market
```

**Direct Fetch:**
```
Get data from DF_B3019 for 2024-10 to 2025-10
```

---

## 🎨 Interface Features

### Status Indicator
- 🟢 **Green (Connected)**: System ready
- 🟡 **Yellow (Processing)**: Query in progress
- 🔴 **Red (Error)**: Connection issue

### Message Types

**User Messages** (right side, purple gradient):
- Your queries
- Displayed as sent

**Assistant Messages** (left side, white):
- AI responses
- Formatted results
- Error messages
- Execution metadata

### Response Format

Successful queries show:
- ✅ Success indicator
- ⚡ Duration and step count
- 🎯 AI reasoning (plan)
- 📊 Execution results per step
- 📋 Raw JSON (expandable)

---

## 🔧 Technical Details

### Architecture

```
Browser (chat.html)
    ↓ HTTP POST
MCP Gateway (localhost:8811)
    ↓ MCP Protocol
Neo4j MCP + SDMX Fetcher MCP
    ↓ Data Fetch
STATEC SDMX API
```

### API Endpoint

The chat interface calls:
```
POST http://localhost:8811/mcp/tools/call
Content-Type: application/json

{
  "name": "plan_and_execute_workflow",
  "arguments": {
    "user_request": "your query here"
  }
}
```

### Technologies Used

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: CSS Grid, Flexbox, Gradients, Animations
- **API**: Fetch API for async requests
- **Server**: Python 3 SimpleHTTPServer with CORS

---

## 🐛 Troubleshooting

### Chat Won't Load

**Problem**: Page doesn't load or shows blank

**Solutions**:
1. Check server is running: `python3 serve_chat.py`
2. Verify correct URL: `http://localhost:8080/chat.html`
3. Check browser console for errors (F12)

### "Offline - Check if services are running"

**Problem**: Status shows offline/error

**Solutions**:
1. Verify MCP Gateway: `curl http://localhost:8811/health`
2. Restart services: `cd ../../sdmx-mcp-ng && ./deploy.sh restart`
3. Check Docker: `docker ps | grep sdmx-mcp-ng`

### Queries Fail or Timeout

**Problem**: All queries return errors

**Solutions**:
1. Check MCP Gateway logs: `./deploy.sh logs mcp-gateway`
2. Verify API key in `.env` file
3. Check Gemini API quota hasn't been exceeded
4. Test with simpler query: "Get DF_B3019 data"

### CORS Errors

**Problem**: Browser shows CORS policy errors

**Solutions**:
1. Use provided `serve_chat.py` server (has CORS enabled)
2. Don't open `chat.html` directly (file://)
3. Ensure server is running on localhost

### Slow Responses

**Problem**: Queries take >30 seconds

**Solutions**:
1. Use more specific queries with dataflow IDs
2. Check network connection
3. Reduce time range (shorter periods)
4. Verify LLM API is responsive

---

## 📚 For Developers

### Customization

**Change Colors:**
Edit the CSS gradient in `chat.html`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Add More Examples:**
Add chips in the HTML:
```html
<div class="example-chip" onclick="useExample('Your query here')">
    🏷️ Label
</div>
```

**Change API Endpoint:**
Update the fetch URL in JavaScript:
```javascript
const response = await fetch('http://your-server:port/mcp/tools/call', {
    // ...
});
```

### File Structure

```
StatecHackathon2025/
├── chat.html              # Main chat interface
├── serve_chat.py          # HTTP server script
├── CHAT_INTERFACE_README.md  # This file
└── QUERY_GUIDE_DF_B3019.md   # Query documentation
```

---

## 🎓 For Hackathon Participants

### Getting Started (3 minutes)

1. **Start the chat interface:**
   ```bash
   cd StatecHackathon2025
   python3 serve_chat.py
   ```

2. **Open browser:** http://localhost:8080/chat.html

3. **Try an example:** Click any example chip or type:
   ```
   Get unemployment statistics for 2024
   ```

4. **Wait 3-8 seconds** for results

5. **Explore the data!**

### Pro Tips

✅ **Use specific time periods** for faster results
✅ **Click "View raw JSON"** to see complete data
✅ **Copy JSON** for use in your analysis
✅ **Try the example chips** to learn query patterns
✅ **Check the guides** in the same directory

### Common Tasks

**Find available data:**
```
What dataflows are available about employment?
```

**Get specific dataflow:**
```
Fetch DF_B3019 for 2024-10 to 2025-10
```

**Analyze trends:**
```
Show me unemployment trends for the last 12 months
```

**Compare periods:**
```
Compare employment between 2024 and 2025
```

---

## 📊 Performance

- **Initial Load**: <1 second
- **Simple Query**: 3-5 seconds
- **Discovery + Fetch**: 6-10 seconds
- **Complex Workflow**: 10-15 seconds

---

## 🔐 Security Notes

- **Local only**: Designed for localhost usage
- **No authentication**: Don't expose to internet
- **CORS enabled**: Only for local development
- **No data storage**: Messages not saved

---

## 📖 Related Documentation

- **[HACKATHON_QUICKSTART.md](HACKATHON_QUICKSTART.md)** - General hackathon guide
- **[QUERY_GUIDE_DF_B3019.md](QUERY_GUIDE_DF_B3019.md)** - Comprehensive query examples
- **[QUICK_REFERENCE_QUERIES.md](QUICK_REFERENCE_QUERIES.md)** - Query cheat sheet

---

## 🙌 Credits

Built for the **State Hackathon 2025** using:
- SDMX-MCP-NG Platform
- Model Context Protocol (MCP)
- Google Gemini 2.5 Flash
- Luxembourg STATEC Data

---

## 📝 License

MIT License - Free to use and modify for hackathon purposes

---

**Happy Querying! 🚀**

For support during the hackathon, ask the organizers or check the documentation in this directory.
