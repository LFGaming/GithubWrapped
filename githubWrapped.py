# import requests
# import datetime
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_2024_commit_count(username, headers):
#     """
#     Fetches commits for the given user and counts only those made in 2024.
#     Uses pagination to get all commits without excessive API calls.
#     """
#     commits_url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc"
#     page = 1
#     commit_count = 0
#     start_of_2024 = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)

#     while True:
#         response = requests.get(f"{commits_url}&page={page}", headers=headers)

#         if response.status_code != 200:
#             print(f"Error fetching commits: {response.status_code} - {response.text}")
#             return commit_count

#         commit_data = response.json()
#         items = commit_data.get("items", [])

#         if not items:
#             break  # No more commits to process

#         for commit in items:
#             commit_date = commit["commit"]["committer"]["date"]
#             commit_datetime = datetime.datetime.fromisoformat(commit_date.rstrip("Z"))

#             if commit_datetime < start_of_2024:
#                 return commit_count  # Stop counting when reaching older commits

#             commit_count += 1

#         page += 1  # Move to the next page if needed

#     return commit_count

# def main():
#     username = "LFGaming"  # Replace with any GitHub username
#     token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
#     headers = {
#         "Authorization": f"token {token}",
#         "Accept": "application/vnd.github.cloak-preview+json"
#     } if token else {}

#     commit_count_2024 = get_2024_commit_count(username, headers)
    
#     print(f"🗓️ Commits made by {username} in 2024: {commit_count_2024}")

# if __name__ == "__main__":
#     main()


import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_2024_commit_count(username, headers):
    """
    Fetches commits for the given user and counts only those made in 2024.
    Uses pagination to get all commits without excessive API calls.
    """
    commits_url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc"
    page = 1
    commit_count = 0
    start_of_2024 = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)

    while True:
        response = requests.get(f"{commits_url}&page={page}", headers=headers)

        if response.status_code != 200:
            print(f"Error fetching commits: {response.status_code} - {response.text}")
            return commit_count

        commit_data = response.json()
        items = commit_data.get("items", [])

        if not items:
            break  # No more commits to process

        for commit in items:
            commit_date = commit["commit"]["committer"]["date"]
            commit_datetime = datetime.datetime.fromisoformat(commit_date.rstrip("Z"))

            if commit_datetime < start_of_2024:
                return commit_count  # Stop counting when reaching older commits

            commit_count += 1

        page += 1  # Move to the next page if needed

    return commit_count


def get_last_year_commit_count(username, headers):
    """
    Fetches all commits for the user, paginating as needed.
    Counts only those from the last year while minimizing API calls.
    """
    commits_url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc"
    page = 1
    commit_count = 0
    one_year_ago = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)

    while True:
        response = requests.get(f"{commits_url}&page={page}", headers=headers)

        if response.status_code != 200:
            print(f"Error fetching commits: {response.status_code} - {response.text}")
            return commit_count

        commit_data = response.json()
        items = commit_data.get("items", [])

        if not items:
            break  # No more commits to process

        for commit in items:
            commit_date = commit["commit"]["committer"]["date"]
            commit_datetime = datetime.datetime.fromisoformat(commit_date.rstrip("Z"))

            if commit_datetime < one_year_ago:
                return commit_count  # Stop counting when we hit older commits

            commit_count += 1

        page += 1  # Move to the next page if needed

    return commit_count

def get_github_wrapped(username):
    token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.cloak-preview+json"
    } if token else {}

    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"
    events_url = f"https://api.github.com/users/{username}/events/public"

    response = requests.get(user_url, headers=headers)
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

        # Get commit count (pagination enabled)
        # commit_count = get_last_year_commit_count(username, headers)
        commit_count_2024 = get_2024_commit_count(username, headers)

        pr_count = 0
        issues_opened = 0
        issues_closed = 0

        one_year_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)).isoformat()
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
            else:
                break

        print("\n📊 GitHub Activity in the Last Year:")
        print(f"  ✅ Commits: {commit_count_2024}")
        print(f"  🔀 Pull Requests: {pr_count}")
        print(f"  📝 Issues Opened: {issues_opened}")
        print(f"  ❌ Issues Closed: {issues_closed}")

    else:
        print("User not found or API request failed.")

if __name__ == "__main__":
    username = "LFGaming"  # Replace with any GitHub username
    get_github_wrapped(username)
