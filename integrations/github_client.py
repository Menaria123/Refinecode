import requests

class GitHubClient:
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo # format: owner/repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_pr_files(self, pr_number: int):
        """
        Fetch files changed in a PR.
        """
        url = f"{self.base_url}/repos/{self.repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def post_comment(self, pr_number: int, body: str):
        """
        Post a general comment on the PR.
        """
        url = f"{self.base_url}/repos/{self.repo}/issues/{pr_number}/comments"
        data = {"body": body}
        response = requests.post(url, headers=self.headers, json=data)
        return response.status_code == 201
