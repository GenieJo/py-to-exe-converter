import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import sys
import os
import re
import shutil

class PyToExeConverter:
    def __init__(self, root):
        self.root = root
        root.title("PyInstaller GUI Converter")
        root.geometry("380x500")
        root.resizable(False, False)
        
        # Dark purple theme
        self.bg_color = "#1a0a2e"      # Deep purple
        self.button_color = "#6a0dad"  # Rich purple
        self.button_hover = "#8a2be2"  # Brighter purple
        self.text_color = "#e0d6ff"
        self.entry_bg = "#2d1b4a"
        self.entry_fg = "#f0f0ff"
        
        root.configure(bg=self.bg_color)
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🐍 Py to EXE Converter",
            font=("Segoe UI", 14, "bold"),
            fg="#d4bfff",
            bg=self.bg_color
        )
        title.pack(pady=(15, 10))

        # Script selection
        tk.Label(self.root, text="Python Script:", font=("Segoe UI", 10, "bold"), fg=self.text_color, bg=self.bg_color).pack(anchor="w", padx=20, pady=(10, 0))
        script_frame = tk.Frame(self.root, bg=self.bg_color)
        script_frame.pack(fill="x", padx=20, pady=5)
        self.script_entry = tk.Entry(script_frame, textvariable=self.get_script_var(), state="readonly", font=("Consolas", 9), bg=self.entry_bg, fg=self.entry_fg, relief="flat")
        self.script_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.script_btn = tk.Button(script_frame, text="Browse...", command=self.select_script, bg=self.button_color, fg="white", relief="flat", font=("Segoe UI", 9))
        self.script_btn.pack(side="right")

        # Icon selection
        tk.Label(self.root, text="Icon File (.ico):", font=("Segoe UI", 10, "bold"), fg=self.text_color, bg=self.bg_color).pack(anchor="w", padx=20, pady=(10, 0))
        icon_frame = tk.Frame(self.root, bg=self.bg_color)
        icon_frame.pack(fill="x", padx=20, pady=5)
        self.icon_entry = tk.Entry(icon_frame, textvariable=self.get_icon_var(), state="readonly", font=("Consolas", 9), bg=self.entry_bg, fg=self.entry_fg, relief="flat")
        self.icon_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.icon_btn = tk.Button(icon_frame, text="Browse...", command=self.select_icon, bg=self.button_color, fg="white", relief="flat", font=("Segoe UI", 9))
        self.icon_btn.pack(side="right")

        # Output name
        tk.Label(self.root, text="Output Name (optional):", font=("Segoe UI", 10, "bold"), fg=self.text_color, bg=self.bg_color).pack(anchor="w", padx=20, pady=(10, 0))
        self.name_entry = tk.Entry(self.root, textvariable=self.get_name_var(), font=("Consolas", 9), bg=self.entry_bg, fg=self.entry_fg, relief="flat")
        self.name_entry.pack(fill="x", padx=20, pady=5)

        # Options
        opts_frame = tk.Frame(self.root, bg=self.bg_color)
        opts_frame.pack(fill="x", padx=20, pady=10)
        tk.Checkbutton(opts_frame, text="Include Console", variable=self.get_console_var(), bg=self.bg_color, fg=self.text_color, selectcolor=self.entry_bg, font=("Segoe UI", 9)).pack(anchor="w")
        tk.Checkbutton(opts_frame, text="One File", variable=self.get_onefile_var(), bg=self.bg_color, fg=self.text_color, selectcolor=self.entry_bg, font=("Segoe UI", 9)).pack(anchor="w", pady=(2,0))
        tk.Checkbutton(opts_frame, text="Auto-inject icon (Tkinter)", variable=self.get_inject_var(), bg=self.bg_color, fg=self.text_color, selectcolor=self.entry_bg, font=("Segoe UI", 9)).pack(anchor="w", pady=(2,0))

        # Convert button
        self.convert_btn = tk.Button(
            self.root,
            text="✨ Convert to .exe",
            command=self.convert,
            bg=self.button_color,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            height=2,
            relief="flat",
            activebackground=self.button_hover
        )
        self.convert_btn.pack(fill="x", padx=40, pady=20)

        # Progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("purple.Horizontal.TProgressbar", foreground='#8a2be2', background='#8a2be2')
        self.progress_bar = ttk.Progressbar(self.root, mode="indeterminate", style="purple.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", padx=40, pady=(0, 10))

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 9), fg="#b8a0d9", bg=self.bg_color)
        self.status_label.pack()

    # Variable getters (to avoid AttributeError on init)
    def get_script_var(self):
        if not hasattr(self, '_script_var'):
            self._script_var = tk.StringVar()
        return self._script_var

    def get_icon_var(self):
        if not hasattr(self, '_icon_var'):
            self._icon_var = tk.StringVar(value="No icon selected")
        return self._icon_var

    def get_name_var(self):
        if not hasattr(self, '_name_var'):
            self._name_var = tk.StringVar()
        return self._name_var

    def get_console_var(self):
        if not hasattr(self, '_console_var'):
            self._console_var = tk.BooleanVar(value=False)
        return self._console_var

    def get_onefile_var(self):
        if not hasattr(self, '_onefile_var'):
            self._onefile_var = tk.BooleanVar(value=True)
        return self._onefile_var

    def get_inject_var(self):
        if not hasattr(self, '_inject_var'):
            self._inject_var = tk.BooleanVar(value=True)
        return self._inject_var

    def select_script(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            self.get_script_var().set(path)
            if not self.get_name_var().get():
                self.get_name_var().set(os.path.splitext(os.path.basename(path))[0])

    def select_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if path:
            self.get_icon_var().set(path)

    def is_tkinter_script(self, script_path):
        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)
            return 'tkinter' in content or 'from tkinter' in content or 'import tkinter' in content
        except:
            return False

    def inject_icon_code(self, script_path, icon_name):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            injected = False
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if re.search(r'\w+\s*=\s*tk\.Tk\(\)', line) or re.search(r'\w+\s*=\s*Tk\(\)', line):
                    indent = line[:len(line) - len(line.lstrip())]
                    new_lines.append(f'{indent}# Injected icon\n')
                    new_lines.append(f'{indent}import os, sys\n')
                    new_lines.append(f'{indent}icon_path = os.path.join(sys._MEIPASS, "{icon_name}") if getattr(sys, "frozen", False) else "{icon_name}"\n')
                    new_lines.append(f'{indent}try:\n')
                    new_lines.append(f'{indent}    {line.split("=")[0].strip()}.iconbitmap(icon_path)\n')
                    new_lines.append(f'{indent}except: pass\n')
                    injected = True

            if injected:
                temp_path = script_path + ".temp"
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                return temp_path
        except Exception as e:
            print(f"Injection failed: {e}")
        return script_path

    def convert(self):
        script = self.get_script_var().get()
        icon = self.get_icon_var().get()
        use_icon = icon != "No icon selected"
        output_name = self.get_name_var().get() or os.path.splitext(os.path.basename(script))[0]

        if not script:
            messagebox.showerror("Error", "Please select a Python script.")
            return

        script_dir = os.path.dirname(script)
        self.status_var.set("Copying icon...")
        self.root.update()

        # Copy icon to script folder (only if it's not already there)
        icon_name = None
        icon_was_copied = False
        if use_icon:
            icon_name = os.path.basename(icon)
            icon_dest = os.path.join(script_dir, icon_name)
            if icon != icon_dest:
                shutil.copy2(icon, icon_dest)
                icon_was_copied = True  # Remember we copied it

        # Prepare script
        final_script = script
        if use_icon and self.get_inject_var().get() and self.is_tkinter_script(script):
            final_script = self.inject_icon_code(script, icon_name)

        # Build command
        cmd = ["pyinstaller"]
        if self.get_onefile_var().get():
            cmd.append("--onefile")
        if not self.get_console_var().get():
            cmd.append("--noconsole")
        if use_icon:
            cmd.extend(["--icon", icon_name])
            cmd.extend(["--add-data", f"{icon_name};."])
        if output_name:
            cmd.extend(["--name", output_name])
        cmd.append(os.path.basename(final_script))

        # Run PyInstaller
        try:
            self.progress_bar.start()
            self.convert_btn.config(state="disabled", text="Building...")
            self.status_var.set("Building EXE...")

            result = subprocess.run(
                cmd,
                cwd=script_dir,
                capture_output=True,
                text=True,
                check=True
            )

            # ✅ POST-BUILD CLEANUP
            self.status_var.set("Cleaning up...")
            self.root.update()

            # Move .exe to script folder
            exe_name = output_name + ".exe"
            dist_exe = os.path.join(script_dir, "dist", exe_name)
            final_exe = os.path.join(script_dir, exe_name)

            if os.path.exists(dist_exe):
                if os.path.exists(final_exe):
                    os.remove(final_exe)
                shutil.move(dist_exe, final_exe)

            # Remove build folders and spec
            for item in ["dist", "build"]:
                folder = os.path.join(script_dir, item)
                if os.path.exists(folder):
                    shutil.rmtree(folder)
            spec_file = os.path.join(script_dir, output_name + ".spec")
            if os.path.exists(spec_file):
                os.remove(spec_file)

            # Clean temp script
            if final_script != script and os.path.exists(final_script):
                os.remove(final_script)

            # 🔥 Remove the COPIED .ico file (only if we copied it)
            if use_icon and icon_was_copied:
                icon_to_remove = os.path.join(script_dir, icon_name)
                try:
                    if os.path.exists(icon_to_remove):
                        os.remove(icon_to_remove)
                except Exception as e:
                    print(f"Warning: Could not delete icon file: {e}")

            self.status_var.set("✅ Done!")
            messagebox.showinfo("Success", f"EXE created:\n{final_exe}")

        except subprocess.CalledProcessError as e:
            self.status_var.set("❌ Build failed")
            messagebox.showerror("Error", f"Build failed:\n{e.stderr}")
        except Exception as e:
            self.status_var.set("❌ Error")
            messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")
        finally:
            self.progress_bar.stop()
            self.convert_btn.config(state="normal", text="✨ Convert to .exe")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyToExeConverter(root)
    root.mainloop()