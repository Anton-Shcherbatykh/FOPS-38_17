#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Your Name <your.email@example.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: write_file
short_description: Create a text file with specified content
version_added: "1.0.0"
description:
    - This module creates a text file on the remote host with the given content.
    - If the file already exists, it will be overwritten.
options:
    path:
        description:
            - The absolute path to the file to be created.
        required: true
        type: str
    content:
        description:
            - The content to write into the file.
        required: true
        type: str
author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create a file with content
  my_namespace.my_collection.write_file:
    path: /tmp/example.txt
    content: "Hello, Ansible!"

- name: Overwrite existing file
  my_namespace.my_collection.write_file:
    path: /tmp/example.txt
    content: "New content"
'''

RETURN = r'''
path:
    description: The path of the file that was created/modified.
    returned: always
    type: str
    sample: "/tmp/example.txt"
content:
    description: The content that was written.
    returned: always
    type: str
    sample: "Hello, Ansible!"
changed:
    description: Whether the file was created or changed.
    returned: always
    type: bool
    sample: true
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # result dictionary
    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    # Check if file already exists and content differs
    file_exists = os.path.exists(path)
    existing_content = None
    if file_exists:
        try:
            with open(path, 'r') as f:
                existing_content = f.read()
        except Exception as e:
            module.fail_json(msg="Failed to read existing file: %s" % str(e), **result)

    # Determine if change is needed
    if file_exists and existing_content == content:
        result['changed'] = False
        result['path'] = path
        result['content'] = content
        module.exit_json(**result)

    # If in check mode, report change but don't write
    if module.check_mode:
        result['changed'] = True
        result['path'] = path
        result['content'] = content
        module.exit_json(**result)

    # Ensure directory exists
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        try:
            os.makedirs(dirname, mode=0o755)
        except Exception as e:
            module.fail_json(msg="Failed to create directory %s: %s" % (dirname, str(e)), **result)

    # Write file
    try:
        with open(path, 'w') as f:
            f.write(content)
    except Exception as e:
        module.fail_json(msg="Failed to write file %s: %s" % (path, str(e)), **result)

    result['changed'] = True
    result['path'] = path
    result['content'] = content
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()