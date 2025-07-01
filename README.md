# 🎵 DJ Jackspace - Professional Website & Automated Agent

A professional DJ website with automated Mixcloud integration and content management. This system automatically scrapes your Mixcloud profile for new sets and updates your website in real-time.

## ✨ Features

### 🌟 Professional Website
- **Modern Design**: Sleek, responsive design with cosmic theme
- **Mobile Responsive**: Perfect viewing on all devices
- **Interactive Elements**: Smooth scrolling, animations, and hover effects
- **Professional Sections**: About, Music, Events, Gallery, Contact
- **SEO Optimized**: Meta tags, structured data, and search engine friendly
- **Fast Loading**: Optimized images and efficient CSS/JS

### 🤖 Automated Agent
- **Real-time Updates**: Automatically checks Mixcloud for new uploads
- **Smart Parsing**: Extracts metadata, thumbnails, and set information
- **Database Tracking**: SQLite database to track all mixes and prevent duplicates
- **Email Notifications**: Optional email alerts for new uploads
- **Background Service**: Runs continuously as a systemd service
- **Error Handling**: Robust error handling and logging
- **Backup System**: Automatic backups before updates

### 🎚️ Technical Features
- **RSS & Web Scraping**: Multiple methods to fetch Mixcloud data
- **Responsive Design**: Tailwind CSS with custom components
- **Modern JavaScript**: ES6+ with smooth animations
- **Python Backend**: Efficient, well-documented Python agent
- **Security**: Secure coding practices and sanitized inputs
- **Monitoring**: Comprehensive logging and status reporting

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip3
- Git
- Web server (nginx/apache) or GitHub Pages

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd djjackspace
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure email notifications** (optional):
   ```bash
   nano .env
   # Update with your email settings
   ```

4. **Start the agent**:
   ```bash
   # For systemd service (if setup as root):
   sudo systemctl start jackspace-agent
   
   # Or run manually:
   python3 jackspace_agent.py --continuous
   ```

## 📁 Project Structure

```
djjackspace/
├── index.html              # Main website file
├── css/
│   └── styles.css          # Professional styling
├── js/
│   └── main.js            # Interactive functionality
├── images/                 # Image assets
├── jackspace_agent.py     # Automated Mixcloud agent
├── requirements.txt       # Python dependencies
├── setup.sh              # Installation script
├── .env                  # Configuration file
├── jackspace-agent.service # Systemd service
└── README.md             # This file
```

## 🛠️ Configuration

### Environment Variables (.env)
```bash
# Mixcloud settings
MIXCLOUD_USERNAME=djjackspace

# Email notifications (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
NOTIFICATION_EMAIL=your-email@gmail.com

# Agent settings
CHECK_INTERVAL_MINUTES=30
LOG_LEVEL=INFO
```

### Website Customization

#### Update Personal Information
Edit `index.html` to customize:
- Name and branding
- About section content
- Event listings
- Contact information
- Social media links

#### Styling
Modify `css/styles.css` to change:
- Color scheme (CSS variables at top)
- Fonts and typography
- Layout and spacing
- Animations and effects

#### Functionality
Update `js/main.js` for:
- Contact form behavior
- Animation triggers
- Interactive features
- Analytics tracking

## 🤖 Agent Usage

### Manual Commands
```bash
# Single check for new mixes
python3 jackspace_agent.py --check-once

# Run continuously with scheduled checks
python3 jackspace_agent.py --continuous

# View help
python3 jackspace_agent.py --help
```

### Service Management
```bash
# Start the service
sudo systemctl start jackspace-agent

# Stop the service
sudo systemctl stop jackspace-agent

# Check status
sudo systemctl status jackspace-agent

# View logs
sudo journalctl -u jackspace-agent -f

# Restart the service
sudo systemctl restart jackspace-agent
```

### Database Operations
The agent uses SQLite to track mixes and updates:
```bash
# View database content
sqlite3 jackspace_agent.db "SELECT * FROM mixes ORDER BY date_added DESC LIMIT 10;"

# Check website updates
sqlite3 jackspace_agent.db "SELECT * FROM website_updates ORDER BY timestamp DESC;"
```

## 📊 Monitoring & Logs

### Log Files
- `jackspace_agent.log` - Agent activity and errors
- System logs via journalctl for service mode

### Monitoring Commands
```bash
# Tail agent logs
tail -f jackspace_agent.log

# Check service logs
journalctl -u jackspace-agent -f --since today

# View recent database activity
sqlite3 jackspace_agent.db "SELECT * FROM website_updates ORDER BY timestamp DESC LIMIT 5;"
```

## 🔧 Troubleshooting

### Common Issues

#### Agent Not Finding New Mixes
1. Check Mixcloud username in `.env`
2. Verify internet connection
3. Check rate limiting (Mixcloud may throttle requests)
4. Review logs for specific errors

#### Website Not Updating
1. Verify file permissions
2. Check if `index.html` is writable
3. Review agent logs for update errors
4. Ensure backup files aren't interfering

#### Email Notifications Not Working
1. Verify SMTP settings in `.env`
2. Check if using app-specific password (Gmail)
3. Test email settings independently
4. Review email-related logs

#### Service Won't Start
1. Check service file syntax: `sudo systemctl status jackspace-agent`
2. Verify file paths in service file
3. Check Python dependencies: `pip3 list`
4. Review systemd logs: `journalctl -u jackspace-agent`

### Debug Mode
Run the agent in debug mode for detailed output:
```bash
LOG_LEVEL=DEBUG python3 jackspace_agent.py --check-once
```

## 🔒 Security Considerations

### File Permissions
- Service runs as `www-data` user
- Minimal required permissions
- Protected system directories

### Data Protection
- Local SQLite database
- No sensitive data in logs
- Environment variables for credentials

### Network Security
- HTTPS for all external requests
- User-Agent identification
- Rate limiting respect

## 🚀 Deployment Options

### GitHub Pages
1. Push to GitHub repository
2. Enable GitHub Pages in settings
3. Set custom domain (optional)
4. Run agent on separate server

### Traditional Web Hosting
1. Upload files via FTP/SFTP
2. Set up cron job for agent
3. Configure proper permissions
4. Set up SSL certificate

### VPS/Cloud Server
1. Full control over environment
2. Run as systemd service
3. Set up monitoring
4. Configure firewall

## 🔄 Updates & Maintenance

### Updating the Agent
```bash
# Pull latest changes
git pull

# Update dependencies
pip3 install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart jackspace-agent
```

### Backup Strategy
- Agent automatically backs up `index.html` before updates
- Database includes all historical data
- Regular backups recommended for images and custom content

### Monitoring Health
- Daily status emails (if configured)
- Log rotation for disk space management
- Database maintenance queries available

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Make changes and test thoroughly

### Code Style
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings for functions
- Include error handling

### Testing
```bash
# Test agent functionality
python3 jackspace_agent.py --check-once

# Validate HTML/CSS
# Use online validators or local tools

# Test responsive design
# Check on multiple devices/browsers
```

## 📄 License

This project is open source. Feel free to modify and adapt for your own DJ website!

## 🎵 About DJ Jackspace

Professional electronic music artist creating cosmic soundscapes and galactic grooves. Specializing in progressive house, techno, and ambient electronic music.

**Website**: [dj.jackspace.com](https://dj.jackspace.com)  
**Mixcloud**: [mixcloud.com/djjackspace](https://www.mixcloud.com/djjackspace/)

---

## 🆘 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Review logs for specific error messages
3. Open an issue in the repository
4. Contact via the website contact form

**Made with ❤️ for the electronic music community**