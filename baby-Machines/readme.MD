
# 🐳 Lightweight Lab: Ansible Nodes as Containers

A simple, reproducible lab to spin up **minimal Linux containers** (Alpine, Debian, RHEL UBI) that act as **Ansible nodes**—perfect for quick testing without heavy VMs.

---

## ✅ What’s New
- **Multi-Distro Support**: Added Dockerfiles for **Debian (bookworm-slim)** and **RHEL UBI9 Minimal** alongside Alpine.
- **Inventory Updated**: Includes Alpine, Debian, and RHEL nodes with group separation.
- **Consistent SSH Hardening**: No root login, no password auth, pubkey only.
- **Passwordless sudo** for `ansible` user across all distros.
- **Host Keys Generated at Build** for lab convenience.

---

## ✅ Directory Structure
```bash
/LearnDevOpsWithAI/baby-Machines
├── Dockerfile.alpine-ansible
├── Dockerfile.debian-ansible
├── Dockerfile.redhat-ubi-ansible
├── inventory.ini
└── readme.md
```

---

## ✅ Inventory Example
`inventory.ini`:
```ini
[labcontainers]
node1 ansible_host=172.19.0.10  # alpine
node2 ansible_host=172.19.0.11  # alpine
node3rhel ansible_host=172.19.0.12  # rhel ubi
node4debian ansible_host=172.19.0.13  # debian

[alpine]
node1
node2

[rhel]
node3rhel

[debian]
node4debian

[labcontainers:vars]
ansible_user=ansible
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

---

## ✅ Plan
1. Use your Ubuntu VM (Hyper-V) as the **control/master** host.
2. Install Docker and Ansible on the Ubuntu VM.
3. Build minimal images for **Alpine**, **Debian**, and **RHEL UBI**:
   - Python3 + pip (for Ansible)
   - OpenSSH server
   - Non-root `ansible` user (passwordless sudo, unlocked)
4. Create a Docker bridge network, then run containers.
5. Push your ED25519 public key into containers.
6. Test connectivity with `ansible -m ping`.

---

## ✅ Prerequisites
- Ubuntu VM with internet access
- Docker installed
- Ansible installed
- SSH key pair (`~/.ssh/id_ed25519` & `~/.ssh/id_ed25519.pub`)

Generate ED25519 key if missing:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
```

---

## ✅ Full Dockerfiles

### Alpine
`Dockerfile.alpine-ansible`:
```dockerfile
FROM alpine:latest

# Install Python (for Ansible), OpenSSH (server), sudo, bash, shadow (for usermod/passwd)
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    openssh \
    sudo \
    bash \
    shadow

# Create ansible user, unlock account, remove password
RUN adduser -D -s /bin/bash ansible && \
    usermod -U ansible && \
    passwd -d ansible && \
    echo "ansible ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible

# Harden SSH config: disable root login, disable password auth, enable pubkey auth
RUN sed -i 's/#PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config && \
    echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config

# Prepare ansible home and .ssh directory
RUN mkdir -p /home/ansible/.ssh && \
    chmod 700 /home/ansible/.ssh && \
    chmod 755 /home/ansible && \
    chown -R ansible:ansible /home/ansible

# Generate SSH host keys at build time (simpler for lab)
RUN ssh-keygen -A

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
```

---

### Debian
`Dockerfile.debian-ansible`:
```dockerfile
FROM debian:bookworm-slim

RUN set -eux; \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-server \
        sudo \
        bash \
        ca-certificates \
        vim-tiny && \
    rm -rf /var/lib/apt/lists/* && \
    \
    adduser --disabled-password --shell /bin/bash --gecos "" ansible && \
    passwd -d ansible || true && \
    \
    echo "ansible ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible && \
    chmod 0440 /etc/sudoers.d/ansible && \
    \
    mkdir -p /var/run/sshd && \
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config && \
    grep -q "^AuthorizedKeysFile" /etc/ssh/sshd_config || echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config && \
    \
    install -d -m 0755 -o ansible -g ansible /home/ansible && \
    install -d -m 0700 -o ansible -g ansible /home/ansible/.ssh && \
    \
    ssh-keygen -A

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
```

---

### RHEL UBI
`Dockerfile.redhat-ubi-ansible`:
```dockerfile
FROM redhat/ubi9-minimal

RUN set -eux; \
    microdnf update -y && \
    microdnf install -y \
        python3 \
        python3-pip \
        openssh-server \
        sudo \
        bash \
        shadow-utils && \
    microdnf clean all && \
    \
    useradd -m -s /bin/bash ansible && \
    passwd -d ansible || true && \
    usermod -U ansible || true && \
    \
    echo "ansible ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible && \
    chmod 0440 /etc/sudoers.d/ansible && \
    \
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config && \
    grep -q "^AuthorizedKeysFile" /etc/ssh/sshd_config || echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config && \
    \
    install -d -m 0755 -o ansible -g ansible /home/ansible && \
    install -d -m 0700 -o ansible -g ansible /home/ansible/.ssh && \
    \
    ssh-keygen -A

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
```

---

## ✅ Build Images
```bash
docker build -t alpine-ansible-sshd:latest -f Dockerfile.alpine-ansible .
docker build -t debian-ansible-sshd:latest -f Dockerfile.debian-ansible .
docker build -t rhel-ansible-sshd:latest -f Dockerfile.redhat-ubi-ansible .
```

---

## ✅ Create Docker Network
```bash
docker network create \
  --driver bridge \
  --subnet 172.19.0.0/24 \
  --gateway 172.19.0.1 \
  labnet
```

---

## ✅ Run Containers
```bash
docker run -d --name node1 --hostname node1 --network labnet --ip 172.19.0.10 -p 2201:22 alpine-ansible-sshd:latest
docker run -d --name node2 --hostname node2 --network labnet --ip 172.19.0.11 -p 2202:22 alpine-ansible-sshd:latest
docker run -d --name node3rhel --hostname node3rhel --network labnet --ip 172.19.0.12 -p 2203:22 rhel-ansible-sshd:latest
docker run -d --name node4debian --hostname node4debian --network labnet --ip 172.19.0.13 -p 2204:22 debian-ansible-sshd:latest
```

---

## ✅ Push SSH Key
Example for node4debian:
```bash
docker cp ~/.ssh/id_ed25519.pub node4debian:/home/ansible/.ssh/authorized_keys
docker exec node4debian sh -c 'chmod 600 /home/ansible/.ssh/authorized_keys && chown ansible:ansible /home/ansible/.ssh/authorized_keys'
```
Repeat for all nodes.

---

## ✅ Test SSH
```bash
ssh -i ~/.ssh/id_ed25519 ansible@172.19.0.13
```

---

## ✅ Test Ansible
```bash
ansible -i inventory.ini labcontainers -m ping
```

---

## ✅ Cleanup
```bash
docker stop node1 node2 node3rhel node4debian
docker rm -f node1 node2 node3rhel node4debian
docker network rm labnet
```

---

**Security Note:** This setup is for labs only. For production, consider unique host keys per container and stricter SSH hardening.
