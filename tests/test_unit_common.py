import os
import tempfile
import unittest
from pathlib import Path

from album.runner import Solution, push_active_solution


class TestUnitCommon(unittest.TestCase):
    """Base class for all Unittest"""

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.closed_tmp_file = tempfile.NamedTemporaryFile(delete=False)
        self.closed_tmp_file.close()

        self.wd = os.getcwd()

    def tearDown(self) -> None:
        Path(self.closed_tmp_file.name).unlink()
        try:
            self.tmp_dir.cleanup()
        except PermissionError:
            print("Cannot clanup! Permission Error!")
            pass

        os.chdir(self.wd)

    @staticmethod
    def get_solution_dict():
        return {
            'group': "tsg",
            'name': "tsn",
            'description': "d1",
            'version': "tsv",
            'format_version': "f1",
            'album_api_version': "t1",
            'album_version': "mhv1",
            'license': "l1",
            'git_repo': "g1",
            'authors': ["a1", "a2"],
            'cite': [{"text": "c1"}],
            'tags': ["t1"],
            'documentation': "do1",
            'covers': [{"source": "co1", "description": ""}],
            'args': [{"name": "a1", "type": "string", "description": ""}],
            'title': "t1",
            'timestamp': "",
        }

    def push_test_solution(self, solution=None):
        if not solution:
            solution = Solution(self.get_solution_dict())
        solution.installation.user_cache_path = Path(self.tmp_dir.name)
        push_active_solution(solution)

    @staticmethod
    def get_resource(r_name):
        current_path = Path(os.path.dirname(os.path.realpath(__file__)))
        path = current_path.joinpath("resources", r_name)

        return path
