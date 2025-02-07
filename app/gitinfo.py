import git


class GitInfo:
    def __init__(self, path='.'):
        try:
            # Lade das Git-Repository
            self.repo = git.Repo(path, search_parent_directories=True)

            # Holen der Informationen
            self.description = self.repo.git.describe(tags=True, always=True)
            self.commit = self.repo.head.commit.hexsha[:7]  # Abkürzung des Commit-Hashes
            self.branch = self.repo.active_branch.name if self.repo.active_branch else "Detached HEAD"
            self.uncommitted_changes = self.repo.is_dirty()  # Überprüfen, ob es uncommitted changes gibt
        except git.exc.InvalidGitRepositoryError:
            raise ValueError("Not a valid Git repository.")
