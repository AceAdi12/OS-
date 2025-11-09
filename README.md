# 💾 Storage Virtualization System

> A lightweight **Storage Virtualization System** implemented in C with a **Python-based GUI shell**.  
> Features include **virtual disk creation, compression, decompression, caching, deduplication, and deletion** — all built from scratch.

---

## 🚀 Project Overview

The **Storage Virtualization System** simulates how modern storage managers handle data efficiently.  
It allows users to:
- Create and manage **virtual disks**.
- Perform **file compression** using **Huffman coding**.
- Enable **data deduplication** via **SHA-256 hashing**.
- Implement **cache-based fast retrieval**.
- View and delete files seamlessly through a **CLI or GUI**.

---

## 🧩 System Architecture

┌────────────────────────────┐
│ GUI (Python) │
│ → Executes storage_cli │
└────────────┬───────────────┘
│
┌────────────▼───────────────┐
│ storage_cli.c │
│ Acts as a command hub │
│ ↳ Calls compression, etc. │
└────────────┬───────────────┘
│
├────────────────────────────┤
│ file_write_compressed.c │ → Handles file compression + deduplication
│ file_read_decompression.c │ → Handles decompression + cache mechanism
│ delete_file.c │ → Manages file deletion + hash updates
└────────────────────────────┘


---

## 🧠 Key Features

✅ **Virtual Disk Creation** — allocate and manage logical storage.  
✅ **Compression Algorithm** — Huffman-based, fully custom-implemented.  
✅ **Data Deduplication** — eliminates redundant writes using SHA-256 hashes.  
✅ **Cache Mechanism** — accelerates re-reads from a local cache folder.  
✅ **GUI Shell** — intuitive interface built using Python’s `tkinter`.  
✅ **Error Handling** — robust against corruption, duplicates, and invalid paths.

---

## 🧱 Technologies Used

| Layer | Technology |
|-------|-------------|
| Core System | **C (GCC)** |
| GUI Layer | **Python (Tkinter)** |
| Hashing | **OpenSSL SHA-256** |
| Compression | **Custom Huffman Coding** |
| OS | **Ubuntu (WSL/Linux)** |

---

## ⚙️ How to Build & Run

### 🔹 Step 1 — Compile all programs

```bash
gcc storage_cli.c -o storage_cli
gcc file_write_compressed.c -o file_write_compressed -lssl -lcrypto
gcc file_read_decompression.c -o file_read_decompression
gcc delete_file.c -o delete_file
```
### 🔹Step 2 — Create and use your virtual disk
```
./storage_cli create_disk vdisk_disk1.meta 419430400
./storage_cli write_file vdisk_disk1.meta test.txt
./storage_cli read_file vdisk_disk1.meta test.txt
./storage_cli list_files vdisk_disk1.meta
./storage_cli delete_file vdisk_disk1.meta test.txt
```
### 🔹Step 3 — Run GUI
```
python3 gui.py

```
📂 Project Structure
```
OS PROJECT/
├── storage_cli.c
├── file_write_compressed.c
├── file_read_decompression.c
├── delete_file.c
├── gui.py
├── cache/
├── storage.bin
├── vdisk_disk1.meta
└── hash_index.txt
```
## 🧪 Testing & Validation

| 🧩 Test Case | 🔍 Description | 🧠 Expected Result | ✅ Status |
|---------------|----------------|--------------------|-----------|
| **1. Disk Creation** | Create a virtual disk metadata file using CLI | Disk metadata file (`.meta`) is created successfully | ✅ Passed |
| **2. File Write (Compression)** | Write a new file into the virtual disk | File is compressed with Huffman coding and stored | ✅ Passed |
| **3. Duplicate File Write** | Try writing the same file again | System detects duplicate (via SHA-256 hash) and skips re-write | ✅ Passed |
| **4. File Read (Decompression)** | Read an existing file from virtual disk | File is decompressed and restored as `recovered_<file>` | ✅ Passed |
| **5. Cache Read Optimization** | Read a file again after caching | File is fetched instantly from `cache/` folder | ✅ Passed |
| **6. File Deletion** | Delete a file from disk and cache | File is removed from metadata, hash index, and cache | ✅ Passed |
| **7. Metadata Integrity** | Inspect `.meta` file after multiple operations | Metadata correctly lists active files only | ✅ Passed |
| **8. GUI Command Execution** | Perform all above operations via Python GUI | GUI runs without crash, correctly invokes CLI binaries | ✅ Passed |
| **9. Error Handling** | Try reading/deleting non-existent file | Graceful error message displayed (no crash) | ✅ Passed |
| **10. Large File Handling** | Compress and decompress large file (10–50 MB) | System handles it efficiently without corruption | ✅ Passed |

##🧑‍💻 Author
Aditya (AceAdi12)
📍 Developed as part of an Operating Systems Project (2025)
🧠 Focus: Storage Virtualization, C Programming, System Design

##🌟 Future Enhancements

-🧩 Add user-level file encryption (AES-256)
-📊 Integrate monitoring dashboard (I/O stats)
-☁️ Extend to cloud-based block storage simulation
-🔐 Implement user access control system

##🏆 Project Outcome

This project demonstrates a complete simulation of a virtual storage manager,
showcasing real-world OS concepts such as file systems, compression, and caching.
It serves as a strong foundation for research or further system-level experimentation.
