import os

print("Terminal Environment Variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")