# Ansible Playbooks - Quick Guide

This README provides a very simple explanation of Ansible playbooks and how to use them.

## What is an Ansible Playbook?
An Ansible playbook is a YAML file that defines automation tasks to be executed on remote systems. Playbooks allow you to:
- Install packages
- Copy files
- Manage services

## Basic Structure of a Playbook
```yaml
---
- name: Example Playbook
  hosts: all
  become: true
  tasks:
    - name: Install Apache
      ansible.builtin.yum:
        name: httpd
        state: present

    - name: Ensure Apache is running
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: true
```

## How to Run a Playbook
```bash
ansible-playbook -i inventory.ini playbook.yml -b -K
```
- `-i inventory.ini` specifies your inventory file.
- `-b` enables privilege escalation (sudo).
- `-K` asks for sudo password if required.

## Official Documentation
For more details on Ansible built-in modules, visit:
[Ansible Built-in Collection](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/index.html#plugins-in-ansible-builtin)

