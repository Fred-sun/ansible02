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
module: azure_rm_managedinstancelongtermretentionpolicy
version_added: '2.9'
short_description: Manage Azure ManagedInstanceLongTermRetentionPolicy instance.
description:
  - >-
    Create, update and delete instance of Azure
    ManagedInstanceLongTermRetentionPolicy.
options:
  resource_group_name:
    description:
      - >-
        The name of the resource group that contains the resource. You can
        obtain this value from the Azure Resource Manager API or the portal.
    required: true
    type: str
  managed_instance_name:
    description:
      - The name of the managed instance.
    required: true
    type: str
  database_name:
    description:
      - The name of the database.
    required: true
    type: str
  policy_name:
    description:
      - The policy name. Should always be Default.
    required: true
    type: str
    choices:
      - default
  weekly_retention:
    description:
      - The weekly retention policy for an LTR backup in an ISO 8601 format.
    type: str
  monthly_retention:
    description:
      - The monthly retention policy for an LTR backup in an ISO 8601 format.
    type: str
  yearly_retention:
    description:
      - The yearly retention policy for an LTR backup in an ISO 8601 format.
    type: str
  week_of_year:
    description:
      - The week of year to take the yearly backup in an ISO 8601 format.
    type: integer
  state:
    description:
      - Assert the state of the ManagedInstanceLongTermRetentionPolicy.
      - >-
        Use C(present) to create or update an
        ManagedInstanceLongTermRetentionPolicy and C(absent) to delete it.
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
    - name: Create or update the LTR policy for the managed database.
      azure_rm_managedinstancelongtermretentionpolicy: 
        database_name: testDatabase
        managed_instance_name: testInstance
        policy_name: default
        resource_group_name: testResourceGroup
        properties:
          monthly_retention: P1Y
          week_of_year: 5
          weekly_retention: P1M
          yearly_retention: P5Y
        

'''

RETURN = '''
id:
  description:
    - Resource ID.
  returned: always
  type: str
  sample: null
name:
  description:
    - Resource name.
  returned: always
  type: str
  sample: null
type:
  description:
    - Resource type.
  returned: always
  type: str
  sample: null
weekly_retention:
  description:
    - The weekly retention policy for an LTR backup in an ISO 8601 format.
  returned: always
  type: str
  sample: null
monthly_retention:
  description:
    - The monthly retention policy for an LTR backup in an ISO 8601 format.
  returned: always
  type: str
  sample: null
yearly_retention:
  description:
    - The yearly retention policy for an LTR backup in an ISO 8601 format.
  returned: always
  type: str
  sample: null
week_of_year:
  description:
    - The week of year to take the yearly backup in an ISO 8601 format.
  returned: always
  type: integer
  sample: null

'''

import time
import json
import re
from ansible.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from copy import deepcopy
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.sql import SqlManagementClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMManagedInstanceLongTermRetentionPolicy(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            managed_instance_name=dict(
                type='str',
                required=True
            ),
            database_name=dict(
                type='str',
                required=True
            ),
            policy_name=dict(
                type='str',
                choices=['default'],
                required=True
            ),
            weekly_retention=dict(
                type='str',
                disposition='/weekly_retention'
            ),
            monthly_retention=dict(
                type='str',
                disposition='/monthly_retention'
            ),
            yearly_retention=dict(
                type='str',
                disposition='/yearly_retention'
            ),
            week_of_year=dict(
                type='integer',
                disposition='/week_of_year'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.managed_instance_name = None
        self.database_name = None
        self.policy_name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMManagedInstanceLongTermRetentionPolicy, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2018-06-01-preview')

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
            response = self.mgmt_client.managed_instance_long_term_retention_policies.create_or_update(resource_group_name=self.resource_group_name,
                                                                                                       managed_instance_name=self.managed_instance_name,
                                                                                                       database_name=self.database_name,
                                                                                                       policy_name=self.policy_name,
                                                                                                       parameters=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the ManagedInstanceLongTermRetentionPolicy instance.')
            self.fail('Error creating the ManagedInstanceLongTermRetentionPolicy instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.managed_instance_long_term_retention_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the ManagedInstanceLongTermRetentionPolicy instance.')
            self.fail('Error deleting the ManagedInstanceLongTermRetentionPolicy instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.managed_instance_long_term_retention_policies.get(resource_group_name=self.resource_group_name,
                                                                                          managed_instance_name=self.managed_instance_name,
                                                                                          database_name=self.database_name,
                                                                                          policy_name=self.policy_name)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMManagedInstanceLongTermRetentionPolicy()


if __name__ == '__main__':
    main()
