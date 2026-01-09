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
        # First, try to fix database location if needed
        print("🔧 Checking database location...")
        fix_response = requests.post(
            f"{service_url}/api/admin/fix-db",
            headers={'Authorization': f'Bearer {admin_token}'},
            timeout=10
        )
        
        if fix_response.status_code == 200:
            print(f"✅ {fix_response.json().get('message')}")
        elif fix_response.status_code == 404:
            print(f"ℹ️  Database already in correct location or not found")
        else:
            print(f"⚠️  Could not fix database: {fix_response.text}")
        
        # Create backup
        print("💾 Creating backup...")
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