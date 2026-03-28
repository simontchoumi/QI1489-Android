# Building QI1489 APK

## Option A — Google Colab (Easiest, no Linux needed)

1. Go to https://colab.research.google.com
2. Create a new notebook
3. Run these cells in order:

```python
# Cell 1 — Install buildozer and dependencies
%%bash
pip install buildozer
apt-get install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

```python
# Cell 2 — Upload your project as a zip
from google.colab import files
uploaded = files.upload()   # upload QI1489_Android.zip
```

```python
# Cell 3 — Unzip and build
%%bash
unzip QI1489_Android.zip -d QI1489_Android
cd QI1489_Android
buildozer android debug
```

```python
# Cell 4 — Download the APK
from google.colab import files
import glob
apk = glob.glob('QI1489_Android/bin/*.apk')[0]
files.download(apk)
```

---

## Option B — WSL2 on Windows (Local build)

### 1. Install WSL2 + Ubuntu
```powershell
# In PowerShell as Administrator:
wsl --install -d Ubuntu
```

### 2. Install build dependencies (inside Ubuntu terminal)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    build-essential python3-dev
pip3 install --user buildozer cython
```

### 3. Copy project and build
```bash
# Copy project to WSL home (adjust path)
cp -r /mnt/c/Users/GSI/QI1489_Android ~/QI1489_Android
cd ~/QI1489_Android
~/.local/bin/buildozer android debug
```

### 4. Get the APK
The APK will be at: `~/QI1489_Android/bin/qi1489-1.0-arm64-v8a_armeabi-v7a-debug.apk`

Copy it back to Windows:
```bash
cp ~/QI1489_Android/bin/*.apk /mnt/c/Users/GSI/Desktop/
```

---

## Option C — GitHub Actions (Cloud build, free)

1. Create a GitHub repository
2. Push this folder to it
3. Create `.github/workflows/build.yml`:

```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with: { python-version: '3.11' }
      - name: Install dependencies
        run: |
          sudo apt-get install -y git zip unzip openjdk-17-jdk \
            autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
            libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
          pip install buildozer cython
      - name: Build APK
        run: buildozer android debug
      - uses: actions/upload-artifact@v3
        with:
          name: QI1489-APK
          path: bin/*.apk
```

---

## Testing on Desktop (No build needed)

Before building the APK, test on your Windows PC:

```bash
cd C:\Users\GSI\QI1489_Android
pip install kivy[base]==2.3.0 kivymd==1.1.1 requests
python main.py
```

---

## Default Admin Credentials

- Username: `admin`
- Password: `admin@QI1489`

Change them after first login via Admin > Users.

---

## Copyright
(c) Simon TCHOUMI NJANJOU | SMJx Game | +237676262622
