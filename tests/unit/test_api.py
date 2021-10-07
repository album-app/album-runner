import sys
import unittest
from pathlib import Path

from album.runner import AlbumRunner
from album.runner.api import download_if_not_exists, extract_tar, in_target_environment

from tests.test_unit_common import TestUnitCommon


class TestAPI(TestUnitCommon):

    @unittest.skip("Needs to be implemented!")
    def test_get_environment_name(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test_get_environment_path(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test_get_data_path(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test_get_package_path(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test_get_app_path(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test_get_cache_path(self):
        # ToDo: implement
        pass

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
    def test_get_args(self):
        # ToDo: implement
        pass


if __name__ == '__main__':
    unittest.main()
