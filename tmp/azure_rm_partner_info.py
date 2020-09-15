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
module: azure_rm_partner_info
version_added: '2.9'
short_description: Get Partner info.
description:
  - Get info of Partner.
options: {}
extends_documentation_fragment:
  - azure
author:
  - GuopengLin (@t-glin)

'''

EXAMPLES = '''
    - name: GetPartnerDetails
      azure_rm_partner_info: 
        {}
        

'''

RETURN = '''
partners:
  description: >-
    A list of dict results where the key is the name of the Partner and the
    values are the facts for that Partner.
  returned: always
  type: complex
  contains:
    etag:
      description:
        - Type of the partner
      returned: always
      type: integer
      sample: null
    id:
      description:
        - Identifier of the partner
      returned: always
      type: str
      sample: null
    name:
      description:
        - Name of the partner
      returned: always
      type: str
      sample: null
    type:
      description:
        - Type of resource. "Microsoft.ManagementPartner/partners"
      returned: always
      type: str
      sample: null
    partner_id:
      description:
        - This is the partner id
      returned: always
      type: str
      sample: null
    partner_name:
      description:
        - This is the partner name
      returned: always
      type: str
      sample: null
    tenant_id:
      description:
        - This is the tenant id.
      returned: always
      type: str
      sample: null
    object_id:
      description:
        - This is the object id.
      returned: always
      type: str
      sample: null
    version:
      description:
        - This is the version.
      returned: always
      type: integer
      sample: null
    updated_time:
      description:
        - This is the DateTime when the partner was updated.
      returned: always
      type: str
      sample: null
    created_time:
      description:
        - This is the DateTime when the partner was created.
      returned: always
      type: str
      sample: null
    state:
      description:
        - This is the partner state
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
    from azure.mgmt.ace import ACE Provisioning ManagementPartner API
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.polling import LROPoller
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMPartnerInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
        )


        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200]

        self.query_parameters = {}
        self.query_parameters['api-version'] = '2018-02-01'
        self.header_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        self.mgmt_client = None
        super(AzureRMPartnerInfo, self).__init__(self.module_arg_spec, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        self.mgmt_client = self.get_mgmt_svc_client(ACE Provisioning ManagementPartner API,
                                                    base_url=self._cloud_environment.endpoints.resource_manager,
                                                    api_version='2018-02-01')

        else:
            self.results['partners'] = self.format_item(self.get())
        return self.results

    def get(self):
        response = None

        try:
            response = self.mgmt_client.partners.get()
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
    AzureRMPartnerInfo()


if __name__ == '__main__':
    main()
