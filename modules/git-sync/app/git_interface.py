import git
import os
import logging


class GitInterface:

    def __init__(self, git_local_path, git_remote_url, _hash):

        self.git_local_path = git_local_path
        self.git_remote_url = git_remote_url
        self.__hash__ = _hash

        self.repo_name = None
        self.repo = self.register_git_repo()

    # Register Git Repo Instance
    def register_git_repo(self):

        self.repo_name = self.git_remote_url.split('.git')[0].split('/')[-1]
        self.git_local_path = self.git_local_path + "/" + str(self.repo_name) + "-" + str(self.__hash__)

        logging.debug("Writing to path %s", self.git_local_path)

        if not os.path.exists(self.git_local_path) or len(os.listdir(self.git_local_path)) == 0:
            self.clone_git_repo()
        else:
            if self.is_git_repo():
                self.update_git_repo()

        return git.Repo(self.git_local_path)

    # Check Integrity of Git Repo
    def check_integrity(self):
        return not self.repo.is_dirty()

    # Check if Remote is valid Git Repo
    def validate_remote(self, url):
        pass

    # Check if Local is valid Git Repo
    def is_git_repo(self):
        try:
            _ = git.Repo(self.git_local_path).git_dir
            return True
        except git.exc.InvalidGitRepositoryError:
            return False

    # Perform Git Clone from Remote
    def clone_git_repo(self):
        git.Repo.clone_from(self.git_remote_url, self.git_local_path)

    # Perform Git Reset --Hard from Remote
    def recover_git_repo(self):
        self.repo.git.reset('--hard', 'origin/main')

    # Perform Git Pull from Remote
    def update_git_repo(self):
        self.repo.remotes[0].pull()
