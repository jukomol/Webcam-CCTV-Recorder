const { app, BrowserWindow } = require('electron');
const path = require('path');
const { exec } = require('child_process');

let pyProc = null;

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    }
  });

  win.loadURL('http://127.0.0.1:5000');
}

function startPythonApp() {
  const script = path.join(__dirname, '..', 'app.py');
  pyProc = exec(`python "${script}"`, (error, stdout, stderr) => {
    if (error) console.error(error);
    if (stdout) console.log(stdout);
    if (stderr) console.error(stderr);
  });
}

app.whenReady().then(() => {
  startPythonApp();
  setTimeout(() => {
    createWindow();
  }, 3000); // wait for Flask to spin up
});

app.on('window-all-closed', () => {
  if (pyProc) {
    pyProc.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
