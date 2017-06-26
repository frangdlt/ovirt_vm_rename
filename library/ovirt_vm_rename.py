#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from datetime import datetime
from ovirtsdk.api import API
from ovirtsdk.xml import params
from time import sleep

DOCUMENTATION = '''
module: ovirt_vm_rename
short_description: Renames an existing OVIRT vm.
description:
    - Longer description of the module
version_added: "0.1"
author: "Fran Garcia, @frangdlt"
notes:
    - Details at https://github.com/frangdlt/ovirt_vm_rename
requirements:
    - ovirt sdk'''

EXAMPLES = '''
- name: Create Ovirt snapshot with specific name
  ovirt_snapshot:
   state: present
   url: https://127.0.0.1/ovirt-engine/api
   user: admin@internal
   password: unix1234
   name: vmname
   newname: vmnewname
'''

def main():
    argument_spec = {
        "url": {"default": 'https://127.0.0.1/ovirt-engine/api', "required": False, "type": "str"},
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "newname": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=argument_spec)
    url = module.params['url']
    # if module.params['user'] in [None, ""]:
    #     user = "admin@internal"
    # else:
    #     user = module.params['user']
    user = "admin@internal"
    password = module.params['password']
    name = module.params['name']
    newname = module.params['newname']
    api = API(url=url, username=user, password=password, insecure=True)

    if name == newname:
        module.exit_json(changed=False, skipped=True, meta="")

    vm = api.vms.get(name=name)
    if not vm:
        module.fail_json(msg='Vm %s not found' % name)

    vmnew = api.vms.get(name=newname)
    if vmnew:
        module.fail_json(msg='Vm %s already exists' % newname)

    vm = vm.update(vm.set_name(newname))
    module.exit_json(changed=True, skipped=False, meta="")

if __name__ == '__main__':
    main()
