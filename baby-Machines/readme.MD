# Lightweight Lab: Ansible Nodes as Containers

A simple, reproducible lab to spin up **minimal Linux containers** (Alpine) that act as **Ansible nodes**—perfect for quick testing without heavy VMs.

---

## ✅ What Changed
- **Simplified Dockerfile**: No entrypoint script, everything handled in Dockerfile.
- **Account Unlock Fix**: `ansible` user is unlocked and password removed to avoid SSH login issues.
- **ED25519 by Default**: Use modern, secure keys for SSH and Ansible.

---

## Plan
1. Use your Ubuntu VM (Hyper-V) as the **control/master** host.
2. Install Docker on the Ubuntu VM.
3. Build a **minimal Alpine image** that includes:
   - `python3` (required by Ansible)
   - `openssh-server` (to SSH into containers)
   - a non-root `ansible` user (passwordless sudo, unlocked)
4. Create a Docker bridge network, then run containers.
5. Push your ED25519 public key into containers.
6. Add container IPs to your Ansible inventory and test with `ansible -m ping`.

---

## ✅ Prerequisites
- Ubuntu VM with internet access
- Docker installed
- Ansible installed on the Ubuntu VM
- SSH key pair on the Ubuntu VM (`~/.ssh/id_ed25519` & `~/.ssh/id_ed25519.pub`)

Generate ED25519 key if missing:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
```

---

## ✅ Install Docker
```bash
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
# log out/in or: newgrp docker
```

(Optional) Install Ansible:
```bash
sudo apt-get install -y ansible
```

---

## ✅ Simplified Dockerfile (Alpine + Python + SSH)
Save as `Dockerfile.alpine-ansible`:

```dockerfile
FROM alpine:latest

# Install Python (for Ansible), OpenSSH (server), sudo, bash, shadow (for usermod/passwd)
RUN apk update && apk add --no-cache     python3     py3-pip     openssh     sudo     bash     shadow

# Create ansible user, unlock account, remove password
RUN adduser -D -s /bin/bash ansible &&     usermod -U ansible &&     passwd -d ansible &&     echo "ansible ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible

# Harden SSH config: disable root login, disable password auth, enable pubkey auth
RUN sed -i 's/#PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config &&     sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config &&     sed -i 's/#PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config &&     echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config

# Prepare ansible home and .ssh directory
RUN mkdir -p /home/ansible/.ssh &&     chmod 700 /home/ansible/.ssh &&     chmod 755 /home/ansible &&     chown -R ansible:ansible /home/ansible

# Generate SSH host keys at build time (simpler for lab)
RUN ssh-keygen -A

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
```

Build the image:
```bash
docker build -t alpine-ansible-sshd:latest -f Dockerfile.alpine-ansible .
```

---

## ✅ Create Docker Network
```bash
docker network create   --driver bridge   --subnet 172.19.0.0/24   --gateway 172.19.0.1   labnet
```

---

## ✅ Run Containers
```bash
docker run -d --name node1 --hostname node1 --network labnet --ip 172.19.0.10 -p 2201:22 alpine-ansible-sshd:latest
docker run -d --name node2 --hostname node2 --network labnet --ip 172.19.0.11 -p 2202:22 alpine-ansible-sshd:latest
docker run -d --name node3 --hostname node3 --network labnet --ip 172.19.0.12 -p 2203:22 alpine-ansible-sshd:latest
```

---

## ✅ Push ED25519 Key (Default Method)
For node3:
```bash
docker cp ~/.ssh/id_ed25519.pub node3:/home/ansible/.ssh/authorized_keys
docker exec node3 sh -c 'chmod 600 /home/ansible/.ssh/authorized_keys && chown ansible:ansible /home/ansible/.ssh/authorized_keys'
```
Repeat for node1 and node2.

Verify permissions:
```bash
docker exec node3 stat -c "%a %U:%G %n" /home/ansible /home/ansible/.ssh /home/ansible/.ssh/authorized_keys
# Expect: 755 / 700 / 600
```

---

## ✅ Test SSH
```bash
ssh -i ~/.ssh/id_ed25519 ansible@172.19.0.12
```

---

## ✅ Ansible Inventory
Create `inventory.ini`:
```ini
[labcontainers]
node1 ansible_host=172.19.0.10
node2 ansible_host=172.19.0.11
node3 ansible_host=172.19.0.12

[labcontainers:vars]
ansible_user=ansible
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

Test:
```bash
ansible -i inventory.ini labcontainers -m ping
```

---

## ✅ Why Unlocking Matters
Alpine's `adduser -D` creates a locked account (`!` in /etc/shadow). SSH refuses login to locked accounts—even with valid keys. We fix this by:
```dockerfile
usermod -U ansible && passwd -d ansible
```
This unlocks the account and removes the password, while `PasswordAuthentication no` ensures password login stays disabled.

---

## ✅ Cleanup
```bash
docker stop node1 node2 node3
docker rm -f node1 node2 node3
docker network rm labnet
```

---

**Security Note:** This setup is for labs only. For production, consider unique host keys per container and stricter SSH hardening.
