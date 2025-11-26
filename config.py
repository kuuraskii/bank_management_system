"""
Configuration module for Supabase connection.
"""

# Add your Supabase credentials here
SUPABASE_URL = "https://uezorcqujukhdhkifoqz.supabase.co"
SUPABASE_KEY = "sb_secret_NMY2z56iv6oKjVi_6_A5IA_nvNQjb5O"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured in config.py")
