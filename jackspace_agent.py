#!/usr/bin/env python3
"""
DJ Jackspace Website Management Agent
Automatically scrapes Mixcloud for new sets and updates the website
"""

import requests
import json
import re
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import schedule
from bs4 import BeautifulSoup
import feedparser
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
MIXCLOUD_USERNAME = "djjackspace"
MIXCLOUD_URL = f"https://www.mixcloud.com/{MIXCLOUD_USERNAME}/"
MIXCLOUD_FEED_URL = f"https://www.mixcloud.com/{MIXCLOUD_USERNAME}/feed/"
DATABASE_FILE = "jackspace_agent.db"
LOG_FILE = "jackspace_agent.log"
WEBSITE_ROOT = Path(".")
INDEX_FILE = WEBSITE_ROOT / "index.html"

# Email settings (configure these with your SMTP settings)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "your-email@gmail.com"  # Replace with your email
EMAIL_PASS = "your-app-password"     # Replace with your app password
NOTIFICATION_EMAIL = "your-email@gmail.com"  # Where to send notifications

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MixcloudScraper:
    """Handles scraping Mixcloud for new content"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DJ Jackspace Website Agent 1.0'
        })
    
    def get_latest_mixes(self, limit: int = 10) -> List[Dict]:
        """
        Scrape the latest mixes from Mixcloud
        Returns list of mix dictionaries with metadata
        """
        try:
            # Try RSS feed first (more reliable)
            mixes = self._get_mixes_from_rss(limit)
            if mixes:
                return mixes
            
            # Fallback to web scraping
            return self._get_mixes_from_web(limit)
            
        except Exception as e:
            logger.error(f"Error getting latest mixes: {e}")
            return []
    
    def _get_mixes_from_rss(self, limit: int) -> List[Dict]:
        """Get mixes from RSS feed"""
        try:
            feed = feedparser.parse(MIXCLOUD_FEED_URL)
            mixes = []
            
            for entry in feed.entries[:limit]:
                mix_data = {
                    'title': entry.title,
                    'url': entry.link,
                    'description': getattr(entry, 'description', ''),
                    'published': entry.published,
                    'published_parsed': entry.published_parsed,
                    'thumbnail': self._extract_thumbnail(entry),
                    'duration': self._extract_duration(entry),
                    'tags': self._extract_tags(entry),
                    'play_count': 0,  # Not available in RSS
                    'favorite_count': 0,  # Not available in RSS
                }
                
                # Generate mix ID from URL
                mix_data['mix_id'] = self._extract_mix_id(mix_data['url'])
                mixes.append(mix_data)
            
            return mixes
            
        except Exception as e:
            logger.error(f"Error parsing RSS feed: {e}")
            return []
    
    def _get_mixes_from_web(self, limit: int) -> List[Dict]:
        """Fallback web scraping method"""
        try:
            response = self.session.get(MIXCLOUD_URL)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            mixes = []
            
            # Look for cloudcast items (Mixcloud's term for mixes)
            cloudcast_items = soup.find_all('div', class_='cloudcast-item')[:limit]
            
            for item in cloudcast_items:
                try:
                    title_elem = item.find('h3') or item.find('h4')
                    link_elem = item.find('a')
                    
                    if title_elem and link_elem:
                        mix_data = {
                            'title': title_elem.get_text(strip=True),
                            'url': f"https://www.mixcloud.com{link_elem.get('href')}",
                            'description': '',
                            'published': '',
                            'published_parsed': None,
                            'thumbnail': '',
                            'duration': '',
                            'tags': [],
                            'play_count': 0,
                            'favorite_count': 0,
                        }
                        
                        mix_data['mix_id'] = self._extract_mix_id(mix_data['url'])
                        mixes.append(mix_data)
                        
                except Exception as e:
                    logger.warning(f"Error parsing mix item: {e}")
                    continue
            
            return mixes
            
        except Exception as e:
            logger.error(f"Error scraping web page: {e}")
            return []
    
    def _extract_mix_id(self, url: str) -> str:
        """Extract mix ID from Mixcloud URL"""
        match = re.search(r'/([^/]+)/?$', url)
        return match.group(1) if match else hashlib.md5(url.encode()).hexdigest()[:8]
    
    def _extract_thumbnail(self, entry) -> str:
        """Extract thumbnail URL from RSS entry"""
        if hasattr(entry, 'media_thumbnail'):
            return entry.media_thumbnail[0]['url'] if entry.media_thumbnail else ''
        return ''
    
    def _extract_duration(self, entry) -> str:
        """Extract duration from RSS entry"""
        if hasattr(entry, 'itunes_duration'):
            return entry.itunes_duration
        return ''
    
    def _extract_tags(self, entry) -> List[str]:
        """Extract tags from RSS entry"""
        if hasattr(entry, 'tags'):
            return [tag.term for tag in entry.tags]
        return []

class DatabaseManager:
    """Handles database operations for tracking mixes"""
    
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mixes (
                    mix_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    description TEXT,
                    published TEXT,
                    thumbnail TEXT,
                    duration TEXT,
                    tags TEXT,
                    play_count INTEGER DEFAULT 0,
                    favorite_count INTEGER DEFAULT 0,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_featured BOOLEAN DEFAULT FALSE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS website_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    update_type TEXT NOT NULL,
                    description TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def mix_exists(self, mix_id: str) -> bool:
        """Check if a mix already exists in the database"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM mixes WHERE mix_id = ?', (mix_id,))
            return cursor.fetchone() is not None
    
    def add_mix(self, mix_data: Dict) -> bool:
        """Add a new mix to the database"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO mixes (
                        mix_id, title, url, description, published, 
                        thumbnail, duration, tags, play_count, favorite_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    mix_data['mix_id'],
                    mix_data['title'],
                    mix_data['url'],
                    mix_data.get('description', ''),
                    mix_data.get('published', ''),
                    mix_data.get('thumbnail', ''),
                    mix_data.get('duration', ''),
                    json.dumps(mix_data.get('tags', [])),
                    mix_data.get('play_count', 0),
                    mix_data.get('favorite_count', 0)
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding mix to database: {e}")
            return False
    
    def get_recent_mixes(self, limit: int = 10) -> List[Dict]:
        """Get recent mixes from database"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM mixes 
                ORDER BY date_added DESC 
                LIMIT ?
            ''', (limit,))
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def log_update(self, update_type: str, description: str):
        """Log a website update"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO website_updates (update_type, description)
                VALUES (?, ?)
            ''', (update_type, description))
            conn.commit()

