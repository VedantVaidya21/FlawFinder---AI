#!/usr/bin/env python3
try:
    from app.main import app
    print("App import successful")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
