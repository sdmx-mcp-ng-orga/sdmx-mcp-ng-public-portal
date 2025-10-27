#!/bin/bash
#
# SDMX-MCP-NG Chat Interface Launcher
# This script starts both the backend bridge and frontend server
#

echo "=========================================="
echo "🚀 SDMX-MCP-NG Chat Interface"
echo "=========================================="
echo ""

# Check if SDMX-MCP-NG services are running
echo "🔍 Checking SDMX-MCP-NG services..."
if ! docker ps | grep -q "sdmx-mcp-ng-mcp-gateway"; then
    echo "❌ MCP Gateway is not running!"
    echo ""
    echo "Please start SDMX-MCP-NG services first:"
    echo "  cd ../../../sdmx-mcp-ng"
    echo "  ./deploy.sh status"
    echo ""
    exit 1
fi

echo "✅ MCP Gateway is running"
echo ""

# Start backend in background
echo "🔧 Starting backend bridge server (port 8000)..."
cd "$(dirname "$0")"

# Check if running in sdmx-mcp-ng directory structure
SDMX_DIR="../../../sdmx-mcp-ng"
if [ -d "$SDMX_DIR" ]; then
    cd "$SDMX_DIR"
    uv run python "../portal/sdmx-mcp-ng-public-portal/StatecHackathon2025/YaSchat/backend.py" &
    BACKEND_PID=$!
    cd - > /dev/null
else
    echo "❌ Cannot find sdmx-mcp-ng directory"
    exit 1
fi

sleep 2

# Check if backend started successfully
if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo "❌ Backend failed to start"
    exit 1
fi

echo "✅ Backend server started (PID: $BACKEND_PID)"
echo ""

# Start frontend server
echo "🌐 Starting frontend server (port 8080)..."
python3 serve_chat.py &
FRONTEND_PID=$!

sleep 1

# Check if frontend started successfully
if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend server started (PID: $FRONTEND_PID)"
echo ""
echo "=========================================="
echo "✨ Chat interface is ready!"
echo "=========================================="
echo ""
echo "📱 Open in browser:"
echo "   http://localhost:8080/chat.html"
echo ""
echo "📊 Backend API:"
echo "   http://localhost:8000/query"
echo ""
echo "🛑 To stop both servers, press Ctrl+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "👋 Goodbye!"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup INT TERM

# Wait for servers
wait
