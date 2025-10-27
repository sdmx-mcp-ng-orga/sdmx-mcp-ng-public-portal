# Quick Reference: How to Query Employment & Unemployment Data

**TL;DR**: Use the simplest script below or any of the query methods shown.

---

## 🎯 Simplest Way (Copy & Run)

**File**: [simple_query_df_b3019.py](../../../simple_query_df_b3019.py)

```bash
cd portal/sdmx-mcp-ng
uv run python ../simple_query_df_b3019.py
```

**Result**:
- ✅ 11 employment/unemployment series
- ✅ 12 months of data (Oct 2024 - Sep 2025)
- ✅ 132 total data points
- ⚡ Completed in ~3-5 seconds
- 💾 Saved to `df_b3019_table.json`

---

## 📝 Query Cheat Sheet

### Python - One-Liner

```python
import asyncio
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

async def query():
    transport = StreamableHttpTransport(url="http://localhost:8811/mcp")
    client = Client(transport)
    async with client:
        return await client.call_tool(
            "plan_and_execute_workflow",
            {"user_request": "Get employment and unemployment data for 2024-2025"}
        )

asyncio.run(query())
```

### Python - Direct URL

```python
import requests

url = "https://lustat.statec.lu/rest/data/DF_B3019/all/all"
params = {"startPeriod": "2024-10", "endPeriod": "2025-10"}
data = requests.get(url, params=params).json()
```

### Bash - cURL

```bash
curl "https://lustat.statec.lu/rest/data/DF_B3019/all/all?startPeriod=2024-10&endPeriod=2025-10"
```

---

## 💡 Natural Language Examples

All of these work with the MCP Gateway:

### Example 1: Simple
```python
"Get unemployment statistics for the last 12 months"
```

### Example 2: Specific
```python
"Fetch employment and unemployment data for 2024 and 2025"
```

### Example 3: Explicit
```python
"Get data from dataflow DF_B3019 for October 2024 to September 2025"
```

### Example 4: Detailed
```python
"Find unemployment dataflows and retrieve monthly data showing unemployment rate, number of unemployed, and active population"
```

---

## 📊 What Data You Get

### All 11 Series:
1. Resident borderers (seasonally adjusted)
2. Number of unemployed (seasonally adjusted)
3. Active population (seasonally adjusted)
4. Unemployment rate (%) (seasonally adjusted)
5. National employment (seasonally adjusted)
6. National wage-earners (seasonally adjusted)
7. Non-resident borderers (seasonally adjusted)
8. Domestic employment (seasonally adjusted)
9. Domestic wage-earners (seasonally adjusted)
10. National self-employed (seasonally adjusted)
11. Domestic self-employed (seasonally adjusted)

### Time Periods:
- **Frequency**: Monthly (M)
- **Default**: Last 12 months
- **Custom**: Specify `start_period` and `end_period`

### Data Format:
```json
{
  "success": true,
  "data": {
    "header": { ... },
    "dataSets": [
      {
        "series": {
          "0:0": {
            "observations": {
              "0": [14049.82, null, null, null, 0],
              "1": [14049.48, null, null, null, 0],
              ...
            }
          }
        }
      }
    ],
    "structure": {
      "name": "Employment, unemployment and unemployment rate...",
      "dimensions": { ... }
    }
  }
}
```

---

## 🔧 Advanced Queries

### Filter by Time Period

```python
# Quarterly data for 2024
"Get DF_B3019 quarterly data for 2024"
```

### Specific Series

```python
# Only unemployment rate
"Show me just the unemployment rate from DF_B3019 for 2024-2025"
```

### Multiple Dataflows

```python
# Combine multiple dataflows
"Get unemployment from DF_B3019 and population from DF_B1001 for 2024"
```

---

## ⚡ Performance Benchmarks

| Method | Time | Complexity |
|--------|------|------------|
| **Direct SDMX API** | ~1-2s | Low (you build URL) |
| **MCP Gateway** | ~3-5s | Very Low (natural language) |
| **Neo4j + SDMX** | ~6-8s | Low (discovery + fetch) |

---

## 🎓 Hackathon Tips

### For Quick Results:
✅ Use [simple_query_df_b3019.py](../../../simple_query_df_b3019.py)

### For Exploration:
✅ Use natural language queries with discovery

### For Integration:
✅ Use direct SDMX API endpoints

### For Complex Workflows:
✅ Combine Neo4j search + SDMX fetch

---

## 🚀 Ready-to-Run Scripts

All these scripts are ready in the `portal/` directory:

1. **[simple_query_df_b3019.py](../../../simple_query_df_b3019.py)** ⭐ RECOMMENDED
   - Simplest and most reliable
   - Returns complete table
   - Saves to JSON automatically

2. **[quick_query_df_b3019.py](../../../quick_query_df_b3019.py)**
   - Multiple method examples
   - Choose your preferred approach
   - Good for learning

3. **[test_df_b3019_simple.py](../../../test_df_b3019_simple.py)**
   - Validation script
   - Checks data completeness
   - Good for testing

---

## 📖 Full Documentation

For detailed explanations:
- **Query Guide**: [QUERY_GUIDE_DF_B3019.md](QUERY_GUIDE_DF_B3019.md)
- **Data Comparison**: [df_b3019_comparison.md](df_b3019_comparison.md)
- **Hackathon Guide**: [HACKATHON_QUICKSTART.md](HACKATHON_QUICKSTART.md)

---

## ✅ Verification

Test that everything works:

```bash
cd portal/sdmx-mcp-ng
uv run python ../simple_query_df_b3019.py
```

**Expected output**:
```
✅ Data retrieved successfully!
📊 Data Summary:
   - Series retrieved: 11
   - Observations per series: 12
   - Total data points: 132
💾 Complete data saved to: df_b3019_table.json
```

---

## 🎉 You're Ready!

Pick a method and start querying. The system retrieves official STATEC data in seconds!

**Questions?** Check the full guides or ask during the hackathon.
