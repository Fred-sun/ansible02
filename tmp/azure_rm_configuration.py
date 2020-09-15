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
module: azure_rm_configuration
version_added: '2.9'
short_description: Manage Azure Configuration instance.
description:
  - 'Create, update and delete instance of Azure Configuration.'
options:
  resource_group_name:
    description:
      - The name of the resource group. The name is case insensitive.
    required: true
    type: str
  server_name:
    description:
      - The name of the server.
    required: true
    type: str
  configuration_name:
    description:
      - The name of the server configuration.
    required: true
    type: str
  value:
    description:
      - Value of the configuration.
    type: str
  source:
    description:
      - Source of the configuration.
    type: str
  state:
    description:
      - Assert the state of the Configuration.
      - >-
        Use C(present) to create or update an Configuration and C(absent) to
        delete it.
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
    - name: ConfigurationCreateOrUpdate
      azure_rm_configuration: 
        configuration_name: array_nulls
        resource_group_name: TestGroup
        server_name: testserver
        properties:
          source: user-override
          value: 'off'
        

'''

RETURN = '''
id:
  description:
    - >-
      Fully qualified resource Id for the resource. Ex -
      /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
  returned: always
  type: str
  sample: null
name:
  description:
    - The name of the resource
  returned: always
  type: str
  sample: null
type:
  description:
    - >-
      The type of the resource. Ex- Microsoft.Compute/virtualMachines or
      Microsoft.Storage/storageAccounts.
  returned: always
  type: str
  sample: null
value:
  description:
    - Value of the configuration.
  returned: always
  type: str
  sample: null
description:
  description:
    - Description of the configuration.
  returned: always
  type: str
  sample: null
default_value:
  description:
    - Default value of the configuration.
  returned: always
  type: str
  sample: null
data_type:
  description:
    - Data type of the configuration.
  returned: always
  type: str
  sample: null
allowed_values:
  description:
    - Allowed values of the configuration.
  returned: always
  type: str
  sample: null
source:
  description:
    - Source of the configuration.
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
    from azure.mgmt.postgre import PostgreSQLManagementClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMConfiguration(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            configuration_name=dict(
                type='str',
                required=True
            ),
            value=dict(
                type='str',
                disposition='/value'
            ),
            source=dict(
                type='str',
                disposition='/source'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.server_name = None
        self.configuration_name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMConfiguration, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        self.mgmt_client = self.get_mgmt_svc_client(PostgreSQLManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2017-12-01')

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
            response = self.mgmt_client.configurations.create_or_update(resource_group_name=self.resource_group_name,
                                                                        server_name=self.server_name,
                                                                        configuration_name=self.configuration_name,
                                                                        parameters=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the Configuration instance.')
            self.fail('Error creating the Configuration instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.configurations.delete()
        except CloudError as e:
            self.log('Error attempting to delete the Configuration instance.')
            self.fail('Error deleting the Configuration instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.configurations.get(resource_group_name=self.resource_group_name,
                                                           server_name=self.server_name,
                                                           configuration_name=self.configuration_name)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMConfiguration()


if __name__ == '__main__':
    main()
