import os

base_dir = os.path.join(os.getcwd(), 'data')
print(f"Walking {base_dir}")
for root, dirs, files in os.walk(base_dir):
    print(f"Root: {root}, Files: {len(files)}")
    for file in files:
        if file.endswith('.xlsx'):
            print(f"  Found Excel: {file}")
