# Autopad

**Autopad** is a robust Python automation tool designed to programmatically control Windows Notepad. It bridges the gap between legacy automation and modern Windows 11 UI patterns, capable of handling text injection, file saving with specific encodings (UTF-8), and intelligent tab management.

It utilizes a hybrid approach, combining **UIA (User Interface Automation)** for reliable control interaction and **Computer Vision** for visual element detection.

## 🚀 Features

* **Windows 11 Ready:** specifically designed to handle the modern `Document` control type and Tab interface in the new Notepad.
* **Smart Content Injection:** Checks if the active document is empty; if not, safely opens a new tab (`Ctrl + N`) to prevent data loss.
* **Hybrid Automation:**
    * **UIA Backend:** Uses `pywinauto` to interact with menus, dialogs, and text controls.
    * **Computer Vision:** Uses image recognition (in `vision/find.py`) to detect specific UI states or icons when standard handles are unavailable.
* **Dynamic Content:** Fetches post content via `api/posts.py` (or local JSON) to automate writing tasks.
* **Modern Dependency Management:** Built using `uv` for fast and reliable package management.

## 🛠️ Prerequisites

* **OS:** Windows 10 or Windows 11
* **Python:** 3.10+
* **Package Manager:** [uv](https://github.com/astral-sh/uv) (recommended)

## 📥 Installation

1.  **Clone the repository**
    ```bash
    git clone --depth 1 --single-branch --branch master [https://github.com/hsamn/autopad.git](https://github.com/hsamn/autopad.git)
    cd autopad
    ```

2.  **Install dependencies**
    Autopad uses `uv` to manage dependencies and lockfiles.
    ```bash
    uv sync
    ```

## ▶️ Usage

To start the automation script, use the standard entry point via `uv`:

```bash
uv run python -m autopad.main
