#!/usr/bin/env python3
"""
Enhanced Conversational Backend for SDMX-MCP-NG Chat Interface
Supports multi-turn conversations, data extraction, and clarifying questions
"""

import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Any, Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../sdmx-mcp-ng'))

try:
    from fastmcp.client import Client
    from fastmcp.client.transports import StreamableHttpTransport
except ImportError:
    print("Error: fastmcp module not found")
    sys.exit(1)

PORT = 8000
MCP_GATEWAY_URL = "http://localhost:8811/mcp"

# Store conversation history (in-memory, simple implementation)
conversation_history: Dict[str, List[Dict]] = {}


def extract_actual_data(result: Dict) -> Dict[str, Any]:
    """Extract and format actual data from MCP result"""

    extracted = {
        'has_data': False,
        'dataflows': [],
        'observations': [],
        'summary': ''
    }

    if not result.get('success'):
        return extracted

    # Check if there's execution data
    if 'execution' not in result or not result['execution']:
        extracted['summary'] = "Query planned but no data was fetched."
        return extracted

    # Extract data from execution steps
    for step in result['execution']:
        if step.get('status') != 'success':
            continue

        step_result = step.get('result', [])
        if not step_result:
            continue

        # Parse the nested JSON in result
        try:
            for item in step_result:
                if hasattr(item, 'text'):
                    data_text = item.text
                elif isinstance(item, dict) and 'text' in item:
                    data_text = item['text']
                else:
                    continue

                data = json.loads(data_text)

                # Check if this is SDMX data (has observations)
                if 'data' in data and 'dataSets' in data['data']:
                    extracted['has_data'] = True

                    # Extract dataflow info
                    structure = data['data'].get('structure', {})
                    extracted['dataflows'].append({
                        'name': structure.get('name', 'Unknown'),
                        'description': structure.get('description', ''),
                    })

                    # Extract observations summary
                    datasets = data['data']['dataSets']
                    if datasets and len(datasets) > 0:
                        series = datasets[0].get('series', {})
                        total_series = len(series)

                        # Count observations
                        total_obs = 0
                        for serie_data in series.values():
                            obs = serie_data.get('observations', {})
                            total_obs += len(obs)

                        extracted['observations'].append({
                            'series_count': total_series,
                            'observation_count': total_obs,
                            'raw_data': data  # Keep full data for display
                        })

                        # Create summary
                        extracted['summary'] = f"Retrieved {total_series} data series with {total_obs} observations"

                # Check if this is Neo4j discovery data
                elif isinstance(data, list) and len(data) > 0:
                    extracted['has_data'] = True
                    extracted['dataflows'].extend(data)
                    extracted['summary'] = f"Found {len(data)} dataflows"

        except json.JSONDecodeError:
            continue
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue

    return extracted


def should_ask_clarification(result: Dict, extracted_data: Dict) -> Optional[Dict]:
    """Determine if we should ask a clarifying question"""

    # If multiple dataflows found, ask which one to fetch
    if extracted_data.get('dataflows') and len(extracted_data['dataflows']) > 3:
        if not extracted_data.get('observations'):  # Only dataflow discovery, no data yet
            return {
                'type': 'select_dataflow',
                'message': f"I found {len(extracted_data['dataflows'])} dataflows. Here are the first 5:",
                'options': extracted_data['dataflows'][:5],
                'prompt': 'Which dataflow would you like to explore? (Type the number or name)'
            }

    # If no data was retrieved, suggest being more specific
    if result.get('success') and not extracted_data.get('has_data'):
        if result.get('plan'):
            return {
                'type': 'refine_query',
                'message': 'I planned the query but couldn\'t retrieve data. This might help:',
                'suggestions': [
                    'Specify a dataflow ID (like DF_B3019)',
                    'Add a time period (like "for 2024")',
                    'Try: "Get data from DF_B3019 for 2024-10 to 2025-10"'
                ]
            }

    return None


