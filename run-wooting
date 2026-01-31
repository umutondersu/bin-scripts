#!/bin/bash

# Convenience script to run Wooting Background Service in distrobox container
# This solves GLIBC compatibility issues on Pop!_OS 22.04

export PATH="$HOME/.local/bin:$PATH"

echo "Starting Wooting Background Service in Ubuntu 24.04 container..."
echo "Press Ctrl+C to stop the service"
echo ""

distrobox enter wooting-container -- bash -c "cd ~/Applications && ./Wooting.Background.Service_0.4.7_amd64.AppImage"
