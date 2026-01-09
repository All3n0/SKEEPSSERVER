#!/usr/bin/env python3
"""
Script to run before Railway redeploy.
"""
import requests
import os
import time
import sys

def main():
    # Get the current service URL - use Railway's internal URL
    service_url = os.environ.get('RAILWAY_STATIC_URL', 'http://localhost:8080')
    admin_token = os.environ.get('ADMIN_TOKEN', 'secret-token-123')
    
    print(f"🔄 Pre-deploy backup starting for {service_url}")
    
    try:
        # Create backup
        response = requests.post(
            f"{service_url}/api/admin/backup",
            headers={'Authorization': f'Bearer {admin_token}'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backup created: {data.get('message')}")
        else:
            print(f"❌ Backup failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")
        print("This is normal if the service is not running yet.")
    
    print("✨ Pre-deploy backup completed")

if __name__ == '__main__':
    main()