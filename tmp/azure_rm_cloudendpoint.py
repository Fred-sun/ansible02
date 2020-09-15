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
module: azure_rm_cloudendpoint
version_added: '2.9'
short_description: Manage Azure CloudEndpoint instance.
description:
  - 'Create, update and delete instance of Azure CloudEndpoint.'
options:
  resource_group_name:
    description:
      - The name of the resource group. The name is case insensitive.
    required: true
    type: str
  storage_sync_service_name:
    description:
      - Name of Storage Sync Service resource.
    required: true
    type: str
  sync_group_name:
    description:
      - Name of Sync Group resource.
    required: true
    type: str
  cloud_endpoint_name:
    description:
      - Name of Cloud Endpoint object.
    required: true
    type: str
  storage_account_resource_id:
    description:
      - Storage Account Resource Id
    type: str
  azure_file_share_name:
    description:
      - Azure file share name
    type: str
  storage_account_tenant_id:
    description:
      - Storage Account Tenant Id
    type: str
  friendly_name:
    description:
      - Friendly Name
    type: str
  state:
    description:
      - Assert the state of the CloudEndpoint.
      - >-
        Use C(present) to create or update an CloudEndpoint and C(absent) to
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
    - name: CloudEndpoints_Create
      azure_rm_cloudendpoint: 
        cloud_endpoint_name: SampleCloudEndpoint_1
        resource_group_name: SampleResourceGroup_1
        storage_sync_service_name: SampleStorageSyncService_1
        sync_group_name: SampleSyncGroup_1
        properties:
          azure_file_share_name: cvcloud-afscv-0719-058-a94a1354-a1fd-4e9a-9a50-919fad8c4ba4
          friendly_name: ankushbsubscriptionmgmtmab
          storage_account_resource_id: >-
            /subscriptions/744f4d70-6d17-4921-8970-a765d14f763f/resourceGroups/tminienv59svc/providers/Microsoft.Storage/storageAccounts/tminienv59storage
          storage_account_tenant_id: '"72f988bf-86f1-41af-91ab-2d7cd011db47"'
        

    - name: CloudEndpoints_Delete
      azure_rm_cloudendpoint: 
        cloud_endpoint_name: SampleCloudEndpoint_1
        resource_group_name: SampleResourceGroup_1
        storage_sync_service_name: SampleStorageSyncService_1
        sync_group_name: SampleSyncGroup_1
        

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
storage_account_resource_id:
  description:
    - Storage Account Resource Id
  returned: always
  type: str
  sample: null
azure_file_share_name:
  description:
    - Azure file share name
  returned: always
  type: str
  sample: null
storage_account_tenant_id:
  description:
    - Storage Account Tenant Id
  returned: always
  type: str
  sample: null
partnership_id:
  description:
    - Partnership Id
  returned: always
  type: str
  sample: null
friendly_name:
  description:
    - Friendly Name
  returned: always
  type: str
  sample: null
backup_enabled:
  description:
    - Backup Enabled
  returned: always
  type: str
  sample: null
provisioning_state:
  description:
    - CloudEndpoint Provisioning State
  returned: always
  type: str
  sample: null
last_workflow_id:
  description:
    - CloudEndpoint lastWorkflowId
  returned: always
  type: str
  sample: null
last_operation_name:
  description:
    - Resource Last Operation Name
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


class AzureRMCloudEndpoint(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            storage_sync_service_name=dict(
                type='str',
                required=True
            ),
            sync_group_name=dict(
                type='str',
                required=True
            ),
            cloud_endpoint_name=dict(
                type='str',
                required=True
            ),
            storage_account_resource_id=dict(
                type='str',
                disposition='/storage_account_resource_id'
            ),
            azure_file_share_name=dict(
                type='str',
                disposition='/azure_file_share_name'
            ),
            storage_account_tenant_id=dict(
                type='str',
                disposition='/storage_account_tenant_id'
            ),
            friendly_name=dict(
                type='str',
                disposition='/friendly_name'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.storage_sync_service_name = None
        self.sync_group_name = None
        self.cloud_endpoint_name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMCloudEndpoint, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                response = self.mgmt_client.cloud_endpoints.create(resource_group_name=self.resource_group_name,
                                                                   storage_sync_service_name=self.storage_sync_service_name,
                                                                   sync_group_name=self.sync_group_name,
                                                                   cloud_endpoint_name=self.cloud_endpoint_name,
                                                                   parameters=self.body)
            else:
                response = self.mgmt_client.cloud_endpoints.update()
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the CloudEndpoint instance.')
            self.fail('Error creating the CloudEndpoint instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.cloud_endpoints.delete(resource_group_name=self.resource_group_name,
                                                               storage_sync_service_name=self.storage_sync_service_name,
                                                               sync_group_name=self.sync_group_name,
                                                               cloud_endpoint_name=self.cloud_endpoint_name)
        except CloudError as e:
            self.log('Error attempting to delete the CloudEndpoint instance.')
            self.fail('Error deleting the CloudEndpoint instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.cloud_endpoints.get(resource_group_name=self.resource_group_name,
                                                            storage_sync_service_name=self.storage_sync_service_name,
                                                            sync_group_name=self.sync_group_name,
                                                            cloud_endpoint_name=self.cloud_endpoint_name)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMCloudEndpoint()


if __name__ == '__main__':
    main()
