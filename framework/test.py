class Colors:
    
    def __getattr__(self, name):
        return name

# Usage
colors = Colors()
print(colors.blue)  # Outputs: blue
print(colors.red)   # Outputs: red
print(colors.grey) # Outputs: green
print(colors.any_color) # Outputs: any_color