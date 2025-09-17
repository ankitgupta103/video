# Installing vyomcloudbridge

You can install `vyomcloudbridge` in three ways:

---

## 1. Install in a Python Virtual Environment (recommended)

1. Create a virtual environment:
   ```bash
   python3 -m venv my_venv
   ```

2. Activate the environment:
   ```bash
   source /complete_path_to/my_venv/bin/activate
   ```

3. Install vyomcloudbridge:
   ```bash
   pip install vyomcloudbridge==<LTS_version>
   ```

4. Now you can use it as both a Python package and CLI command.

> **Note**: `vyomcloudbridge` works only inside the virtual environment where it is installed and activated.

---

## 2. Install Without Virtual Environment (user-level, no root)

1. Install package:
   ```bash
   pip install --user vyomcloudbridge==<LTS_version>
   ```

2. Verify installation:
   ```bash
   vyomcloudbridge list --all
   ```

3. If the `vyomcloudbridge` command is not found:

   - **3.1 Check installation path:**
     ```bash
     pip show vyomcloudbridge
     ```
     Expected output:  
     ```
     $HOME/.local/lib/python3.10/site-packages
     ```

   - **3.2 Check PATH configuration:**
     ```bash
     echo $PATH
     ```
     Should contain:
     ```
     $HOME/.local/bin
     ```

     If missing, update bash file:
     ```bash
     echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
     source ~/.bashrc
     ```

   - **3.3 Confirm installation:**
     ```bash
     vyomcloudbridge list --all
     ```
     Now `vyomcloudbridge` CLI should be accessible.

> **Note**: User-level installation does not require root access but may affect other Python packages in your user environment.

---

## 3. Install in Root (system-wide)

1. Install package:
   ```bash
   sudo pip install vyomcloudbridge==<LTS_version>
   ```

2. Accessible as both Python package and CLI command.

> **Note**: Requires root access and can affect the global Python environment for all users.

---

## Notes

- Use **Option 1 (virtual environment)** for clean and isolated installation.  
- Use **Option 2** if you don’t have root access.  
- Use **Option 3** only if system-wide installation is required.  