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
module: azure_rm_registeredprefix
version_added: '2.9'
short_description: Manage Azure RegisteredPrefix instance.
description:
  - 'Create, update and delete instance of Azure RegisteredPrefix.'
options:
  resource_group_name:
    description:
      - The name of the resource group.
    required: true
    type: str
  peering_name:
    description:
      - The name of the peering.
    required: true
    type: str
  registered_prefix_name:
    description:
      - The name of the registered prefix.
    required: true
    type: str
  prefix:
    description:
      - The customer's prefix from which traffic originates.
    type: str
  state:
    description:
      - Assert the state of the RegisteredPrefix.
      - >-
        Use C(present) to create or update an RegisteredPrefix and C(absent) to
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
    - name: Create or update a registered prefix for the peering
      azure_rm_registeredprefix: 
        peering_name: peeringName
        registered_prefix_name: registeredPrefixName
        resource_group_name: rgName
        

    - name: Deletes a registered prefix associated with the peering
      azure_rm_registeredprefix: 
        peering_name: peeringName
        registered_prefix_name: registeredPrefixName
        resource_group_name: rgName
        

'''

RETURN = '''
name:
  description:
    - The name of the resource.
  returned: always
  type: str
  sample: null
id:
  description:
    - The ID of the resource.
  returned: always
  type: str
  sample: null
type:
  description:
    - The type of the resource.
  returned: always
  type: str
  sample: null
prefix:
  description:
    - The customer's prefix from which traffic originates.
  returned: always
  type: str
  sample: null
prefix_validation_state:
  description:
    - The prefix validation state.
  returned: always
  type: str
  sample: null
peering_service_prefix_key:
  description:
    - The peering service prefix key that is to be shared with the customer.
  returned: always
  type: str
  sample: null
error_message:
  description:
    - 'The error message associated with the validation state, if any.'
  returned: always
  type: str
  sample: null
provisioning_state:
  description:
    - The provisioning state of the resource.
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
    from azure.mgmt.peering import PeeringManagementClient
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMRegisteredPrefix(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            peering_name=dict(
                type='str',
                required=True
            ),
            registered_prefix_name=dict(
                type='str',
                required=True
            ),
            prefix=dict(
                type='str',
                disposition='/prefix'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.peering_name = None
        self.registered_prefix_name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRegisteredPrefix, self).__init__(derived_arg_spec=self.module_arg_spec,
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

        self.mgmt_client = self.get_mgmt_svc_client(PeeringManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-04-01')

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
            response = self.mgmt_client.registered_prefixes.create_or_update(resource_group_name=self.resource_group_name,
                                                                             peering_name=self.peering_name,
                                                                             registered_prefix_name=self.registered_prefix_name,
                                                                             registered_prefix=self.body)
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the RegisteredPrefix instance.')
            self.fail('Error creating the RegisteredPrefix instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.registered_prefixes.delete(resource_group_name=self.resource_group_name,
                                                                   peering_name=self.peering_name,
                                                                   registered_prefix_name=self.registered_prefix_name)
        except CloudError as e:
            self.log('Error attempting to delete the RegisteredPrefix instance.')
            self.fail('Error deleting the RegisteredPrefix instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.registered_prefixes.get(resource_group_name=self.resource_group_name,
                                                                peering_name=self.peering_name,
                                                                registered_prefix_name=self.registered_prefix_name)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMRegisteredPrefix()


if __name__ == '__main__':
    main()
