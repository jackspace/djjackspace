#!/bin/bash

# DJ Jackspace Website Setup Script
# This script sets up the professional DJ website and automated agent

set -e

echo "🎵 Setting up DJ Jackspace Professional Website & Agent 🎵"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root for system service setup
check_permissions() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. This will install system-wide components."
        SYSTEM_INSTALL=true
    else
        print_status "Running as regular user. Will skip system service installation."
        SYSTEM_INSTALL=false
    fi
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Check if pip is installed
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 not found. Please install Python 3 and pip first."
        exit 1
    fi
    
    # Install requirements
    pip3 install -r requirements.txt
    
    print_success "Python dependencies installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p js
    mkdir -p logs
    mkdir -p backups
    
    print_success "Directories created"
}

# Set up file permissions
setup_permissions() {
    print_status "Setting up file permissions..."
    
    chmod +x jackspace_agent.py
    chmod +x setup.sh
    
    if [ "$SYSTEM_INSTALL" = true ]; then
        # If running as root, set up proper web server permissions
        chown -R www-data:www-data .
        chmod 644 index.html
        chmod 644 css/styles.css
        chmod 644 js/main.js
        chmod 755 images/
    fi
    
    print_success "Permissions set"
}

# Test the agent
test_agent() {
    print_status "Testing the Jackspace agent..."
    
    # Run a single check to verify everything works
    python3 jackspace_agent.py --check-once
    
    if [ $? -eq 0 ]; then
        print_success "Agent test completed successfully"
    else
        print_warning "Agent test completed with warnings (this is normal for first run)"
    fi
}

# Install systemd service (if root)
install_service() {
    if [ "$SYSTEM_INSTALL" = true ]; then
        print_status "Installing systemd service..."
        
        # Update service file with current directory
        CURRENT_DIR=$(pwd)
        sed -i "s|/var/www/dj.jackspace.com|$CURRENT_DIR|g" jackspace-agent.service
        
        # Copy service file
        cp jackspace-agent.service /etc/systemd/system/
        
        # Reload systemd and enable service
        systemctl daemon-reload
        systemctl enable jackspace-agent
        
        print_success "Systemd service installed and enabled"
        print_status "To start the service: sudo systemctl start jackspace-agent"
        print_status "To check status: sudo systemctl status jackspace-agent"
        print_status "To view logs: sudo journalctl -u jackspace-agent -f"
    else
        print_warning "Skipping systemd service installation (requires root)"
        print_status "To run manually: python3 jackspace_agent.py --continuous"
    fi
}

# Create configuration file
create_config() {
    print_status "Creating configuration file..."
    
    cat > .env << EOF
# DJ Jackspace Agent Configuration
# Copy this file and update with your actual values

# Mixcloud settings
MIXCLOUD_USERNAME=djjackspace

# Email notification settings (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
NOTIFICATION_EMAIL=your-email@gmail.com

# Agent settings
CHECK_INTERVAL_MINUTES=30
LOG_LEVEL=INFO
EOF

    print_success "Configuration file created (.env)"
    print_warning "Please edit .env file with your actual email settings if you want notifications"
}

# Display final instructions
show_final_instructions() {
    echo ""
    echo "🎵 DJ Jackspace Setup Complete! 🎵"
    echo "=================================="
    echo ""
    print_success "Your professional DJ website is now set up!"
    echo ""
    echo "📁 Files created:"
    echo "   - index.html (professional website)"
    echo "   - css/styles.css (modern styling)"
    echo "   - js/main.js (interactive functionality)"
    echo "   - jackspace_agent.py (automated agent)"
    echo "   - .env (configuration file)"
    echo ""
    echo "🤖 Agent capabilities:"
    echo "   - Automatically scrapes Mixcloud for new sets"
    echo "   - Updates website with latest content"
    echo "   - Sends email notifications (when configured)"
    echo "   - Runs as background service"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Edit .env file with your email settings (optional)"
    echo "   2. Test the website by opening index.html in a browser"
    
    if [ "$SYSTEM_INSTALL" = true ]; then
        echo "   3. Start the agent service: sudo systemctl start jackspace-agent"
        echo "   4. Check service status: sudo systemctl status jackspace-agent"
    else
        echo "   3. Run the agent manually: python3 jackspace_agent.py --continuous"
        echo "   4. Or run a single check: python3 jackspace_agent.py --check-once"
    fi
    
    echo ""
    echo "📝 Useful commands:"
    echo "   - View agent logs: tail -f jackspace_agent.log"
    echo "   - Manual agent check: python3 jackspace_agent.py --check-once"
    echo "   - Stop agent service: sudo systemctl stop jackspace-agent"
    echo ""
    print_success "Setup complete! Your cosmic DJ website is ready to launch! 🚀"
}

# Main execution
main() {
    check_permissions
    create_directories
    install_python_deps
    setup_permissions
    create_config
    test_agent
    install_service
    show_final_instructions
}

# Run main function
main