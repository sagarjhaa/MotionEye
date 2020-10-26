# MotionEye

motion eye client to capture images and upload to server.

# Setup raspberry pi

# setup motioneye to capture images

# download this repo on to PI and the server

# configure

# Run the client

# Run the server

# Run client code as service on raspberry pi

Source: [link](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-3-systemd)

### create a new service

```
sudo nano /lib/systemd/system/fileUpload.service
```

### copy paste the below details in the file if the git repo is on Desktop

```
[Unit]
Description=File upload service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python /home/pi/Desktop/MotionEye/client.py

[Install]
WantedBy=multi-user.target
```

### reload demon to recognize our new service

```
sudo systemctl daemon-reload
```

### Enable out new service

```
sudo systemctl enable fileUpload.service
```

### Reboot to test if it runs on startup

```
sudo reboot
```

### Check status of service

```
systemctl status fileUpload.service
```
