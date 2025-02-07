# # import requests
# # import datetime
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # def get_2024_commit_count(username, headers):
# #     """
# #     Fetches commits for the given user and counts only those made in 2024.
# #     Uses pagination to get all commits without excessive API calls.
# #     """
# #     commits_url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc"
# #     page = 1
# #     commit_count = 0
# #     start_of_2024 = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)

# #     while True:
# #         response = requests.get(f"{commits_url}&page={page}", headers=headers)

# #         if response.status_code != 200:
# #             print(f"Error fetching commits: {response.status_code} - {response.text}")
# #             return commit_count

# #         commit_data = response.json()
# #         items = commit_data.get("items", [])

# #         if not items:
# #             break  # No more commits to process

# #         for commit in items:
# #             commit_date = commit["commit"]["committer"]["date"]
# #             commit_datetime = datetime.datetime.fromisoformat(commit_date.rstrip("Z"))

# #             if commit_datetime < start_of_2024:
# #                 return commit_count  # Stop counting when reaching older commits

# #             commit_count += 1

# #         page += 1  # Move to the next page if needed

# #     return commit_count

# # def main():
# #     username = "LFGaming"  # Replace with any GitHub username
# #     token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
# #     headers = {
# #         "Authorization": f"token {token}",
# #         "Accept": "application/vnd.github.cloak-preview+json"
# #     } if token else {}

# #     commit_count_2024 = get_2024_commit_count(username, headers)
    
# #     print(f"🗓️ Commits made by {username} in 2024: {commit_count_2024}")

# # if __name__ == "__main__":
# #     main()


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


# def get_last_year_commit_count(username, headers):
#     """
#     Fetches all commits for the user, paginating as needed.
#     Counts only those from the last year while minimizing API calls.
#     """
#     commits_url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc"
#     page = 1
#     commit_count = 0
#     one_year_ago = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)

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

#             if commit_datetime < one_year_ago:
#                 return commit_count  # Stop counting when we hit older commits

#             commit_count += 1

#         page += 1  # Move to the next page if needed

#     return commit_count

# def get_github_wrapped(username):
#     token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
#     headers = {
#         "Authorization": f"token {token}",
#         "Accept": "application/vnd.github.cloak-preview+json"
#     } if token else {}

#     user_url = f"https://api.github.com/users/{username}"
#     repos_url = f"https://api.github.com/users/{username}/repos"
#     events_url = f"https://api.github.com/users/{username}/events/public"

#     response = requests.get(user_url, headers=headers)
#     repos_response = requests.get(repos_url, headers=headers)
#     events_response = requests.get(events_url, headers=headers)

#     if response.status_code == 200 and repos_response.status_code == 200 and events_response.status_code == 200:
#         user_data = response.json()
#         repos_data = repos_response.json()
#         events_data = events_response.json()

#         print("\n🎉 GitHub Wrapped 2024 🎉\n")
#         print(f"👤 Username: {user_data.get('login', 'N/A')}")
#         print(f"📛 Name: {user_data.get('name', 'N/A')}")
#         print(f"📝 Bio: {user_data.get('bio', 'N/A')}")
#         print(f"📦 Public Repos: {user_data.get('public_repos', 'N/A')}")
#         print(f"👥 Followers: {user_data.get('followers', 'N/A')} | Following: {user_data.get('following', 'N/A')}")
#         print(f"🔗 Profile URL: {user_data.get('html_url', 'N/A')}\n")

#         print("🚀 Top 5 Repositories:")
#         top_repos = sorted(repos_data, key=lambda repo: repo.get('stargazers_count', 0), reverse=True)[:5]
#         for repo in top_repos:
#             print(f"  ⭐ {repo.get('stargazers_count', 0)} | {repo.get('name', 'N/A')} - {repo.get('html_url', 'N/A')}")

#         # Get commit count (pagination enabled)
#         # commit_count = get_last_year_commit_count(username, headers)
#         commit_count_2024 = get_2024_commit_count(username, headers)

#         pr_count = 0
#         issues_opened = 0
#         issues_closed = 0

#         one_year_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)).isoformat()
#         for event in events_data:
#             event_type = event.get('type')
#             created_at = event.get('created_at', '')

#             if created_at >= one_year_ago:
#                 if event_type == 'PullRequestEvent':
#                     pr_count += 1
#                 elif event_type == 'IssuesEvent':
#                     action = event.get('payload', {}).get('action')
#                     if action == 'opened':
#                         issues_opened += 1
#                     elif action == 'closed':
#                         issues_closed += 1
#             else:
#                 break

        # print("\n📊 GitHub Activity in the Last Year:")
        # print(f"  ✅ Commits: {commit_count_2024}")
        # print(f"  🔀 Pull Requests: {pr_count}")
        # print(f"  📝 Issues Opened: {issues_opened}")
        # print(f"  ❌ Issues Closed: {issues_closed}")

#     else:
#         print("User not found or API request failed.")

# if __name__ == "__main__":
#     username = "LFGaming"  # Replace with any GitHub username
#     get_github_wrapped(username)

import requests
import datetime
import os
from dotenv import load_dotenv
from dateutil import parser  # Handles timezone-aware datetime parsing

load_dotenv()

