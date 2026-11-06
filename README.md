README 

# Bug Dance

* What the project does

An interactive, ambient desktop overlay application for Windows 11 built with Python and PyQt6. Floating invertebrate graphics animate across your screen while full control remains accessible via the Windows System Tray. The invertebrates are real; the photographs were taken between 2022 and 2026 in the Czech Republic. No creatures, beetles, or spiders were harmed during the photography or the development of this software.
The repository does not publish the application code; it merely provides information about its existence. The repository contains documentation and support.

* Technical Setup & Running

Install from the Microsoft Store

* Features

System Tray Navigation: Runs seamlessly in the system notification area with `Bug_Dance.ico`.
Right-Click Control Menu
Pause / Play: Pause or resume all floating bug animations instantly.
Speed Controls: 5 speed tiers (Very Slow, Slow, Normal, Fast, Very Fast).
Always on top Toggle: Option to pin floating bugs above all active desktop windows.
Bugs Submenu (Bug #1 – Bug #24): Toggle individual bugs on or off.
Catalog of Bugs Sub-window: Open the About dialog and click ‘HERE’ - the Bugs Catalog automatically presents a 1000px wide Catalog preview (`Catalog_of_Bugs.png`) with numbers of bugs an explicit "Close" button.
Persistent Configuration: Automatically saves your speed, "Always on top" state, and bug selection to `bug_dance_config.json` upon exit and restores them on launch.
About Dialog: Displays legal notices, photographer credits, and clickable contact links.
Run at Windows start-up: Configures HKCU registry auto-start without requiring UAC administrative elevation.
Exit: Completely closes the application, overlay windows, and catalog dialog.

* Download Bug Dance from the Microsoft Store (https://apps.microsoft.com/detail/9n2sxrc95vv5?hl=en-US&gl=CZ
)

## Running from source and building

### Requirements

- Windows
- Python 3 with pip and venv support
- PyQt6
- PyInstaller (only needed to build the executable)

### Prepare the project

Download and extract the repository, or clone it. Keep these files together in the project directory:

- `main.py`
- `BugDance.spec`
- `Bug_Dance.ico`
- `Catalog_of_Bugs.png`
- All 24 photographs: `Jaroslav.M.Soukup_bugs_1.png` through `Jaroslav.M.Soukup_bugs_24.png`

Open PowerShell in that directory. Create a virtual environment and install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install PyQt6 PyInstaller
```

These commands install the currently available dependency versions; this project does not yet provide a pinned, tested dependency list.

### Run from source

```powershell
.\.venv\Scripts\python.exe main.py
```

Use the Bug Dance notification-area icon to access the controls. Choose **Exit** to close the application.

### Build the Windows executable

Run this command from the project directory:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm BugDance.spec
```

The executable is created at `dist\BugDance.exe`.

The supplied build configuration does not bundle the runtime images. Copy them and the icon into `dist`:

```powershell
Copy-Item -LiteralPath "Bug_Dance.ico", "Catalog_of_Bugs.png" -Destination ".\dist"
Copy-Item -Path ".\Jaroslav.M.Soukup_bugs_*.png" -Destination ".\dist"
```

Keep these files alongside the executable when moving or distributing the application.

### Run the built application

```powershell
.\dist\BugDance.exe
```

The application stores `bug_dance_config.json` beside the executable, or beside `main.py` when running from source. Use a folder where your Windows account has write permission so that preferences can be saved.

### Microsoft Store packaging

This procedure builds a standalone Windows executable. It does not create or sign a Microsoft Store MSIX package. Store packaging files and instructions are not included in this source folder.

### Redistribution

When distributing a build, include the applicable license texts and copyright notices, and provide the corresponding source code as required by GPLv3. Preserve the separate license terms for photographs and third-party components.

## License

Bug Dance software © 2026 Jiří X. Doležal is licensed under the GNU General Public License, version 3 (GPL-3.0-only). See [LICENSE](LICENSE) for the full terms.

The software may be used, modified, and redistributed, including commercially, subject to GPLv3. Redistribution requires preserving copyright and license notices and providing the corresponding source code as required by GPLv3. Distributed modified versions must also remain under GPLv3.

Photographs © 2026 Jaroslav M. Soukup are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). You may share and adapt them, including commercially, provided that you credit the photographer, link to the license, and indicate any changes.

Third-party components and artwork, including PyQt6, Qt, and Tux, remain subject to their respective licenses.

Concept & Software: © Jiri X. Dolezal (https://jxd.cz/)

Photography: © Jaroslav M. Soukup https://web.facebook.com/profile.php?id=100008282163799  https://www.instagram.com/jaroslavsoukup/ 

Tux © Larry Ewing 

Organization: JXD VibeLabs

Contact: jxd@jxd.cz

* Who manages and contributes to the project

The project manager and lead penguin is Jiří X. Doležal (jxd-cmyk), a universally odd individual from the Czech Republic.  Please contact him regarding this software, suggestions for application development, and complaints. Contact: jxd@jxd.cz

The director of the creature documentation section is Jaroslav M. Soukup, who enlists creatures dancing across desktops to collaborate and photographs them. Please contact him with questions regarding the use of his photographs, requests to add specific creatures to the project that are not yet featured here, and other matters related to RL.Contact: jsoukup1@centrum.cz

* VibeLabs is the last refuge for stoned binary penguins in Central Europe. It is based in Prague 6 and serves as a defense for its owner against senile dementia caused by brain inactivity in old age. 
Small flying creatures such as beetles, spiders, and bats fill the monitor with movement and inspire.
<img width="500" height="500" alt="JXD VibeLabs_white_500" src="https://github.com/user-attachments/assets/690589c4-b7c7-4fb3-8aad-a993bf3deae5" />
