import requests
import datetime
import os
from dotenv import load_dotenv
from dateutil import parser  # Handles timezone-aware datetime parsing
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

load_dotenv()

global commit_count
pr_opened = 0
pr_closed = 0
issues_opened = 0
issues_closed = 0

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
        # print(f"Checking commits in {repo_name}...")  # Debugging line
        commits_url = f"https://api.github.com/repos/{repo_name}/commits?author={username}"
        page = 1

        while True:
            response = requests.get(f"{commits_url}&page={page}", headers=headers)
            # print(f"API response for page {page}: {response.status_code}")  # Debugging line
            
            if response.status_code != 200:
                print(f"Error fetching commits from {repo_name}: {response.status_code} - {response.text}")
                break
            
            commits = response.json()
            if not commits:
                break  # No more commits to process

            for commit in commits:
                commit_date = commit["commit"]["committer"]["date"]
                commit_datetime = parser.isoparse(commit_date).astimezone(datetime.timezone.utc)  # Convert to UTC
                # print(f"  Commit Date: {commit_datetime}")  # Debugging line

                if commit_datetime >= end_of_year:
                    continue  # Skip commits from future years
                if commit_datetime < start_of_year:
                    break  # Stop counting when reaching older commits

                commit_count += 1
                # print(f"  📅 {commit_datetime} - {commit['sha']}")  # Debugging line

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
            # print(f"API response for PR page {page}: {response.status_code}")  # Debugging line

            if response.status_code != 200:
                print(f"Error fetching pull requests from {repo_name}: {response.status_code} - {response.text}")
                break

            prs = response.json()
            if not prs:
                break  # No more PRs to process

            for pr in prs:
                pr_created_at = parser.isoparse(pr["created_at"]).astimezone(datetime.timezone.utc)
                pr_closed_at = pr.get("closed_at")
                # print(f"  PR Created: {pr_created_at}, Closed: {pr_closed_at}")  # Debugging line

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
            # print(f"API response for issue page {page}: {response.status_code}")  # Debugging line

            if response.status_code != 200:
                print(f"Error fetching issues from {repo_name}: {response.status_code} - {response.text}")
                break

            issues = response.json()
            if not issues:
                break  # No more issues to process

            for issue in issues:
                issue_created_at = parser.isoparse(issue["created_at"]).astimezone(datetime.timezone.utc)
                issue_closed_at = issue.get("closed_at")
                # print(f"  Issue Created: {issue_created_at}, Closed: {issue_closed_at}")  # Debugging line

                if issue_created_at >= end_of_year:
                    continue  # Skip issues from future years
                if issue_created_at < start_of_year:
                    break  # Stop counting when reaching older issues

                issues_opened += 1
                if issue_closed_at:
                    issues_closed += 1

            page += 1  # Move to the next page if needed

    return pr_opened, pr_closed, issues_opened, issues_closed

