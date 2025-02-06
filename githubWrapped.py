import requests

def get_github_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"Username: {user_data.get('login', 'N/A')}")
        print(f"Name: {user_data.get('name', 'N/A')}")
        print(f"Bio: {user_data.get('bio', 'N/A')}")
        print(f"Public Repos: {user_data.get('public_repos', 'N/A')}")
        print(f"Followers: {user_data.get('followers', 'N/A')}")
        print(f"Following: {user_data.get('following', 'N/A')}")
        print(f"Profile URL: {user_data.get('html_url', 'N/A')}")
    else:
        print("User not found or API request failed.")

if __name__ == "__main__":
    # Predefined username to avoid input issues
    username = "LFGaming"  # Replace with any GitHub username
    get_github_user(username)
