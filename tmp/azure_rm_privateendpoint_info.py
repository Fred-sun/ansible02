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
module: azure_rm_privateendpoint_info
version_added: '2.9'
short_description: Get PrivateEndpoint info.
description:
  - Get info of PrivateEndpoint.
options:
  resource_group_name:
    description:
      - The name of the resource group. The name is case insensitive.
    required: true
    type: str
  cluster_name:
    description:
      - The name of the cluster.
    required: true
    type: str
  private_endpoint_name:
    description:
      - The name of the private endpoint.
    type: str
extends_documentation_fragment:
  - azure
author:
  - GuopengLin (@t-glin)

'''

EXAMPLES = '''
    - name: Get a private endpoint
      azure_rm_privateendpoint_info: 
        cluster_name: testcluster
        private_endpoint_name: testpe
        resource_group_name: sjrg
        

    - name: Get the private endpoints in a cluster
      azure_rm_privateendpoint_info: 
        cluster_name: testcluster
        resource_group_name: sjrg
        

'''

RETURN = '''
private_endpoints:
  description: >-
    A list of dict results where the key is the name of the PrivateEndpoint and
    the values are the facts for that PrivateEndpoint.
  returned: always
  type: complex
  contains:
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
    etag:
      description:
        - >-
          Unique opaque string (generally a GUID) that represents the metadata
          state of the resource (private endpoint) and changes whenever the
          resource is updated. Required on PUT (CreateOrUpdate) requests.
      returned: always
      type: str
      sample: null
    created_date:
      description:
        - The date when this private endpoint was created.
      returned: always
      type: str
      sample: null
    manual_private_link_service_connections:
      description:
        - >-
          A list of connections to the remote resource. Immutable after it is
          set.
      returned: always
      type: list
      sample: null
      contains:
        private_link_service_id:
          description:
            - >-
              The resource id of the private link service. Required on PUT
              (CreateOrUpdate) requests.
          returned: always
          type: str
          sample: null
        group_ids:
          description:
            - >-
              The ID(s) of the group(s) obtained from the remote resource that
              this private endpoint should connect to. Required on PUT
              (CreateOrUpdate) requests.
          returned: always
          type: list
          sample: null
        request_message:
          description:
            - >-
              A message passed to the owner of the remote resource with this
              connection request. Restricted to 140 chars.
          returned: always
          type: str
          sample: null
        private_link_service_connection_state:
          description:
            - >-
              A collection of read-only information about the state of the
              connection to the private remote resource.
          returned: always
          type: dict
          sample: null
          contains:
            status:
              description:
                - >-
                  Indicates whether the connection has been
                  Approved/Rejected/Removed by the owner of the remote
                  resource/service.
              returned: always
              type: str
              sample: null
            description:
              description:
                - The reason for approval/rejection of the connection.
              returned: always
              type: str
              sample: null
            actions_required:
              description:
                - >-
                  A message indicating if changes on the service provider
                  require any updates on the consumer.
              returned: always
              type: str
              sample: null
    value:
      description:
        - A list of private endpoints.
      returned: always
      type: list
      sample: null
      contains:
        etag:
          description:
            - >-
              Unique opaque string (generally a GUID) that represents the
              metadata state of the resource (private endpoint) and changes
              whenever the resource is updated. Required on PUT (CreateOrUpdate)
              requests.
          returned: always
          type: str
          sample: null
        created_date:
          description:
            - The date when this private endpoint was created.
          returned: always
          type: str
          sample: null
        manual_private_link_service_connections:
          description:
            - >-
              A list of connections to the remote resource. Immutable after it
              is set.
          returned: always
          type: list
          sample: null
          contains:
            private_link_service_id:
              description:
                - >-
                  The resource id of the private link service. Required on PUT
                  (CreateOrUpdate) requests.
              returned: always
              type: str
              sample: null
            group_ids:
              description:
                - >-
                  The ID(s) of the group(s) obtained from the remote resource
                  that this private endpoint should connect to. Required on PUT
                  (CreateOrUpdate) requests.
              returned: always
              type: list
              sample: null
            request_message:
              description:
                - >-
                  A message passed to the owner of the remote resource with this
                  connection request. Restricted to 140 chars.
              returned: always
              type: str
              sample: null
            private_link_service_connection_state:
              description:
                - >-
                  A collection of read-only information about the state of the
                  connection to the private remote resource.
              returned: always
              type: dict
              sample: null
              contains:
                status:
                  description:
                    - >-
                      Indicates whether the connection has been
                      Approved/Rejected/Removed by the owner of the remote
                      resource/service.
                  returned: always
                  type: str
                  sample: null
                description:
                  description:
                    - The reason for approval/rejection of the connection.
                  returned: always
                  type: str
                  sample: null
                actions_required:
                  description:
                    - >-
                      A message indicating if changes on the service provider
                      require any updates on the consumer.
                  returned: always
                  type: str
                  sample: null
    next_link:
      description:
        - The URL to fetch the next set of private endpoints.
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
    from azure.mgmt.stream import Stream Analytics Management Client
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPrivateEndpointInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            cluster_name=dict(
                type='str',
                required=True
            ),
            private_endpoint_name=dict(
                type='str'
            )
        )

        self.resource_group_name = None
        self.cluster_name = None
        self.private_endpoint_name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2020-03-01-preview'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMPrivateEndpointInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(Stream Analytics Management Client,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2020-03-01-preview')

        if (self.resource_group_name is not None and
            self.cluster_name is not None and
            self.private_endpoint_name is not None):
            self.results['private_endpoints'] = self.format_item(self.get())
        elif (self.resource_group_name is not None and
              self.cluster_name is not None):
            self.results['private_endpoints'] = self.format_item(self.listbycluster())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.private_endpoints.get(resource_group_name=self.resource_group_name,
                                                              cluster_name=self.cluster_name,
                                                              private_endpoint_name=self.private_endpoint_name)
        except CloudError as e:
            self.log('Could not get info for @(Model.ModuleOperationNameUpper).')

        return response

    def listbycluster(self):
        response = None

        try:
            response = self.mgmt_client.private_endpoints.list_by_cluster(resource_group_name=self.resource_group_name,
                                                                          cluster_name=self.cluster_name)
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
    AzureRMPrivateEndpointInfo()


if __name__ == '__main__':
    main()