def get_github_wrapped(username, years=None):
    token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
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

        username = f'{username}'
        followers = f"{user_data.get('followers', 'N/A')}"
        public_repos = f"{user_data.get('public_repos', 'N/A')}"

        # Default to last year if no years are provided
        if not years:
            years = [datetime.datetime.now().year - 1]
            # print(f"📅 No years specified. Using data for {years[0]} by default.")
        
        for year in years:
            print(f"\n🎉 GitHub Wrapped {year} 🎉\n")
            print(f"👤 Username: {user_data.get('login', 'N/A')}")
            print(f"📛 Name: {user_data.get('name', 'N/A')}")
            print(f"📝 Bio: {user_data.get('bio', 'N/A')}")
            print(f"📦 Public Repos: {public_repos}")
            print(f"👥 Followers: {followers} | Following: {user_data.get('following', 'N/A')}")
            print(f"🔗 Profile URL: {user_data.get('html_url', 'N/A')}\n")

            print("🚀 Top 5 Repositories:")
            top_repos = sorted(repos_data, key=lambda repo: repo.get('stargazers_count', 0), reverse=True)[:5]
            for repo in top_repos:
                print(f"  ⭐ {repo.get('stargazers_count', 0)} | {repo.get('name', 'N/A')} - {repo.get('html_url', 'N/A')}")


        # for year in years:
            print(f"\n📊 GitHub Activity for {year}:")
            
            # Get commit count for the year
            commit_count = get_commit_count(username, headers, year)
            
            # Get Pull Request and Issue counts for the year
            pr_opened, pr_closed, issues_opened, issues_closed = get_pr_and_issue_counts(username, headers, year)

            commits = commit_count
            prs_opened = pr_opened
            prs_closed = pr_closed
            issues_opened = issues_opened
            issues_closed = issues_closed
            
            print(f"  ✅ Commits: {commit_count}")
            print(f"  🔀 Pull Requests Opened: {pr_opened}")
            print(f"  🔀 Pull Requests Closed: {pr_closed}")
            print(f"  📝 Issues Opened: {issues_opened}")
            print(f"  ❌ Issues Closed: {issues_closed}")
    else:
        print("User not found or API request failed.")
        
            
    # Mock data (replace with actual GitHub data)


    # top_repos = [("Project1", 100), ("Project2", 85), ("Project3", 75)]

    # Pie chart data
    labels = ["Commits", "PRs Opened", "PRs Closed", "Issues Opened", "Issues Closed"]
    sizes = [commits, prs_opened, prs_closed, issues_opened, issues_closed]
    colors = ["#8A2BE2", "#7B68EE", "#6A5ACD", "#483D8B", "#2E1A47"]  # Shades of purple

    # Create figure
    fig, ax = plt.subplots(figsize=(5, 5), facecolor="black")

    # Define a function to show both percentage and actual count
    def autopct_format(p):
        total = sum(sizes)
        count = int(p * total / 100)  # Convert percentage to actual count
        return f"{p:.1f}%\n({count})"  # Show both percentage and count

    # Create the pie chart with updated labels
    ax.pie(sizes, labels=labels, autopct=autopct_format, startangle=140, colors=colors, textprops={'color': "white"})
    # ax.set_title(f"{username}'s GitHub Wrapped", color="white", fontsize=14)

    # Save pie chart as an image
    pie_chart_path = "pie_chart.png"
    plt.savefig(pie_chart_path, bbox_inches="tight", facecolor="#011627")
    plt.close()

    # Create the final image
    img_width, img_height = 800, 600
    img = Image.new("RGB", (img_width, img_height), color="#011627")
    draw = ImageDraw.Draw(img)

    # Load fonts (use a built-in one or specify a ttf path)
    try:
        font_title = ImageFont.truetype("arial.ttf", 30)
        font_text = ImageFont.truetype("arial.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # Add text
    draw.text((20, 20), f"{username}'s GitHub Wrapped", fill="white", font=font_title)
    draw.text((20, 60), f"Public Repos: {public_repos}", fill="white", font=font_text)
    draw.text((20, 90), f"Followers: {followers}", fill="white", font=font_text)
    draw.text((20, 120), "Top Repositories:", fill="white", font=font_text)

    # List top repositories
    y_offset = 150
    for repo in top_repos:
        draw.text((40, y_offset), f"{repo.get('stargazers_count', 0)} - {repo.get('name', 'N/A')}", fill="white", font=font_text)
        y_offset += 30

    # Load and paste the pie chart
    pie_chart = Image.open(pie_chart_path).resize((350, 350))
    img.paste(pie_chart, (400, 150))

    # Save the final image
    output_path = "github_wrapped.png"
    img.save(output_path)
    print(f"Image saved as {output_path}")


if __name__ == "__main__":
    username = "LFGaming"  # Replace with any GitHub username
    years = [2025]  # Specify the years for which you want the data, or leave it as [] for the last year
    get_github_wrapped(username, years)