def get_commit_count(username, headers, year):
    """
    Fetches commits for the given user from all repositories and counts only those made in the specified year.
    Includes private commits if the token has the necessary permissions.
    """
    repos_url = f"https://api.github.com/user/repos?visibility=all&affiliation=owner"
    response = requests.get(repos_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching repositories: {response.status_code} - {response.text}")
        return 0

    repos = response.json()
    commit_count = 0
    start_of_year = datetime.datetime(year, 1, 1, tzinfo=datetime.timezone.utc)
    end_of_year = datetime.datetime(year + 1, 1, 1, tzinfo=datetime.timezone.utc)

    for repo in repos:
        repo_name = repo["full_name"]
        print(f"Checking commits in {repo_name}...")  # Debugging line
        commits_url = f"https://api.github.com/repos/{repo_name}/commits?author={username}"
        page = 1

        while True:
            response = requests.get(f"{commits_url}&page={page}", headers=headers)
            print(f"API response for page {page}: {response.status_code}")  # Debugging line
            
            if response.status_code != 200:
                print(f"Error fetching commits from {repo_name}: {response.status_code} - {response.text}")
                break
            
            commits = response.json()
            if not commits:
                break  # No more commits to process

            for commit in commits:
                commit_date = commit["commit"]["committer"]["date"]
                commit_datetime = parser.isoparse(commit_date).astimezone(datetime.timezone.utc)  # Convert to UTC
                print(f"  Commit Date: {commit_datetime}")  # Debugging line

                if commit_datetime >= end_of_year:
                    continue  # Skip commits from future years
                if commit_datetime < start_of_year:
                    break  # Stop counting when reaching older commits

                commit_count += 1
                print(f"  📅 {commit_datetime} - {commit['sha']}")  # Debugging line

            page += 1  # Move to the next page if needed

    return commit_count

def get_pr_and_issue_counts(username, headers, year):
    """
    Fetches the number of Pull Requests and Issues (opened and closed) for the given user in the specified year.
    """
    repos_url = f"https://api.github.com/user/repos?visibility=all&affiliation=owner"
    response = requests.get(repos_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching repositories: {response.status_code} - {response.text}")
        return 0, 0, 0, 0  # Pull requests opened, closed, issues opened, closed

    repos = response.json()
    pr_opened = 0
    pr_closed = 0
    issues_opened = 0
    issues_closed = 0
    start_of_year = datetime.datetime(year, 1, 1, tzinfo=datetime.timezone.utc)
    end_of_year = datetime.datetime(year + 1, 1, 1, tzinfo=datetime.timezone.utc)

    for repo in repos:
        repo_name = repo["full_name"]

        # Fetch Pull Requests
        pr_url = f"https://api.github.com/repos/{repo_name}/pulls?state=all&sort=updated"
        page = 1

        while True:
            response = requests.get(f"{pr_url}&page={page}", headers=headers)
            print(f"API response for PR page {page}: {response.status_code}")  # Debugging line

            if response.status_code != 200:
                print(f"Error fetching pull requests from {repo_name}: {response.status_code} - {response.text}")
                break

            prs = response.json()
            if not prs:
                break  # No more PRs to process

            for pr in prs:
                pr_created_at = parser.isoparse(pr["created_at"]).astimezone(datetime.timezone.utc)
                pr_closed_at = pr.get("closed_at")
                print(f"  PR Created: {pr_created_at}, Closed: {pr_closed_at}")  # Debugging line

                if pr_created_at >= end_of_year:
                    continue  # Skip PRs from future years
                if pr_created_at < start_of_year:
                    break  # Stop counting when reaching older PRs

                pr_opened += 1
                if pr_closed_at:
                    pr_closed += 1

            page += 1  # Move to the next page if needed

        # Fetch Issues
        issues_url = f"https://api.github.com/repos/{repo_name}/issues?state=all"
        page = 1

        while True:
            response = requests.get(f"{issues_url}&page={page}", headers=headers)
            print(f"API response for issue page {page}: {response.status_code}")  # Debugging line

            if response.status_code != 200:
                print(f"Error fetching issues from {repo_name}: {response.status_code} - {response.text}")
                break

            issues = response.json()
            if not issues:
                break  # No more issues to process

            for issue in issues:
                issue_created_at = parser.isoparse(issue["created_at"]).astimezone(datetime.timezone.utc)
                issue_closed_at = issue.get("closed_at")
                print(f"  Issue Created: {issue_created_at}, Closed: {issue_closed_at}")  # Debugging line

                if issue_created_at >= end_of_year:
                    continue  # Skip issues from future years
                if issue_created_at < start_of_year:
                    break  # Stop counting when reaching older issues

                issues_opened += 1
                if issue_closed_at:
                    issues_closed += 1

            page += 1  # Move to the next page if needed

    return pr_opened, pr_closed, issues_opened, issues_closed

def get_github_wrapped(username):
    token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    } if token else {}

    user_url = "https://api.github.com/user"  # Accessing private user data
    response = requests.get(user_url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()

        print("\n🎉 GitHub Wrapped 🎉\n")
        print(f"👤 Username: {user_data.get('login', 'N/A')}")
        print(f"📛 Name: {user_data.get('name', 'N/A')}")
        print(f"🔗 Profile URL: {user_data.get('html_url', 'N/A')}\n")

        # Get commit count for last year only
        last_year = datetime.datetime.now().year - 1
        commit_count_last_year = get_commit_count(username, headers, last_year)
        
        # Get Pull Request and Issue counts for last year
        pr_opened, pr_closed, issues_opened, issues_closed = get_pr_and_issue_counts(username, headers, last_year)

        print("\n📊 GitHub Activity in the Last Year:")
        print(f"  ✅ Commits: {commit_count_last_year}")
        print(f"  🔀 Pull Requests Opened: {pr_opened}")
        print(f"  🔀 Pull Requests Closed: {pr_closed}")
        print(f"  📝 Issues Opened: {issues_opened}")
        print(f"  ❌ Issues Closed: {issues_closed}")
    else:
        print("User not found or API request failed.")

if __name__ == "__main__":
    username = "LFGaming"  # Replace with any GitHub username
    get_github_wrapped(username)
