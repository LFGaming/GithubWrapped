import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_github_wrapped(username):
    token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
    headers = {"Authorization": f"token {token}"} if token else {}
    
    url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"
    events_url = f"https://api.github.com/users/{username}/events/public"
    
    response = requests.get(url, headers=headers)
    repos_response = requests.get(repos_url, headers=headers)
    events_response = requests.get(events_url, headers=headers)
    
    if response.status_code == 200 and repos_response.status_code == 200 and events_response.status_code == 200:
        user_data = response.json()
        repos_data = repos_response.json()
        events_data = events_response.json()
        
        print("\n🎉 GitHub Wrapped 2024 🎉\n")
        print(f"👤 Username: {user_data.get('login', 'N/A')}")
        print(f"📛 Name: {user_data.get('name', 'N/A')}")
        print(f"📝 Bio: {user_data.get('bio', 'N/A')}")
        print(f"📦 Public Repos: {user_data.get('public_repos', 'N/A')}")
        print(f"👥 Followers: {user_data.get('followers', 'N/A')} | Following: {user_data.get('following', 'N/A')}")
        print(f"🔗 Profile URL: {user_data.get('html_url', 'N/A')}\n")
        
        print("🚀 Top 5 Repositories:")
        top_repos = sorted(repos_data, key=lambda repo: repo.get('stargazers_count', 0), reverse=True)[:5]
        for repo in top_repos:
            print(f"  ⭐ {repo.get('stargazers_count', 0)} | {repo.get('name', 'N/A')} - {repo.get('html_url', 'N/A')}")
        
        one_year_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)).isoformat()
        commit_count, pr_count, issues_opened, issues_closed = 0, 0, 0, 0
        
        def fetch_all_commits(repo_name, username):
            commits_url = f"https://api.github.com/repos/{repo_name}/commits?author={username}&since={one_year_ago}&per_page=100"
            page = 1
            count = 0
            while True:
                response = requests.get(f"{commits_url}&page={page}", headers=headers)
                if response.status_code != 200:
                    break
                commits = response.json()
                if not commits:
                    break
                count += len(commits)
                page += 1
            return count
        
        for repo in repos_data:
            repo_name = repo.get('full_name')
            commit_count += fetch_all_commits(repo_name, username)
            
        for event in events_data:
            event_type = event.get('type')
            created_at = event.get('created_at', '')
            if created_at >= one_year_ago:
                if event_type == 'PullRequestEvent':
                    pr_count += 1
                elif event_type == 'IssuesEvent':
                    action = event.get('payload', {}).get('action')
                    if action == 'opened':
                        issues_opened += 1
                    elif action == 'closed':
                        issues_closed += 1
        
        print("\n📊 GitHub Activity in the Last Year:")
        print(f"  ✅ Commits: {commit_count}")
        print(f"  🔀 Pull Requests: {pr_count}")
        print(f"  📝 Issues Opened: {issues_opened}")
        print(f"  ❌ Issues Closed: {issues_closed}")
    else:
        print("User not found or API request failed.")

if __name__ == "__main__":
    # Predefined username to avoid input issues
    username = "LFGaming"  # Replace with any GitHub username
    get_github_wrapped(username)
