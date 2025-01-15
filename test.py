from git import Repo
from git.exc import GitCommandError

def check_and_pull_updates(repo_path="."):
    try:
        # Open the repository
        repo = Repo(repo_path)
        
        if repo.is_dirty(untracked_files=True):
            print("The repository has uncommitted changes. Please commit or stash them first.")
            return

        # Fetch updates from the remote
        print("Fetching updates from the remote...")
        repo.remotes.origin.fetch()

        # Check for updates
        current_branch = repo.active_branch.name
        local_commit = repo.commit(f"refs/heads/{current_branch}")
        remote_commit = repo.commit(f"refs/remotes/origin/{current_branch}")

        if local_commit != remote_commit:
            print(f"Updates are available for branch '{current_branch}'. Pulling updates...")
            repo.remotes.origin.pull()
            print("Updates pulled successfully.")
        else:
            print("The repository is up to date.")

    except GitCommandError as e:
        print(f"Git command error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function in the current directory
check_and_pull_updates()
