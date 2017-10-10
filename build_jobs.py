import sys
import os
import re

import jenkins

from config.config import *

from update_xml import *


class BuildJob:
    class __BuildJob:
        def __init__(self):
            self.server = jenkins.Jenkins(server_url, username=username, password=token)

    __jenkins = None

    def __init__(self, path_to_tests):
        if not BuildJob.__jenkins:
            BuildJob.__jenkins = BuildJob.__BuildJob().server
        self._path = self.validate_path(path_to_tests)

        self.service_name = os.path.basename(os.path.normpath(self._path))
        self.create_view = raw_input("Enter view name? [{}]: ".format(self.service_name.title())) \
                           or self.service_name.title()

    def __copy__(self):
        return self.__jenkins

    def get_connection(self):
        return self.__jenkins

    def validate_path(self, path_to_tests):
        if not os.path.isdir(path_to_tests):
            raise 'Directory does not exist!'

        return path_to_tests

    def build_jobs(self):
        handlers_files = os.listdir(self._path)

        for handler in handlers_files:
            match = re.search(r'^test.*', handler)
            if match:
                job_name = match.group()

                self.build_task(job_name)

    def build_task(self, job_name):
        self.__jenkins.build_job(job_name, parameters={"VENTURE": "<paste your venture here>"}, token=token)


if __name__ == '__main__':
    path = sys.argv[1]
    server = BuildJob(path)

    server.build_jobs()
