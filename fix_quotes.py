import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py'):
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Replace escaped triple quotes with actual triple quotes
                new_content = content.replace('\\"\\"\\"', '"""')
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"Fixed {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
