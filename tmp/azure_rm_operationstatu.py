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
module: azure_rm_operationstatu
version_added: '2.9'
short_description: Manage Azure OperationStatu instance.
description:
  - 'Create, update and delete instance of Azure OperationStatu.'
options:
  resource_group_name:
    description:
      - The name of the resource group. The name is case insensitive.
    required: true
    type: str
  location_name:
    description:
      - The desired region to obtain information from.
    required: true
    type: str
  workflow_id:
    description:
      - workflow Id
    required: true
    type: str
  operation_id:
    description:
      - operation Id
    required: true
    type: str
  state:
    description:
      - Assert the state of the OperationStatu.
      - >-
        Use C(present) to create or update an OperationStatu and C(absent) to
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
'''

RETURN = '''
name:
  description:
    - Operation Id
  returned: always
  type: str
  sample: null
status:
  description:
    - Operation status
  returned: always
  type: str
  sample: null
start_time:
  description:
    - Start time of the operation
  returned: always
  type: str
  sample: null
end_time:
  description:
    - End time of the operation
  returned: always
  type: str
  sample: null
error:
  description:
    - Error details.
  returned: always
  type: dict
  sample: null
  contains:
    code:
      description:
        - Error code of the given entry.
      returned: always
      type: str
      sample: null
    message:
      description:
        - Error message of the given entry.
      returned: always
      type: str
      sample: null
    target:
      description:
        - Target of the given error entry.
      returned: always
      type: str
      sample: null
    details:
      description:
        - Error details of the given entry.
      returned: always
      type: dict
      sample: null
      contains:
        code:
          description:
            - Error code of the given entry.
          returned: always
          type: str
          sample: null
        message:
          description:
            - Error message of the given entry.
          returned: always
          type: str
          sample: null
        target:
          description:
            - Target of the given entry.
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
    from azure.mgmt.microsoft import Microsoft Storage Sync
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOperationStatu(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            location_name=dict(
                type='str',
                required=True
            ),
            workflow_id=dict(
                type='str',
                required=True
            ),
            operation_id=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.location_name = None
        self.workflow_id = None
        self.operation_id = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMOperationStatu, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        self.mgmt_client = self.get_mgmt_svc_client(Microsoft Storage Sync,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-03-01')

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
            if self.to_do == Actions.Create:
                response = self.mgmt_client.operation_status.create()
            else:
                response = self.mgmt_client.operation_status.update()
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the OperationStatu instance.')
            self.fail('Error creating the OperationStatu instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.operation_status.delete()
        except CloudError as e:
            self.log('Error attempting to delete the OperationStatu instance.')
            self.fail('Error deleting the OperationStatu instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.operation_status.get(resource_group_name=self.resource_group_name,
                                                             location_name=self.location_name,
                                                             workflow_id=self.workflow_id,
                                                             operation_id=self.operation_id)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMOperationStatu()


if __name__ == '__main__':
    main()
