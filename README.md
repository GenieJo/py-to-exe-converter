
🧠 Program Purpose 

A user-friendly GUI tool that converts any Python script into a standalone .exe file using PyInstaller, with automatic icon handling, smart cleanup, and a beautiful dark-purple interface. 
 
🏗️ Core Components 
1. UI Layer (Tkinter) 

    Window: Fixed size 380x500, non-resizable.  
    Theme: Dark purple (#1a0a2e) background with rich purple buttons (#6a0dad).  
    Widgets:  
        File browsers for .py and .ico  
        Optional output name field  
        Checkboxes for:  
            Include Console (shows terminal window)  
            One File (bundles everything into one .exe)  
            Auto-inject icon (for Tkinter apps only)
             
        Progress bar and status label  
        "✨ Convert to .exe" button
         
     

    💡 Where to modify UI:
    → create_widgets() method
    → Color constants at top of __init__ 
     

 
2. File Selection & Validation 

    Uses filedialog.askopenfilename() to pick:  
        Python script (.py)  
        Icon file (.ico)
         
    Auto-fills output name from script filename if empty.
     

    💡 Where to add new file types:
    → select_script() / select_icon() methods
    → Update filetypes in askopenfilename() 
     

 
3. Tkinter Detection & Icon Injection 

    Detects Tkinter: Scans first 2KB of script for "tkinter" import.  
    Injects icon code: If enabled and script uses Tkinter, it:  
        Finds lines like root = tk.Tk()  
        Inserts code right after to load iconbitmap from embedded resources  
        Uses a temporary modified script (.temp) during build
         
     

    💡 Where to support other GUIs (PyQt, Kivy, etc.):
    → Add new detection logic in is_tkinter_script() (rename to detect_gui_type())
    → Add injection templates in a new method like inject_pyqt_icon() 
     

 
4. Icon Handling Strategy 

    If selected .ico is not in the same folder as the .py:  
        Copies it into the script folder temporarily  
        Uses it in PyInstaller via --icon and --add-data
         
    After build:  
        Deletes the copied .ico (original remains untouched)  
        Only deletes if it was copied (not if it was already there)
         
     

    💡 Key variable: icon_was_copied (boolean flag) 
     

 
5. PyInstaller Execution 

    Builds command dynamically based on user options:  
    python
     

     
    1
    ["pyinstaller", "--onefile", "--noconsole", "--icon=app.ico", "--add-data=app.ico;.", "script.py"]
     
     
    Runs in the script’s directory (cwd=script_dir)  
    Captures output and errors
     

    💡 Where to add new PyInstaller flags:
    → Inside the cmd = [...] block in convert() 
     

 
6. Post-Build Cleanup (Critical!) 

After successful build, it:   

    Moves .exe from dist/ → same folder as original .py  
    Deletes:  
        dist/ folder  
        build/ folder  
        .spec file  
        Temporary injected script (.temp)  
        Copied .ico file (if any)
         
     

    💡 Cleanup logic location:
    → Bottom of try block in convert() method
    → Look for comments: # ✅ POST-BUILD CLEANUP and # 🔥 Remove the COPIED .ico 
     

 
7. Error Handling 

    Catches:  
        PyInstaller failures (subprocess.CalledProcessError)  
        Missing dependencies (FileNotFoundError)  
        Unexpected errors (Exception)
         
    Shows user-friendly messages via messagebox
     

    💡 Where to improve logging:
    → Add log file output or detailed error reporting 
     

 
📁 File Flow Summary 
 
 
1
2
3
4
5
6
7
8
9
10
User selects:
  script.py  → in any folder
  icon.ico   → anywhere

Program:
  1. Copies icon.ico → script folder (if needed)
  2. Optionally creates script.py.temp (with icon code)
  3. Runs PyInstaller in script folder
  4. Moves dist/script.exe → script folder
  5. Deletes: dist/, build/, script.spec, script.py.temp, (copied) icon.ico
 
 

✅ Final result: Only script.py and script.exe remain in the folder. 
 
🔮 Ideas for Future Extensions 
Support for
PyQt/Kivy icon injection
	
New detection + injection methods
Drag & drop
file support
	
Bind
<Drop>
events to entries
Save last used paths
	
Use
json
or
configparser
Multi-file project support
	
Add
--add-data
for folders
Custom PyInstaller args
	
Add text entry for extra flags
Dark/light theme toggle
	
Add theme switcher in UI
 
 
🧩 Key Design Principles 

    Non-destructive: Never modifies original .py or .ico  
    Self-cleaning: Leaves zero build artifacts  
    User-first: Clear status, progress, and error feedback  
    Tkinter-smart: Only injects when safe and needed
     