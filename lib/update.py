from git import Repo
from git.exc import GitCommandError
from lib.misc import log

class updatePage:
    def __init__(self,displayMethod,backToMain):
        self.displayMethod
        self.backToMain = backToMain
    def update(self):
        try:
            # Open the repository
            repo = Repo(".")
            
            if repo.is_dirty(untracked_files=True):
                displayMethod("there are uncommited changes!",method=self.backToMain)
                return

            # Fetch updates from the remote
            log("checking for updates")
            displayMethod("checking for updates...")
            repo.remotes.origin.fetch()

            # Check for updates
            current_branch = repo.active_branch.name
            local_commit = repo.commit(f"refs/heads/{current_branch}")
            remote_commit = repo.commit(f"refs/remotes/origin/{current_branch}")

            if local_commit != remote_commit:
                displayMethod("updating...")
                log("pulling updates")
                repo.remotes.origin.pull()
                displayMethod("successfully updated!\nclose and re open to apply.",method=self.backToMain)
            else:
                displayMethod("already up to date.",method=self.backToMain)
                print("The repository is up to date.")

        except Exception as e:
            print(f"An error occurred: {e}")
            displayMethod("an error occured!",method=self.backToMain)