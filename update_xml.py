import os
import re

import xml.etree.ElementTree

from config.config import *

job_xml_root = xml.etree.ElementTree.parse(
    '{}/xml/job.xml'.format(os.path.dirname(os.path.realpath(__file__)))).getroot()

view_xml_root = xml.etree.ElementTree.parse(
        '{}/xml/view.xml'.format(os.path.dirname(os.path.realpath(__file__)))).getroot()


def update_job_xml(service_name, job_name):

    for git_params in job_xml_root.iter('hudson.plugins.git.BranchSpec'):

        git_params.find('name').text = jenkins_git_branch

        for git_params in job_xml_root.iter('hudson.plugins.git.UserRemoteConfig'):
            git_params.find('url').text = jenkins_git_url
            git_params.find('credentialsId').text = jenkins_git_credentials_id

        for shell_params in job_xml_root.iter('hudson.tasks.Shell'):
            shell_params.find('command').text = re.sub('%service_name%', service_name,
                                                       shell_params.find('command').text)

        for job_params in job_xml_root.iter('hudson.plugins.parameterizedtrigger.PredefinedBuildParameters'):
            job_params.find('properties').text = re.sub('%service_name%', service_name,
                                                        job_params.find('properties').text)
            job_params.find('properties').text = re.sub('%service_job_name%', job_name,
                                                        job_params.find('properties').text)

    return xml.etree.ElementTree.tostring(job_xml_root)


def update_service_name_view_xml(service_name):
    view_xml_root.find('name').text = service_name.title()

    return xml.etree.ElementTree.tostring(view_xml_root)


def update_job_name_view_xml(job_name):
    for view_params in view_xml_root.findall('jobNames'):
        xml.etree.ElementTree.SubElement(view_params, "string")
        view_params.find('string[last()]').text = job_name
