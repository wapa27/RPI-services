
# Raspberry Pi Setup Instructions

## 1) Install Hella Listener
- Download `HellaListener.py` to `~/Documents/Hella_sensor/`
- Setup virtual environment:  
  ```bash
  python -m venv hella-fast
  ```

* Activate virtual environment:

  ```bash
  source hella-fast/bin/activate
  ```
* Install dependencies:

  ```bash
  pip install fastapi uvicorn defusedxml requests
  ```
* Test app:

  ```bash
  uvicorn HellaListener:app --host 192.168.1.1 --port 8080
  ```
* Deactivate environment:

  ```bash
  deactivate
  ```
* Create the systemd service:

  ```bash
  sudo nano /etc/systemd/system/aaa-hella-listener.service
  ```
* Paste the contents of `aaa-hella-listener.service` into the file, save and exit (`Ctrl+X`, then `Y`, then `Enter`)
* Enable the service:

  ```bash
  sudo systemctl enable aaa-hella-listener.service
  ```

---

## 2) Install Modem API

* Download `ModemApi.py` to `~/Documents/ModemInterface/`
* Setup virtual environment:

  ```bash
  python -m venv modemVenv
  ```
* Activate virtual environment:

  ```bash
  source modemVenv/bin/activate
  ```
* Install dependencies:

  ```bash
  pip install flask pyserial
  ```
* Test app:

  ```bash
  python ModemApi.py
  ```
* Deactivate environment:

  ```bash
  deactivate
  ```
* Create the systemd service:

  ```bash
  sudo nano /etc/systemd/system/aaa-modem.service
  ```
* Paste the contents of `aaa-modem.service` into the file, save and exit (`Ctrl+X`, then `Y`, then `Enter`)
* Enable the service:

  ```bash
  sudo systemctl enable aaa-modem.service
  ```

---

## 3) Configure dhcpcd

* Install dhcpcd:

  ```bash
  sudo apt-get update
  sudo apt-get install dhcpcd5
  ```
* Override service configuration:

  ```bash
  sudo systemctl edit dhcpcd
  ```
* Add the following to the override file:

  ```ini
  interface eth0
  static ip_address=192.168.1.1/24
  nolink
  ```
* Enable and start dhcpcd:

  ```bash
  sudo systemctl enable dhcpcd
  sudo systemctl restart dhcpcd
  ```

---

## 4) Configure dnsmasq

* Install dnsmasq:

  ```bash
  sudo apt-get update
  sudo apt-get install dnsmasq
  ```
* Modify /etc/dnsmasq.conf:
```bash
bind-interfaces
dhcp-range=192.168.50.10,192.168.50.50,12h
dhcp-option=3,192.168.50.1
dhcp-option=6,8.8.8.8,8.8.4.4
```
* Create override directory if it doesn't exist and edit override file:

  ```bash
  sudo mkdir -p /etc/systemd/system/dnsmasq.service.d
  sudo nano /etc/systemd/system/dnsmasq.service.d/override.conf
  ```
* Add the following:
```
  [Unit]
  After=network-online.target
  Wants=network-online.target
  [Service]
  Restart=on-failure
  RestartSec=10
  ExecStartPre=/bin/bash -c 'until ip link show eth0 | grep -q "state UP"; do sleep 1; done

  ```
* Reload systemd and enable dnsmasq:

  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable dnsmasq
  sudo systemctl restart dnsmasq
  ```

---

## 5) Reboot the Raspberry Pi

```bash
sudo reboot
```

---

## 6) Verify services are running

```bash
sudo systemctl list-units --type=service
```

