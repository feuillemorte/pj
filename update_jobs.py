import sys
import os
import re

import jenkins

from config.config import *

from update_xml import *


class UpdateJob:
    class __UpdateJob:
        def __init__(self):
            self.server = jenkins.Jenkins(server_url, username=username, password=token)

    __jenkins = None

    def __init__(self, path_to_tests):
        if not UpdateJob.__jenkins:
            UpdateJob.__jenkins = UpdateJob.__UpdateJob().server
        self._path = self.validate_path(path_to_tests)

        self.build_job = raw_input("Build jobs (MY venture)? [y/N]: ") or 'n'

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

    def update_jobs(self):
        handlers_files = os.listdir(self._path)

        for handler in handlers_files:
            match = re.search(r'^test.*', handler)
            if match:
                job_name = match.group()

                if self.__jenkins.job_exists(job_name):
                    self.__jenkins.reconfig_job(job_name, update_job_xml(self.service_name, job_name))

                self.build_task(job_name)

    def build_task(self, job_name):
        if self.build_job.lower() == 'y':
            self.__jenkins.build_job(job_name, parameters={"VENTURE": "MY"}, token=token)


if __name__ == '__main__':
    path = sys.argv[1]
    server = UpdateJob(path)

    server.update_jobs()
