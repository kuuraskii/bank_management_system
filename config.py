"""
Configuration module for Supabase connection.
"""

# Add your Supabase credentials here
SUPABASE_URL = "https://uezorcqujukhdhkifoqz.supabase.co"
SUPABASE_KEY = "sb_secret_tKehqTTmwlxKz1tQA7Fw9Q_wM0S9cr9"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured in config.py")