class ConversationalMCPHandler(BaseHTTPRequestHandler):
    """Enhanced HTTP Handler with conversation support"""

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/query':
            self.handle_query()
        elif self.path == '/reset':
            self.handle_reset()
        else:
            self.send_error(404, "Not Found")

    def handle_query(self):
        """Handle query with conversation context"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            user_request = request_data.get('user_request', '')
            session_id = request_data.get('session_id', 'default')
            context = request_data.get('context', {})

            if not user_request:
                self.send_json_response({'error': 'Missing user_request'}, 400)
                return

            # Get conversation history
            if session_id not in conversation_history:
                conversation_history[session_id] = []

            # Execute query
            result = asyncio.run(self.execute_mcp_query(user_request, session_id, context))

            # Extract actual data
            extracted_data = extract_actual_data(result)

            # Check if clarification needed
            clarification = should_ask_clarification(result, extracted_data)

            # Build enhanced response
            response = {
                'success': result.get('success', False),
                'original_result': result,
                'extracted_data': extracted_data,
                'clarification': clarification,
                'conversation_id': session_id
            }

            # Store in history
            conversation_history[session_id].append({
                'query': user_request,
                'result': result,
                'extracted': extracted_data
            })

            self.send_json_response(response, 200)

            print(f"[Query] {user_request[:50]}... -> {extracted_data.get('summary', 'No summary')}")

        except json.JSONDecodeError:
            self.send_json_response({'error': 'Invalid JSON'}, 400)
        except Exception as e:
            print(f"[Error] {e}")
            self.send_json_response({
                'error': str(e),
                'type': type(e).__name__
            }, 500)

    def handle_reset(self):
        """Reset conversation history"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            session_id = request_data.get('session_id', 'default')

            if session_id in conversation_history:
                del conversation_history[session_id]

            self.send_json_response({'success': True, 'message': 'Conversation reset'}, 200)

        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)

    async def execute_mcp_query(self, user_request: str, session_id: str, context: Dict):
        """Execute query via MCP protocol with context"""
        transport = StreamableHttpTransport(url=MCP_GATEWAY_URL)
        client = Client(transport)

        # Enhance request with conversation context if available
        history = conversation_history.get(session_id, [])
        if history and len(history) > 0:
            last_query = history[-1]
            if context.get('use_context'):
                user_request = f"Context: {last_query['query']}\nNew request: {user_request}"

        try:
            async with client:
                result = await client.call_tool(
                    "plan_and_execute_workflow",
                    {"user_request": user_request}
                )

                # Parse result
                if hasattr(result, 'content'):
                    content = result.content
                    if isinstance(content, list) and len(content) > 0:
                        result_text = content[0].text if hasattr(content[0], 'text') else str(content[0])
                    else:
                        result_text = str(content)
                else:
                    result_text = str(result)

                return json.loads(result_text)

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }

    def send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()

        response_json = json.dumps(data, indent=2)
        self.wfile.write(response_json.encode('utf-8'))

    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, format, *args):
        """Custom log format"""
        # Reduce verbose logging
        pass


def run_server():
    """Start the conversational backend server"""
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ConversationalMCPHandler)

    print("=" * 80)
    print("🔧 SDMX-MCP-NG Conversational Chat Backend")
    print("=" * 80)
    print(f"\n✅ Backend server running on http://localhost:{PORT}")
    print(f"✅ Bridging to MCP Gateway at {MCP_GATEWAY_URL}")
    print(f"\n📡 Endpoints:")
    print(f"   POST http://localhost:{PORT}/query   - Send queries")
    print(f"   POST http://localhost:{PORT}/reset   - Reset conversation")
    print("\n✨ Features:")
    print("   - Extracts actual data from responses")
    print("   - Supports conversation history")
    print("   - Asks clarifying questions")
    print("   - Provides data summaries")
    print("\n⚠️  Make sure MCP Gateway is running on http://localhost:8811")
    print("\n🛑 Press Ctrl+C to stop\n")
    print("=" * 80)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Backend server stopped. Goodbye!")
        httpd.shutdown()


if __name__ == "__main__":
    run_server()
