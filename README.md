🚀 Automating Network Switch Backups with Python & SSH 🔐

In our hospital's IT infrastructure, we manage 50+ Netgear switches, and maintaining their configuration backups is crucial for quick recovery and auditing. Manually backing them up was time-consuming and prone to human error.

So, I automated the entire backup process using Python + Paramiko (SSH)! 🐍💻

✅ Automatically connects to each switch via SSH
✅ Enters privileged mode (with enable)
✅ Executes key commands like show running-config, show startup-config
✅ Handles paginated outputs (--More--)
✅ Saves config files into date-wise folders with proper naming conventions

🔒 This ensures all switch configurations are backed up securely and consistently every day — with zero manual intervention.

Here's a glimpse of the script in action:

python
Copy
Edit
# Folder structure: E:\SWITCH\SWITCH-27-04-2025\10.1.1.11_20250427_154500.cfg
📂 With this scalable approach, I can now easily plug in multiple switch IPs and keep their configurations backed up daily — a small step towards robust network automation and cyber resilience.
