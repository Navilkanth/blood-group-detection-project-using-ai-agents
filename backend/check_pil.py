try:
    import PIL
    from PIL import Image
    print(f"PIL Version: {PIL.__version__}")
    print(f"PIL Path: {PIL.__file__}")
    print("SUCCESS: PIL imported and working correctly.")
except Exception as e:
    import traceback
    print("FAILURE: Could not import PIL correctly.")
    traceback.print_exc()
