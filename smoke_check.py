"""Smoke check หลัง Deploy: เปิดแอปจากโฟลเดอร์ที่ deploy แล้วเรียก /health"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app  # noqa: E402

response = create_app().test_client().get("/health")
print("Smoke test:", response.status_code, response.get_json())
sys.exit(0 if response.status_code == 200 else 1)
