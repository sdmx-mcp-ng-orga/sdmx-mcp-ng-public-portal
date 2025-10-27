# SDMX-MCP-NG Public Portal

**Access Gateway for the SDMX-MCP-NG Project**

---

## 🏆 **FOR HACKATHON PARTICIPANTS** 🏆

**If you're here for the State Hackathon, start here:**

👉 **[HACKATHON QUICK START GUIDE](HACKATHON_QUICKSTART.md)** 👈

This guide will get you querying 873 Luxembourg statistical dataflows in under 5 minutes!

**System Status**: ✅ All services operational and ready for the hackathon

---

## 🚀 Quick Start: Deploying the Platform

This guide provides the fastest way to get the SDMX-MCP-NG platform running.

### Step 1: Get Access to the Private Repository

The main source code is in a private repository. You must be granted access before you can deploy/play with the platform.

- **[➡️ Click here to fill out the Project Access Request form](https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal/issues/new?template=access-request.md)**
- Wait for approval (typically 1-3 business days) and accept the GitHub invitation you receive via email.

### Step 2: Clone This Public Portal

Clone this repository to your local machine to get the deployment script.

```bash
git clone https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal.git
cd sdmx-mcp-ng-public-portal
```

### Step 3: Run the Setup Script

Once you have been granted access, run the setup command. This script will check your permissions and clone the private `sdmx-mcp-ng` repository for you.

```bash
# Make the script executable
chmod +x deploy-public-portal.sh

# Run the setup
./deploy-public-portal.sh setup
```
The private repository will be cloned into a new `sdmx-mcp-ng` directory.

### Step 4: Configure API Keys

The platform requires API keys for the LLM provider (like Gemini, Claude, or OpenAI).

1.  Navigate to the private repository: `cd sdmx-mcp-ng`
2.  Create a `.env` file: `cp .env.example .env`
3.  Edit the `.env` file (`nano .env`) and add your `PLANNER_LLM_API_KEY` and set a secure `NEO4J_PASSWORD`.

### Step 5: Deploy the Platform

Now you can start all the services using the deployment script.

```bash
# From the sdmx-mcp-ng-public-portal directory
./deploy-public-portal.sh dev
```
This command starts the entire stack (database, applications, monitoring) in development mode.

### Managing the Environment

Use the wrapper script to manage your deployment:

-   **Stop all services:** `./deploy-public-portal.sh down`
-   **Check service status:** `./deploy-public-portal.sh status`
-   **View logs:** `./deploy-public-portal.sh logs`
-   **Check health:** `./deploy-public-portal.sh health`

---

## 📦 What is SDMX-MCP-NG?

An advanced, **AI-driven platform** for interacting with **SDMX** (Statistical Data and Metadata eXchange) data.

### Key Features

- 🗄️ **Neo4j Graph Database** - Efficient metadata storage and querying. in a future a GraphQL driven architecture could be considred
- 🤖 **AI-Powered Queries** - Natural language to Cypher using LLMs
- 🔌 **MCP Protocol** - Standard integration with AI assistants
- 🚀 **Fast Demo Setup** - Pre-populated backups/golden images for quick start
- 🌍 **Multi-Source Support** - NSIs, ECB, and other SDMX providers

### Technology Stack

- **Database:** Neo4j 5.21 with APOC
- **Backend:** Python 3.10+ with FastMCP
- **Protocol:** Model Context Protocol (MCP)
- **AI/LLM:** Google Gemini, Anthropic, Claude, OpenAI,Mistral,  Custom
- **Deployment:** Docker & Docker Compose

---

## 📚 Documentation

Full documentation is available in the private repository after access is granted.

**Available after access:**
- Installation & setup guides
- Architecture documentation
- API reference
- Configuration guides
- Demo tutorials

---

## 🤝 Access Levels

### Reader (Default)
- ✅ Clone and pull repository
- ✅ View code and documentation
- ✅ Create and comment on issues
- ❌ Push code

### Writer (By Request)
- ✅ All Reader permissions
- ✅ Push to branches
- ✅ Create pull requests

*Most users receive **Reader** access*

---

## 💬 Contact & Support

- **Access Requests:** [Use the issue template](https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal/issues/new?template=access-request.md)
- **Questions:** [GitHub Discussions](https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal/discussions)
- **Response Time:** 1-3 business days

---

## ❓ FAQ

**Q: Is this open source?**
A: Yes in the future,  meanwhile for the moment the private repository is with controlled access  in order to refine (sdmx-graph db schema mapping, LLM Agentic Architecture, golden image to accelerate the deployment process ...) .

**Q: How long does approval take?**
A: Typically 1-2 business days.

**Q: Can I redistribute the code?**
A: No, others must request their own access.

**Q: Is there a cost?**
A: No, access is free for legitimate use cases (research, development, evaluation).

---

## 📜 License

The code in the private repository has its own license, which is available after access is granted. This public portal repository is under the MIT License.

---

<div align="center">

**🔒 Private Repository - Access Required**

[**Request Access**](https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal/issues/new?template=access-request.md) | [Discussions](https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal/discussions) | [FAQ](#-faq)

*Maintained by @hdjebar*

</div>