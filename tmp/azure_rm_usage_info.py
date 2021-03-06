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
module: azure_rm_usage_info
version_added: '2.9'
short_description: Get Usage info.
description:
  - Get info of Usage.
options:
  region_id:
    description:
      - 'The region Id (westus, eastus)'
    required: true
    type: str
  filter:
    description:
      - >-
        The filter to apply on the list operation. only name.value is allowed
        here as a filter e.g. $filter=name.value eq 'xxxx'
    required: true
    type: str
extends_documentation_fragment:
  - azure
author:
  - GuopengLin (@t-glin)

'''

EXAMPLES = '''
    - name: ListUsages
      azure_rm_usage_info: 
        region_id: westus2
        

'''

RETURN = '''
usages:
  description: >-
    A list of dict results where the key is the name of the Usage and the values
    are the facts for that Usage.
  returned: always
  type: complex
  contains:
    next_link:
      description:
        - Link for next list of DedicatedCloudNode
      returned: always
      type: str
      sample: null
    value:
      description:
        - The list of usages
      returned: always
      type: list
      sample: null
      contains:
        current_value:
          description:
            - The current usage value
          returned: always
          type: integer
          sample: null
        limit:
          description:
            - >-
              limit of a given sku in a region for a subscription. The maximum
              permitted value for the usage quota. If there is no limit, this
              value will be -1
          returned: always
          type: integer
          sample: null
        name:
          description:
            - Usage name value and localized name
          returned: always
          type: dict
          sample: null
          contains:
            localized_value:
              description:
                - e.g. "Virtual Machines"
              returned: always
              type: str
              sample: null
            value:
              description:
                - 'resource type or resource type sku name, e.g. virtualMachines'
              returned: always
              type: str
              sample: null
        unit:
          description:
            - The usages' unit
          returned: always
          type: sealed-choice
          sample: null

'''

import time
import json
from ansible.module_utils.azure_rm_common import AzureRMModuleBase
from copy import deepcopy
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.vmware import VMwareCloudSimple
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMUsageInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            region_id=dict(
                type='str',
                required=True
            ),
            filter=dict(
                type='str',
                required=True
            )
        )

        self.region_id = None
        self.filter = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2019-04-01'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMUsageInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(VMwareCloudSimple,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2019-04-01')

        if (self.region_id is not None):
            self.results['usages'] = self.format_item(self.list())
        return self.results

    def list(self):
        response = None

        try:
            response = self.mgmt_client.usages.list(region_id=self.region_id,
                                                    filter=self.filter)
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
    AzureRMUsageInfo()


if __name__ == '__main__':
    main()
