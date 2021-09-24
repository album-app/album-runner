import os
import sys
import unittest
from pathlib import Path

from album_runner import AlbumRunner
from album_runner.api import download_if_not_exists, extract_tar, download_solution_repository, chdir_repository, \
    add_dir_to_path, in_target_environment
from tests.test_unit_common import TestUnitCommon


class TestAPI(TestUnitCommon):

    def test_download_if_not_exists(self):
        self.push_test_solution()

        url = "https://gitlab.com/album-app/album-runner/-/raw/main/.gitlab-ci.yml?inline=false"
        file_name = Path(self.tmp_dir.name).joinpath("myDownload")
        r = download_if_not_exists(url, file_name)

        self.assertTrue(Path(r).exists())
        self.assertTrue(Path(r).stat().st_size > 0)

    def test_extract_tar(self):
        zip = self.get_resource("test_tar.tar.xz")

        extract_tar(zip, self.tmp_dir.name)

        self.assertTrue(Path(self.tmp_dir.name).joinpath("myfile").exists())
        self.assertTrue(Path(self.tmp_dir.name).joinpath("myfile").stat().st_size > 0)

    def test_download_solution_repository(self):
        solution = AlbumRunner(self.get_solution_dict())
        solution.git_repo = "https://gitlab.com/album-app/album-runner.git"

        self.push_test_solution(solution)

        d = download_solution_repository()

        expected = Path(self.tmp_dir.name).joinpath("tsn")

        self.assertEqual(str(expected), d)
        self.assertTrue(expected.joinpath("album_runner").exists())

    @unittest.skip("Needs to be implemented!")
    def test_install_package(self):
        # ToDo: implement
        pass

    def test_chdir_repository(self):
        Path(self.tmp_dir.name).joinpath(".git").touch()
        self.assertNotEqual(os.getcwd(), self.tmp_dir.name)

        chdir_repository(self.tmp_dir.name)
        self.assertEqual(os.getcwd(), self.tmp_dir.name)

    def test_chdir_repository_no_git(self):
        try:
            cur_wd = os.getcwd()
        except FileNotFoundError:
            cur_wd = None

        self.assertNotEqual(cur_wd, self.tmp_dir.name)

        with self.assertRaises(FileNotFoundError):
            chdir_repository(self.tmp_dir.name)

    def test_add_dir_to_path(self):
        self.assertNotIn(self.tmp_dir.name, sys.path)

        add_dir_to_path(self.tmp_dir.name)

        self.assertIn(self.tmp_dir.name, sys.path)

    def test_in_target_environment(self):
        solution = AlbumRunner(self.get_solution_dict())
        solution.environment_path = sys.executable

        self.push_test_solution(solution)

        self.assertTrue(in_target_environment())

    def test_in_target_environment_wrong_env(self):
        solution = AlbumRunner(self.get_solution_dict())
        solution.environment_path = "fake_env_path"

        self.push_test_solution(solution)

        self.assertFalse(in_target_environment())

    @unittest.skip("Needs to be implemented!")
    def test_run_as_executable(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test_get_args(self):
        # ToDo: implement
        pass


if __name__ == '__main__':
    unittest.main()
