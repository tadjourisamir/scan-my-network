# 🔍 Scan My Network

A lightweight web app built with Flask, Scapy, and SQLite to scan your local network and display connected devices in real time.

---

## ⚙️ Features

- 🔎 ARP-based network scanning
- 🧠 Device identification (IP, MAC, hostname)
- 🗃 Local result storage with SQLite
- 📊 Web interface for viewing scan results
- 🔐 All data stays local (no external calls)

---

## 🚀 Getting Started (Local)

1. Clone the repository  
2. Create a virtual environment  
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment config:
   ```bash
   cp .env.example .env
   ```

5. Run the app:
   ```bash
   python app.py
   ```

Then open: [http://localhost:5001](http://localhost:5001)

---

## 📁 Project Structure

```
scan-my-network/
├── app.py
├── scanner.py
├── init_db.py
├── config/
│   └── version.py
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── scanner.html
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

---

## 🛠️ Technologies Used

- 🐍 Python 3.11  
- 🌐 Flask  
- 🧰 Scapy  
- 🗄 SQLite  
- 🎨 HTML + CSS + Javascript
---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](./LICENSE) for details.