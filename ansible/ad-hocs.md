# Ansible Ad-Hoc Commands (Quick Guide)

  Introduction to ad hoc commands : https://docs.ansible.com/projects/ansible/latest/command_guide/intro_adhoc.html#intro-adhoc

Run one-off tasks without playbooks using `ansible` CLI.

## Syntax
```bash
ansible <pattern> -m <module> -a "<args>"
```
- `<pattern>`: target hosts/groups
- `-m`: module (default = command)
- `-a`: module arguments

## Common Flags
`-u <user>` SSH user | `--become` escalate | `-K` ask sudo pwd | `-f <n>` forks | `-C` check mode

---

### Examples

#### Ping
```bash
ansible all -m ping
```

#### Reboot
```bash
ansible atlanta -a "/sbin/reboot" -f 10 --become -K
```

#### Shell vs Command
```bash
ansible raleigh -a "/usr/bin/uptime"           # command
ansible raleigh -m shell -a 'echo $TERM'       # shell
```

#### Copy & File
```bash
ansible atlanta -m copy -a "src=/etc/hosts dest=/tmp/hosts"
ansible webservers -m file -a "dest=/srv/foo/a.txt mode=600"
```

#### Packages
```bash
ansible webservers -m yum -a "name=acme state=present"
ansible webservers -m yum -a "name=acme state=absent"
```

#### Users
```bash
ansible all -m user -a "name=foo state=present"
ansible all -m user -a "name=foo state=absent"
```

#### Services
```bash
ansible webservers -m service -a "name=httpd state=started"
```

#### Facts
```bash
ansible all -m setup
```

#### Dry Run
```bash
ansible all -m copy -a "content=foo dest=/root/bar.txt" -C
```

---

## Patterns
`all` | `group` | `host` | combine/exclude/slice/regex

---

### Best Practices
- Use ad-hoc for quick tasks; playbooks for reusable workflows.

