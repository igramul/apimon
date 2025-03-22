import os
import json
import subprocess


class GitInfo:

    DEFAULT_FILE = 'gitinfo'

    def __init__(self, path='.'):

        self.version = None
        self.commit = None
        self.branch = None
        self.uncommitted_changes = None
        self.description = None

        # check whether current directory is a git repository
        try:
            output = subprocess.check_output('git rev-parse --is-inside-work-tree',
                                             stderr=subprocess.STDOUT, shell=True)
            if output.decode().strip() == 'true':
                self.is_git_repo = True
            else:
                self.is_git_repo = False
        except subprocess.CalledProcessError:
            self.is_git_repo = False

        if self.is_git_repo:
            self.version = subprocess.check_output('git describe --tags --always', shell=True).decode().rstrip()
            self.commit = subprocess.check_output('git log -1 --pretty="%h"', shell=True).decode().rstrip()
            self.branch = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).decode().rstrip()
            self.uncommitted_changes =subprocess.check_output('git status --porcelain', shell=True).decode().rstrip()
            self.description = '%s (commit %s)' % (self.version, self.commit)
            if self.uncommitted_changes:
                self.description += ' with uncommitted changes'

    @classmethod
    def from_path(cls, path):
        """ Alternative constructor to get git information of path """
        cwd = os.getcwd()
        os.chdir(path)
        try:
            self = cls()
        finally:
            os.chdir(cwd)
        return self

    @classmethod
    def from_json(cls, json_string: str):
        self = cls()
        for key, value in json.loads(json_string).items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    @classmethod
    def load_json(cls, file: str=None):
        if file is None:
            file = cls.DEFAULT_FILE + '.json'
        with open(file, 'r') as fh:
            return cls.from_json(fh.read())

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    def save_json(self, file: str=None):
        if file is None:
            file = self.DEFAULT_FILE + '.json'
        with open(file, 'w') as fh:
            fh.write(self.to_json())

    def __str__(self):
        return self.description