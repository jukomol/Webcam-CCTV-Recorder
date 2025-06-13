# CCTV Web App with Flask + Electron

A lightweight Python web application built with Flask that turns your webcam into a basic CCTV system. Stream the live camera feed in your browser, record footage hourly, browse saved videos, and start/stop recording from the interface.

This project is a full-featured CCTV application that allows you to:
- Stream live webcam footage
- Record footage into hourly segments
- Browse and download past recordings from the UI
- Run as a web server or cross-platform desktop app (via Electron)

---

## 🔧 Features

- 🔴 **Live Webcam Feed** via browser
- 📁 **Automatic Hourly Recording** (MP4 format)
- ▶️ **Start/Stop Recording** from UI
- 📂 **Explore & Download Recordings** from a simple file browser
- 🧵 Thread-safe capture and recording using locks and threading
- 🐳 **Docker Support** for easy deployment
- 💻 **Windows Compatible** (uses `cv2.CAP_DSHOW`)
- 🌐 **Accessible over LAN, public IP, Cloudflare Tunnel, or ZeroTier**

---

## 📂 Project Structure

```
📁 webcam-cctv-recorder/
│
├── app.py                     # Flask backend
├── templates/
│   └── index.html             # UI layout with stream and recordings
├── static/
│   └── recordings/            # Folder where hourly videos are stored
│
└── electron/                  # Electron desktop app shell
    ├── main.js                # Electron launcher
    └── package.json           # Electron dependencies & scripts
```

---

## ⚙️ Setup Instructions

### 🐍 Run as Flask Web App

1. Install dependencies:
   ```bash
   pip install flask opencv-python
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Visit `http://localhost:5000` in your browser.

---

### 🐳 Docker Deployment

#### Build the Image

```bash
docker build -t webcam-cctv .
```

#### Run the Container

On **Linux**:

```bash
docker run -p 5000:5000 --device=/dev/video0 webcam-cctv
```

On **Windows** (Hyper-V / WSL2 only):

> Pass USB webcam through WSL2 or use `--mount` with host integration.

---


### 💻 Run as Desktop App with Electron

1. Navigate to the Electron folder:
   ```bash
   cd electron
   npm install
   ```

2. Add this to your `package.json`:
   ```json
   {
     "name": "cctv-app",
     "version": "1.0.0",
     "main": "main.js",
     "scripts": {
       "start": "electron ."
     },
     "dependencies": {
       "electron": "^29.0.0"
     }
   }
   ```

3. Run the app:
   ```bash
   npm start
   ```

4. Electron main process (`main.js`):
   ```js
   const { app, BrowserWindow } = require('electron');

   function createWindow() {
     const win = new BrowserWindow({
       width: 1280,
       height: 800,
       webPreferences: {
         nodeIntegration: false
       }
     });
     win.loadURL('http://localhost:5000');
   }

   app.whenReady().then(createWindow);
   ```

---

## 🌐 Remote Access Options

- **LAN**: `http://<your-local-IP>:5000`
- **Cloudflare Tunnel**:
  ```bash
  cloudflared tunnel --url http://localhost:5000
  ```
- **ZeroTier**: Configure devices on the same ZeroTier network and access via assigned IP

---

## 📸 UI Preview

![alt text](image.png)

---

## 👤 Author

Developed by [JU KOMOL](https://github.com/jukomol)

---

## 📜 License

[MIT License](LICENSE)
