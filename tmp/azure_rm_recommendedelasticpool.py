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
module: azure_rm_recommendedelasticpool
version_added: '2.9'
short_description: Manage Azure RecommendedElasticPool instance.
description:
  - 'Create, update and delete instance of Azure RecommendedElasticPool.'
options:
  resource_group_name:
    description:
      - >-
        The name of the resource group that contains the resource. You can
        obtain this value from the Azure Resource Manager API or the portal.
    required: true
    type: str
  server_name:
    description:
      - The name of the server.
    required: true
    type: str
  recommended_elastic_pool_name:
    description:
      - The name of the recommended elastic pool to be retrieved.
    required: true
    type: str
  state:
    description:
      - Assert the state of the RecommendedElasticPool.
      - >-
        Use C(present) to create or update an RecommendedElasticPool and
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
database_edition:
  description:
    - >-
      The edition of the recommended elastic pool. The ElasticPoolEdition
      enumeration contains all the valid editions.
  returned: always
  type: str
  sample: null
dtu:
  description:
    - The DTU for the recommended elastic pool.
  returned: always
  type: number
  sample: null
database_dtu_min:
  description:
    - The minimum DTU for the database.
  returned: always
  type: number
  sample: null
database_dtu_max:
  description:
    - The maximum DTU for the database.
  returned: always
  type: number
  sample: null
storage_mb:
  description:
    - Gets storage size in megabytes.
  returned: always
  type: number
  sample: null
observation_period_start:
  description:
    - The observation period start (ISO8601 format).
  returned: always
  type: str
  sample: null
observation_period_end:
  description:
    - The observation period start (ISO8601 format).
  returned: always
  type: str
  sample: null
max_observed_dtu:
  description:
    - Gets maximum observed DTU.
  returned: always
  type: number
  sample: null
max_observed_storage_mb:
  description:
    - Gets maximum observed storage in megabytes.
  returned: always
  type: number
  sample: null
databases:
  description:
    - The list of databases in this pool. Expanded property
  returned: always
  type: list
  sample: null
  contains:
    location:
      description:
        - Resource location.
      returned: always
      type: str
      sample: null
    tags:
      description:
        - Resource tags.
      returned: always
      type: dictionary
      sample: null
metrics:
  description:
    - The list of databases housed in the server. Expanded property
  returned: always
  type: list
  sample: null
  contains:
    date_time:
      description:
        - The time of metric (ISO8601 format).
      returned: always
      type: str
      sample: null
    dtu:
      description:
        - >-
          Gets or sets the DTUs (Database Transaction Units). See
          https://azure.microsoft.com/documentation/articles/sql-database-what-is-a-dtu/
      returned: always
      type: number
      sample: null
    size_gb:
      description:
        - Gets or sets size in gigabytes.
      returned: always
      type: number
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


class AzureRMRecommendedElasticPool(AzureRMModuleBaseExt):
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
            recommended_elastic_pool_name=dict(
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
        self.server_name = None
        self.recommended_elastic_pool_name = None
        self.body = {}

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMRecommendedElasticPool, self).__init__(derived_arg_spec=self.module_arg_spec,
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
                                                    api_version='2014-04-01')

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
                response = self.mgmt_client.recommended_elastic_pools.create()
            else:
                response = self.mgmt_client.recommended_elastic_pools.update()
            if isinstance(response, AzureOperationPoller) or isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the RecommendedElasticPool instance.')
            self.fail('Error creating the RecommendedElasticPool instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_resource(self):
        try:
            response = self.mgmt_client.recommended_elastic_pools.delete()
        except CloudError as e:
            self.log('Error attempting to delete the RecommendedElasticPool instance.')
            self.fail('Error deleting the RecommendedElasticPool instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        try:
            response = self.mgmt_client.recommended_elastic_pools.get(resource_group_name=self.resource_group_name,
                                                                      server_name=self.server_name,
                                                                      recommended_elastic_pool_name=self.recommended_elastic_pool_name)
        except CloudError as e:
            return False
        return response.as_dict()


def main():
    AzureRMRecommendedElasticPool()


if __name__ == '__main__':
    main()
