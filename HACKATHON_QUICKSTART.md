# 🚀 SDMX-MCP-NG Hackathon Quick Start Guide

**Welcome to the State Hackathon!** This guide will get you querying Luxembourg statistical data in under 5 minutes.

## 📋 System Status

All services are **READY** and operational:
- ✅ Neo4j Graph Database (873 Luxembourg dataflows)
- ✅ SDMX Data Fetcher
- ✅ MCP Gateway with Gemini 2.5 Flash AI
- ✅ Monitoring Stack (Grafana, Prometheus, Loki)

## 🎯 What Can You Do?

Ask natural language questions about Luxembourg statistics, and the AI will:
1. Search 873 dataflows in Neo4j
2. Plan multi-step workflows
3. Fetch real SDMX data from STATEC

## 💡 Example Queries

Try these queries to get started:

### Basic Queries
```
Find unemployment dataflows and fetch monthly data for 2024
```

```
Show me population statistics available from Luxembourg
```

```
Get quarterly GDP data for the last year
```

### Advanced Queries
```
Find employment dataflows related to labor market and retrieve annual data
```

```
Search for price index dataflows and get monthly observations
```

```
What dataflows are available about education or training?
```

## 🛠️ How to Test

### Option 1: Using Python Test Script

```bash
cd /path/to/sdmx-mcp-ng
uv run python ../test_agency_field_fix.py
```

### Option 2: Using MCP Client

```python
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

transport = StreamableHttpTransport(url="http://localhost:8811/mcp")
client = Client(transport)

async with client:
    result = await client.call_tool(
        "plan_and_execute_workflow",
        {"user_request": "Find unemployment dataflows and fetch monthly data for 2024"}
    )
    print(result)
```

### Option 3: Direct HTTP Request

```bash
curl -X POST http://localhost:8811/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "plan_and_execute_workflow",
    "arguments": {
      "user_request": "Find unemployment dataflows and fetch monthly data for 2024"
    }
  }'
```

## 📊 Access Monitoring Dashboards

- **Grafana**: http://localhost:3001 (admin/grafana_s3cr3t)
- **Prometheus**: http://localhost:9090
- **Neo4j Browser**: http://localhost:7474 (neo4j/s3cr3tP@ss)

## 🏆 Hackathon Challenges

### Challenge 1: Data Discovery (Easy)
Find 3 different types of statistical domains (e.g., employment, prices, trade)

### Challenge 2: Time Series Analysis (Medium)
Retrieve and compare unemployment trends across different regions or demographics

### Challenge 3: Multi-Domain Insights (Hard)
Combine data from multiple domains (e.g., employment + education + population) to derive insights

### Challenge 4: Custom Workflow (Expert)
Create a complex multi-step workflow that discovers, filters, and aggregates data from multiple dataflows

## 🐛 Troubleshooting

### Services Not Responding?
```bash
cd sdmx-mcp-ng
./deploy.sh status    # Check all services
./deploy.sh restart   # Restart if needed
```

### Need Fresh Logs?
```bash
./deploy.sh logs mcp-gateway     # Gateway logs
./deploy.sh logs neo4j-mcp       # Neo4j MCP logs
./deploy.sh logs sdmx-fetcher-mcp # Fetcher logs
```

### Rate Limits Hit?
The system has a quota of **1500 requests/day** on Gemini 2.5 Flash. If you hit limits:
- Check current usage in logs
- Consider batching related queries
- Use more specific queries to reduce planning steps

## 📈 Expected Performance

Based on validated testing:
- **Query Planning**: ~1-2 seconds
- **Neo4j Discovery**: ~0.5-1 second
- **SDMX Data Fetch**: ~2-5 seconds per dataflow
- **Total End-to-End**: **3-9 seconds** for typical queries

## 🎓 Understanding the Results

### Workflow Plan
The AI will show you:
1. **Reasoning**: Why it chose this approach
2. **Steps**: Each tool call with arguments
3. **Field Validation**: Confirms correct field names (agency vs agencyID)

### Execution Results
You'll see:
- ✓ Success or ✗ Failure for each step
- Retrieved data (dataflows, observations, metadata)
- Performance metrics (duration, step count)

## 📚 Data Available

**873 Luxembourg Dataflows** covering:
- 📊 Employment & Labor Market (DF_B3xxx series)
- 💰 Economic Indicators & GDP
- 📈 Price Indices & Inflation
- 👥 Population & Demographics
- 🏢 Business Statistics
- 🎓 Education & Training
- 🏥 Health Statistics
- 🌍 Trade & External Sector

## 🤝 Need Help?

1. Check the main [README.md](../sdmx-mcp-ng/Readme.md)
2. Review the [statechackathon.md](statechackathon.md) proposal
3. Check monitoring dashboards for service health
4. Ask hackathon organizers for assistance

## 🎉 Let's Build Something Amazing!

The system is **production-ready** and waiting for your queries. Start with simple questions and work your way up to complex multi-domain analytics.

**Good luck, and have fun exploring Luxembourg's statistical data!** 🇱🇺

---

*Last verified: October 27, 2025 - All systems operational*