class WebsiteUpdater:
    """Handles updating the website with new content"""
    
    def __init__(self, index_file: Path):
        self.index_file = index_file
    
    def update_mixcloud_section(self, mixes: List[Dict]) -> bool:
        """Update the Mixcloud section with new mixes"""
        try:
            if not self.index_file.exists():
                logger.error(f"Index file not found: {self.index_file}")
                return False
            
            # Read current HTML
            with open(self.index_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Generate new Mixcloud iframes
            mixcloud_html = self._generate_mixcloud_html(mixes)
            
            # Replace the mixcloud container content
            pattern = r'(<div id="mixcloud-container"[^>]*>)(.*?)(</div>)'
            replacement = f'\\1\n{mixcloud_html}\n        \\3'
            
            updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
            
            if updated_html != html_content:
                # Backup the original file
                backup_file = self.index_file.with_suffix('.html.backup')
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Write updated content
                with open(self.index_file, 'w', encoding='utf-8') as f:
                    f.write(updated_html)
                
                logger.info("Website updated with new Mixcloud content")
                return True
            else:
                logger.info("No website update needed")
                return False
                
        except Exception as e:
            logger.error(f"Error updating website: {e}")
            return False
    
    def _generate_mixcloud_html(self, mixes: List[Dict]) -> str:
        """Generate HTML for Mixcloud iframes"""
        html_parts = []
        
        for mix in mixes[:6]:  # Show top 6 mixes
            iframe_url = self._get_mixcloud_iframe_url(mix['url'])
            html_parts.append(f'''        <div class="mixcloud-set">
          <iframe width="100%" height="120" 
                  src="{iframe_url}" 
                  frameborder="0" class="rounded-lg">
          </iframe>
        </div>''')
        
        return '\n'.join(html_parts)
    
    def _get_mixcloud_iframe_url(self, mix_url: str) -> str:
        """Convert Mixcloud URL to iframe embed URL"""
        # Extract the path from the mix URL
        match = re.search(r'mixcloud\.com(/.*)', mix_url)
        if match:
            path = match.group(1)
            return f"https://www.mixcloud.com/widget/iframe/?hide_cover=1&mini=1&feed={path}"
        return mix_url

class NotificationManager:
    """Handles email notifications"""
    
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email_user = EMAIL_USER
        self.email_pass = EMAIL_PASS
    
    def send_notification(self, subject: str, message: str, recipient: str = None):
        """Send email notification"""
        if not recipient:
            recipient = NOTIFICATION_EMAIL
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            
            logger.info(f"Notification sent: {subject}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")

class JackspaceAgent:
    """Main agent class that coordinates all operations"""
    
    def __init__(self):
        self.scraper = MixcloudScraper()
        self.db = DatabaseManager(DATABASE_FILE)
        self.updater = WebsiteUpdater(INDEX_FILE)
        self.notifier = NotificationManager()
    
    def check_for_new_mixes(self):
        """Main method to check for new mixes and update website"""
        logger.info("Starting check for new mixes...")
        
        try:
            # Get latest mixes from Mixcloud
            latest_mixes = self.scraper.get_latest_mixes(limit=20)
            
            if not latest_mixes:
                logger.warning("No mixes found from Mixcloud")
                return
            
            # Check for new mixes
            new_mixes = []
            for mix in latest_mixes:
                if not self.db.mix_exists(mix['mix_id']):
                    new_mixes.append(mix)
                    self.db.add_mix(mix)
            
            if new_mixes:
                logger.info(f"Found {len(new_mixes)} new mixes")
                
                # Update website
                success = self.updater.update_mixcloud_section(latest_mixes)
                
                if success:
                    # Log the update
                    self.db.log_update(
                        'mixcloud_update',
                        f'Added {len(new_mixes)} new mixes'
                    )
                    
                    # Send notification
                    self._send_update_notification(new_mixes)
                    
                    logger.info("Website successfully updated")
                else:
                    logger.error("Failed to update website")
            else:
                logger.info("No new mixes found")
                
        except Exception as e:
            logger.error(f"Error in check_for_new_mixes: {e}")
            self.notifier.send_notification(
                "DJ Jackspace Agent Error",
                f"Error occurred while checking for new mixes: {e}"
            )
    
    def _send_update_notification(self, new_mixes: List[Dict]):
        """Send notification about new mixes"""
        if not new_mixes:
            return
        
        subject = f"DJ Jackspace: {len(new_mixes)} new mix{'es' if len(new_mixes) > 1 else ''} added"
        
        message = f"""
        <h2>New Mixcloud uploads detected!</h2>
        <p>The following mix{'es have' if len(new_mixes) > 1 else ' has'} been added to your website:</p>
        <ul>
        """
        
        for mix in new_mixes:
            message += f'<li><strong>{mix["title"]}</strong><br><a href="{mix["url"]}">{mix["url"]}</a></li>'
        
        message += """
        </ul>
        <p>Your website has been automatically updated with the latest content.</p>
        <p>Visit your site: <a href="https://dj.jackspace.com">https://dj.jackspace.com</a></p>
        """
        
        self.notifier.send_notification(subject, message)
    
    def run_continuous(self):
        """Run the agent continuously with scheduled checks"""
        logger.info("Starting DJ Jackspace Agent in continuous mode...")
        
        # Schedule checks
        schedule.every(30).minutes.do(self.check_for_new_mixes)
        schedule.every().day.at("09:00").do(self._daily_maintenance)
        
        # Run initial check
        self.check_for_new_mixes()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled tasks
    
    def _daily_maintenance(self):
        """Daily maintenance tasks"""
        logger.info("Running daily maintenance...")
        
        # Clean up old backups (keep last 7 days)
        backup_files = list(Path('.').glob('*.backup'))
        for backup_file in backup_files:
            if backup_file.stat().st_mtime < time.time() - (7 * 24 * 60 * 60):
                backup_file.unlink()
                logger.info(f"Removed old backup: {backup_file}")
        
        # Send daily status report
        recent_mixes = self.db.get_recent_mixes(limit=5)
        self.notifier.send_notification(
            "DJ Jackspace Agent - Daily Status",
            f"Agent is running normally. {len(recent_mixes)} mixes in recent database."
        )

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DJ Jackspace Website Management Agent')
    parser.add_argument('--check-once', action='store_true', 
                       help='Run a single check and exit')
    parser.add_argument('--continuous', action='store_true',
                       help='Run continuously with scheduled checks')
    
    args = parser.parse_args()
    
    agent = JackspaceAgent()
    
    if args.check_once:
        agent.check_for_new_mixes()
    elif args.continuous:
        agent.run_continuous()
    else:
        # Default: run once
        agent.check_for_new_mixes()

if __name__ == "__main__":
    main()