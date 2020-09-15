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
module: azure_rm_configurationassignment
version_added: '2.9'
short_description: Manage Azure ConfigurationAssignment instance.
description:
  - 'Create, update and delete instance of Azure ConfigurationAssignment.'
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
  configuration_assignment_name:
    description:
      - Configuration assignment name
      - Unique configuration assignment name
    required: true
    type: str
  location:
    description:
      - Location of the resource
    type: str
  maintenance_configuration_id:
    description:
      - The maintenance configuration Id
    type: str
  resource_id:
    description:
      - The unique resourceId
    type: str
  state:
    description:
      - Assert the state of the ConfigurationAssignment.
      - >-
        Use C(present) to create or update an ConfigurationAssignment and
        C(absent) to delete it.
    default: present
    choices:
      - absent
      - present
extends_documentation_fragment:
  - azure
author:
  - GuopengLin (@t-glin)

'''

EXAMPLES = '''
    - name: ConfigurationAssignments_CreateOrUpdate
      azure_rm_configurationassignment: 
        configuration_assignment_name: workervmConfiguration
        provider_name: Microsoft.Compute
        resource_group_name: examplerg
        resource_name: smdtest1
        resource_type: virtualMachineScaleSets
        

    - name: ConfigurationAssignments_Delete
      azure_rm_configurationassignment: 
        configuration_assignment_name: workervmConfiguration
        provider_name: Microsoft.Compute
        resource_group_name: examplerg
        resource_name: smdtest1
        resource_type: virtualMachineScaleSets
        

'''

RETURN = '''
id:
  description:
    - Fully qualified identifier of the resource
  returned: always
  type: str
  sample: null
name:
  description:
    - Name of the resource
  returned: always
  type: str
  sample: null
type:
  description:
    - Type of the resource
  returned: always
  type: str
  sample: null
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
import re
from ansible.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from copy import deepcopy
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.maintenance import MaintenanceClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMConfigurationAssignment(AzureRMModuleBaseExt):
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
            resource_type=dict(
                type='str',
                required=True
            ),
            resource_name=dict(
                type='str',
                required=True
            ),
            configuration_assignment_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                disposition='/location'
            ),
            maintenance_configuration_id=dict(
                type='str',
                disposition='/maintenance_configuration_id'
            ),
            resource_id=dict(
                type='str',
                disposition='/resource_id'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.provider_name = None
        self.resource_type = None
        self.resource_name = None
        self.configuration_assignment_name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConfigurationAssignment, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                             supports_check_mode=True,
                                                             supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_parameters(self.module_arg_spec, self.body, 0)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(MaintenanceClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-07-01-preview')

        old_response = self.get_resource()

        if not old_response:
            if self.state == 'present':
                self.to_do = Actions.Create
        else:
            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                modifiers = {}
                self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                self.results['modifiers'] = modifiers
                self.results['compare'] = []
                if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_resource()
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_resource()
        else:
            self.results['changed'] = False
            response = old_response

        return self.results

    def create_update_resource(self):
        try:
            response = self.mgmt_client.configuration_assignments.create_or_update(resource_group_name=self.resource_group_name,
                                                                                   provider_name=self.provider_name,
                                                                                   resource_type=self.resource_type,
                                                                                   resource_name=self.resource_name,
                                                                                   configuration_assignment_name=self.configuration_assignment_name,
                                                                                   configuration_assignment=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the ConfigurationAssignment instance.')
            self.fail('Error creating the ConfigurationAssignment instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.configuration_assignments.delete(resource_group_name=self.resource_group_name,
                                                                         provider_name=self.provider_name,
                                                                         resource_type=self.resource_type,
                                                                         resource_name=self.resource_name,
                                                                         configuration_assignment_name=self.configuration_assignment_name)
        except CloudError as e:
            self.log('Error attempting to delete the ConfigurationAssignment instance.')
            self.fail('Error deleting the ConfigurationAssignment instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.configuration_assignments.get()
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMConfigurationAssignment()


if __name__ == '__main__':
    main()
