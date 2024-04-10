import subprocess

def get_pods(namespace=None):
    command = ['kubectl', 'get', 'pods']
    if namespace:
        command.extend(['-n', namespace])
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(e.stderr)

def main():
    print("Welcome to Kubernetes CLI")
    print("Choose an action:")
    print("1. Get pods")
    choice = input("Enter your choice: ")

    if choice == "1":
        namespace = input("Enter namespace (press Enter for default): ")
        get_pods(namespace.strip() if namespace else None)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
