import os
import sys
import re

import jenkins

from config.config import *

from update_xml import *


class GenerateJob:
    class __GenerateJob:
        def __init__(self):
            self.server = jenkins.Jenkins(server_url, username=username, password=token)

    __jenkins = None

    def __init__(self, path_to_tests):
        if not GenerateJob.__jenkins:
            GenerateJob.__jenkins = GenerateJob.__GenerateJob().server
        self._path = self.validate_path(path_to_tests)

        self.build_job = raw_input("Build jobs (MY venture)? [y/N]: ") or 'n'
        self.delete_old_jobs = raw_input("Delete old jobs? [y/N]: ") or 'n'
        self.create_view = raw_input("Create view? [y/N]: ") or 'n'

        self.service_name = os.path.basename(os.path.normpath(self._path))

    def __copy__(self):
        return self.__jenkins

    def get_connection(self):
        return self.__jenkins

    def validate_path(self, path_to_tests):
        if not os.path.isdir(path_to_tests):
            raise 'Directory does not exist!'
        return path_to_tests

    def generate_jobs(self):
        handlers_files = os.listdir(self._path)

        for handler in handlers_files:
            match = re.search(r'^test.*', handler)
            if match:
                job_name = match.group()

                if self.delete_old_jobs.lower() == 'y' and self.__jenkins.job_exists(job_name):
                    self.__jenkins.delete_job(job_name)
                if not self.__jenkins.job_exists(job_name):
                    self.__jenkins.create_job(job_name, update_job_xml(self.service_name, job_name))

                self.build_task(job_name)

                update_job_name_view_xml(job_name)

        self.create_or_update_view(self.service_name)

    def build_task(self, job_name):
        if self.build_job.lower() == 'y':
            self.__jenkins.build_job(job_name, parameters={"VENTURE": "MY"}, token=token)

    def create_or_update_view(self, service_name):
        xml_body = update_service_name_view_xml(self.service_name)
        if self.create_view.lower() == 'y':
            self.__jenkins.create_view(service_name.title(), xml_body)
        else:
            self.__jenkins.reconfig_view(service_name.title(), xml_body)

if __name__ == '__main__':

    path = sys.argv[1]
    server = GenerateJob(path)

    # comment this --------
    if 'delete' in sys.argv:
        delete_all_confirm = \
            raw_input("Do you really want to delete all jobs? This operation can't undo [yes/No]: ") or 'no'
        if delete_all_confirm.lower() == 'yes':
            for job in server.get_connection().get_jobs():
                server.get_connection().delete_job(job['name'])
            exit('Jobs deleted. Exit.')
    # ---------------------

    server.generate_jobs()
