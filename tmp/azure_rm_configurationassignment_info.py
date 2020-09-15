#!/usr/bin/python
#
# Copyright (c) 2020 GuopengLin, (@t-glin)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_configurationassignment_info
version_added: '2.9'
short_description: Get ConfigurationAssignment info.
description:
  - Get info of ConfigurationAssignment.
options:
  resource_group_name:
    description:
      - Resource group name
    required: true
    type: str
  provider_name:
    description:
      - Resource provider name
    required: true
    type: str
  resource_parent_type:
    description:
      - Resource parent type
    type: str
  resource_parent_name:
    description:
      - Resource parent identifier
    type: str
  resource_type:
    description:
      - Resource type
    required: true
    type: str
  resource_name:
    description:
      - Resource identifier
    required: true
    type: str
extends_documentation_fragment:
  - azure
author:
  - GuopengLin (@t-glin)

'''

EXAMPLES = '''
    - name: ConfigurationAssignments_ListParent
      azure_rm_configurationassignment_info: 
        provider_name: Microsoft.Compute
        resource_group_name: examplerg
        resource_name: smdtestvm1
        resource_parent_name: smdtest1
        resource_parent_type: virtualMachineScaleSets
        resource_type: virtualMachines
        

    - name: ConfigurationAssignments_List
      azure_rm_configurationassignment_info: 
        provider_name: Microsoft.Compute
        resource_group_name: examplerg
        resource_name: smdtest1
        resource_type: virtualMachineScaleSets
        

'''

RETURN = '''
configuration_assignments:
  description: >-
    A list of dict results where the key is the name of the
    ConfigurationAssignment and the values are the facts for that
    ConfigurationAssignment.
  returned: always
  type: complex
  contains:
    value:
      description:
        - The list of configuration Assignments
      returned: always
      type: list
      sample: null
      contains:
        location:
          description:
            - Location of the resource
          returned: always
          type: str
          sample: null
        maintenance_configuration_id:
          description:
            - The maintenance configuration Id
          returned: always
          type: str
          sample: null
        resource_id:
          description:
            - The unique resourceId
          returned: always
          type: str
          sample: null

'''

import time
import json
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from copy import deepcopy
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.maintenance import MaintenanceClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMConfigurationAssignmentInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            provider_name=dict(
                type='str',
                required=True
            ),
            resource_parent_type=dict(
                type='str'
            ),
            resource_parent_name=dict(
                type='str'
            ),
            resource_type=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            )
        )

        self.resource_group_name = None
        self.provider_name = None
        self.resource_parent_type = None
        self.resource_parent_name = None
        self.resource_type = None
        self.resource_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2020-07-01-preview'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMConfigurationAssignmentInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(MaintenanceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-07-01-preview')

        if (self.resource_group_name is not None and
            self.provider_name is not None and
            self.resource_parent_type is not None and
            self.resource_parent_name is not None and
            self.resource_type is not None and
            self.resource_name is not None):
            self.results['configuration_assignments'] = self.format_item(self.listparent())
        elif (self.resource_group_name is not None and
              self.provider_name is not None and
              self.resource_type is not None and
              self.resource_name is not None):
            self.results['configuration_assignments'] = self.format_item(self.list())
        return self.results

    def listparent(self):
        response = None

        try:
            response = self.mgmt_client.configuration_assignments.list_parent(resource_group_name=self.resource_group_name,
                                                                              provider_name=self.provider_name,
                                                                              resource_parent_type=self.resource_parent_type,
                                                                              resource_parent_name=self.resource_parent_name,
                                                                              resource_type=self.resource_type,
                                                                              resource_name=self.resource_name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def list(self):
        response = None

        try:
            response = self.mgmt_client.configuration_assignments.list(resource_group_name=self.resource_group_name,
                                                                       provider_name=self.provider_name,
                                                                       resource_type=self.resource_type,
                                                                       resource_name=self.resource_name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def format_item(self, item):
        if hasattr(item, 'as_dict'):
            return [item.as_dict()]
        else:
            result = []
            items = list(item)
            for tmp in items:
               result.append(tmp.as_dict())
            return result


def main():
    AzureRMConfigurationAssignmentInfo()


if __name__ == '__main__':
    main()
