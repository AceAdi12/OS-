import tkinter as tk
from tkinter import messagebox
import subprocess
import re
import os

# ---------- Config ----------
CLI_BIN      = "./storage_cli"
DEFAULT_META = "vdisk_disk1.meta"

# ---------- Theme ----------
DARK_BG = "#1e1e2e"
TERM_BG = "#0e0e15"
TERM_FG = "#00ffaa"
ENTRY_BG = "#101018"

TITLE_FONT = ("Noto Sans Symbols2", 22, "bold")
TEXT_FONT  = ("Noto Sans Symbols2", 13)
INPUT_FONT = ("Courier New", 16)
BTN_FONT   = ("Noto Sans Symbols2", 14, "bold")

# ---------- CLI output----------
def clean_cli_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", s)
    s = s.replace("\u200b", "").replace("\u200c", "").replace("\u00A0", "")
    s = re.sub(r"(?<=\w)\s+([0-9]+)", r"\1", s)
    s = re.sub(r"\s*\.\s*", ".", s)
    lines = []
    for line in s.splitlines():
        if line.startswith("DEBUG") or line.startswith("argv["):
            continue
        lines.append(line)
    return "\n".join(lines).rstrip()

def fix_name(s: str) -> str:
    s = s.replace("\u00A0", "")                  
    s = re.sub(r"\s*([0-9]+)\s*", r"\1", s)      
    s = re.sub(r"\s*\.\s*", ".", s)              
    return s.strip()

class StorageShell(tk.Toplevel):
    def __init__(self, master, username="guest", role="guest"):
        super().__init__(master)
        self.title(f"💾 Storage Shell — {username} ({role.upper()})")
        self.geometry("1100x760")
        self.configure(bg=DARK_BG)

        tk.Label(self, text="🖥️ Storage Shell (Restricted Access)",
                 font=TITLE_FONT, bg=DARK_BG, fg=TERM_FG).pack(pady=(10, 2))
        tk.Label(self,
                 text="Commands:  list_files   read_file <file>   write_file <file>   delete_file <file>",
                 bg=DARK_BG, fg="#cfcfcf", font=("Noto Sans Symbols2", 13)).pack(pady=(0, 8))

        wrap = tk.Frame(self, bg=DARK_BG)
        wrap.pack(fill=tk.BOTH, expand=True)

        sc = tk.Scrollbar(wrap)
        sc.pack(side=tk.RIGHT, fill=tk.Y)

        self.term = tk.Text(wrap, bg=TERM_BG, fg=TERM_FG, insertbackground=TERM_FG,
                            font=TEXT_FONT, wrap="word", yscrollcommand=sc.set)
        self.term.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc.config(command=self.term.yview)

        self.term.insert(tk.END, "📢 Welcome! Type a command below.\n" + "─" * 80 + "\n")
        bottom = tk.Frame(self, bg=DARK_BG)
        bottom.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry = tk.Entry(bottom, font=INPUT_FONT, bg=ENTRY_BG, fg=TERM_FG, insertbackground=TERM_FG)
        self.entry.pack(side=tk.LEFT, padx=12, pady=10, ipadx=10, ipady=8, expand=True, fill=tk.X)
        self.entry.focus_set()

        tk.Button(bottom, text="▶ Run",  font=BTN_FONT, bg=TERM_FG, fg="black",
                  relief="flat", width=10, command=self.execute).pack(side=tk.LEFT, padx=(8, 6), pady=8)
        tk.Button(bottom, text="🧹 Clear", font=BTN_FONT, bg="#ff5c5c", fg="white",
                  relief="flat", width=10, command=lambda: self.term.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=(6, 12), pady=8)

        self.bind("<Return>", lambda _: self.execute())

    def execute(self):
        raw = self.entry.get()
        if raw is None:
            return

        self.term.insert(tk.END, f"\n$ {raw}\n")

        parts = raw.strip().split(" ", 1)
        cmd = parts[0]
        filename = parts[1] if len(parts) > 1 else ""

        allowed = {"list_files", "read_file", "write_file", "delete_file"}
        if cmd not in allowed:
            self.term.insert(tk.END,
                "❌ Unknown command.\n"
                "💡 Try: list_files | read_file <file> | write_file <file> | delete_file <file>\n")
            self._reset_after()
            return

        filename = fix_name(filename)
        meta_file = fix_name(DEFAULT_META)

        # Build argv
        if cmd == "list_files":
            argv = [CLI_BIN, "list_files", meta_file]
            title = "📂 Files Stored in Virtual Disk:\n"
        elif cmd == "read_file":
            argv = [CLI_BIN, "read_file", meta_file, filename]
            title = f"📥 Reading file: {filename}\n"
        elif cmd == "write_file":
            argv = [CLI_BIN, "write_file", meta_file, filename]
            title = f"📤 Writing file: {filename}\n"
        elif cmd == "delete_file":
            argv = [CLI_BIN, "delete_file", meta_file, filename]
            title = f"🗑️ Deleting file: {filename}\n"
        else:
            argv = []
            title = ""

        try:
            proc = subprocess.run(argv, text=True, capture_output=True, check=False)
            raw_output = (proc.stdout or "") + (proc.stderr or "")
            cleaned_output = clean_cli_text(raw_output)
            final_output = title + (cleaned_output if cleaned_output.strip() else "ℹ️ No output from CLI.")
            self.term.insert(tk.END, final_output + "\n")
        except FileNotFoundError:
            self.term.insert(tk.END, f"❌ CLI not found at '{CLI_BIN}'.\n")
        except Exception as e:
            self.term.insert(tk.END, f"❌ Error: {e}\n")

        self._reset_after()

    def _reset_after(self):
        self.term.insert(tk.END, "─" * 80 + "\n")
        self.term.see(tk.END)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

