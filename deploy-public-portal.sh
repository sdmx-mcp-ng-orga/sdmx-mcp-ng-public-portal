#!/bin/bash

################################################################################
# SDMX-MCP-NG Public Portal - Simplified Deployment Wrapper
#
# Repository: https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal
#
# This script is a user-friendly wrapper for the main deployment script
# located in the private SDMX-MCP-NG repository.
#
# It simplifies setup and deployment by delegating commands to the core
# `deploy.sh` script after ensuring the private repository is available.
#
# USAGE:
#   ./deploy-public-portal.sh setup          # Clones the private repo
#   ./deploy-public-portal.sh <command>      # Passes command to deploy.sh
#
# EXAMPLE COMMANDS:
#   ./deploy-public-portal.sh setup
#   ./deploy-public-portal.sh dev
#   ./deploy-public-portal.sh prod
#   ./deploy-public-portal.sh down
#   ./deploy-public-portal.sh status
#   ./deploy-public-portal.sh logs
#   ./deploy-public-portal.sh health
#
################################################################################

set -e

# --- Configuration ---
PRIVATE_REPO_URL="https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng.git"
PRIVATE_REPO_PATH="./sdmx-mcp-ng"
DEPLOY_SCRIPT_PATH="${PRIVATE_REPO_PATH}/deploy.sh"
PUBLIC_PORTAL_URL="https://github.com/sdmx-mcp-ng-orga/sdmx-mcp-ng-public-portal"

# --- UI ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

CHECK="✅"
CROSS="❌"
INFO="ℹ️"
ROCKET="🚀"
LOCK="🔒"
UNLOCK="🔓"

# --- Utility Functions ---
print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║        ${ROCKET} SDMX-MCP-NG Public Portal Wrapper                   ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}${CHECK} $1${NC}"; }
print_error() { echo -e "${RED}${CROSS} $1${NC}"; }
print_info() { echo -e "${CYAN}${INFO} $1${NC}"; }
print_step() { echo -e "\n${YELLOW}▶ $1${NC}"; }

# --- Core Functions ---

# Guide user on how to get access to the private repository
show_access_request_guide() {
    print_step "How to Request Access"
    echo "${LOCK} The SDMX-MCP-NG source code is in a private repository."
    echo "To get access, please follow these steps:"
    echo "  1. Visit: ${PUBLIC_PORTAL_URL}/issues/new"
    echo "  2. Select the 'Project Access Request' template."
    echo "  3. Fill out the form and submit the issue."
    echo "  4. Wait for approval (1-3 business days) and accept the GitHub invitation."
    echo "${UNLOCK} Once approved, run '$0 setup' again."
}

# Check for git and clone the private repository
run_setup() {
    print_step "Running First-Time Setup"

    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install it to continue."
        exit 1
    fi
    print_success "Git is installed."

    if [ -d "$PRIVATE_REPO_PATH" ]; then
        print_success "Private repository already exists at '$PRIVATE_REPO_PATH'."
        print_info "To get the latest updates, navigate to the directory and run 'git pull'."
        return
    fi

    print_info "Checking access to the private repository..."
    if ! git ls-remote "$PRIVATE_REPO_URL" &> /dev/null; then
        print_error "You do not have access to the private repository."
        show_access_request_guide
        exit 1
    fi

    print_success "Access confirmed!"
    print_info "Cloning private repository into '$PRIVATE_REPO_PATH'..."
    if git clone "$PRIVATE_REPO_URL" "$PRIVATE_REPO_PATH"; then
        print_success "Repository cloned successfully!"
        print_info "Next, configure your API keys by running: nano ${PRIVATE_REPO_PATH}/.env"
        print_info "Then, you can deploy the platform with: $0 dev"
    else
        print_error "Failed to clone the repository."
        exit 1
    fi
}

# Show help message
show_usage() {
    echo "SDMX-MCP-NG Public Portal Deployment Wrapper"
    echo ""
    echo "This script simplifies interaction with the main deployment script."
    echo ""
    echo "USAGE:"
    echo "  $0 [command]"
    echo ""
    echo "COMMANDS:"
    echo "  setup         - Clones the private repository (run this first)."
    echo "  dev           - Deploys the development environment."
    echo "  prod          - Deploys the production environment."
    echo "  down          - Stops all running services."
    echo "  restart       - Restarts all services."
    echo "  status        - Shows the status of all services."
    echo "  logs          - Tails the logs from all services."
    echo "  health        - Checks the health of all services."
    echo "  help          - Shows this help message."
    echo ""
    echo "WORKFLOW:"
    echo "  1. Run '$0 setup' to clone the code."
    echo "  2. Edit '${PRIVATE_REPO_PATH}/.env' to add your API keys."
    echo "  3. Run '$0 dev' to start the platform."
}

# --- Main Execution ---
main() {
    COMMAND="${1:-help}"

    print_header

    if [ "$COMMAND" = "setup" ]; then
        run_setup
        exit 0
    fi

    if [ "$COMMAND" = "help" ]; then
        show_usage
        exit 0
    fi

    # For any other command, ensure the private repo exists first.
    if [ ! -f "$DEPLOY_SCRIPT_PATH" ]; then
        print_error "Private repository not found or 'deploy.sh' is missing."
        print_info "Please run '$0 setup' first."
        exit 1
    fi

    # Pass the command to the main deployment script
    print_info "Passing command '$COMMAND' to the core deployment script..."
    echo "----------------------------------------------------------------"
    
    # Execute the script from within its directory
    (cd "$PRIVATE_REPO_PATH" && ./deploy.sh "$@")
}

main "$@"