# --------- Simple login ----------
class Login(tk.Tk):
    USERS = {
        "admin":   {"password": "admin123", "role": "admin"},
        "student": {"password": "stud123",  "role": "student"},
        "guest":   {"password": "guest123", "role": "guest"},
    }

    def __init__(self):
        super().__init__()
        self.title("🔐 Storage Virtualization OS — Login")
        self.geometry("480x380")
        self.configure(bg=DARK_BG)

        tk.Label(self, text="🔐 Login", font=TITLE_FONT, bg=DARK_BG, fg=TERM_FG).pack(pady=(18, 10))

        card = tk.Frame(self, bg="#222334")
        card.pack(padx=20, pady=10, fill=tk.X)

        tk.Label(card, text="👤 Username", bg="#222334", fg="#ddd").pack(anchor="w", padx=12, pady=(12, 4))
        self.u = tk.Entry(card, font=INPUT_FONT, bg=ENTRY_BG, fg=TERM_FG, insertbackground=TERM_FG)
        self.u.pack(fill=tk.X, padx=12, ipady=6)

        tk.Label(card, text="🔑 Password", bg="#222334", fg="#ddd").pack(anchor="w", padx=12, pady=(12, 4))
        self.p = tk.Entry(card, show="•", font=INPUT_FONT, bg=ENTRY_BG, fg=TERM_FG, insertbackground=TERM_FG)
        self.p.pack(fill=tk.X, padx=12, ipady=6)

        tk.Button(self, text="🚀 Login", font=BTN_FONT, bg=TERM_FG, fg="black",
                  relief="flat", width=16, command=self.try_login).pack(pady=12)

        self.u.focus_set()
        self.bind("<Return>", lambda _: self.try_login())

    def try_login(self):
        user = (self.u.get() or "").strip()
        pwd  = (self.p.get() or "")
        rec = self.USERS.get(user)
        if rec and rec["password"] == pwd:
            messagebox.showinfo("✅ Login Success", f"Welcome {user} ({rec['role']})")
            self.withdraw()
            StorageShell(self, username=user, role=rec["role"])
        else:
            messagebox.showerror("❌ Login Failed", "Invalid username or password")
            self.p.delete(0, tk.END)
            self.u.focus_set()

# --------- Main ---------
if __name__ == "__main__":
    if not os.path.exists(CLI_BIN):
        print(f"[WARN] CLI binary not found at {CLI_BIN}. The UI will open, but commands will fail.")
    app = Login()
    app.mainloop()
