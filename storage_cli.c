#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STORAGE_FILE "storage.bin"
#define STORAGE_SIZE 1073741824 // 1 GB

// === Utility: Clean filename ===
// Removes extra spaces, tabs, and newlines safely into a destination buffer.
void clean_filename(const char *src, char *dest) {
    int j = 0;
    for (int i = 0; src[i]; i++) {
        if (src[i] != ' ' && src[i] != '\t' && src[i] != '\n' && src[i] != '\r') {
            dest[j++] = src[i];
        }
    }
    dest[j] = '\0';
}

void create_disk(const char *meta_file, long long size) {
    FILE *meta = fopen(meta_file, "w");
    if (!meta) {
        perror("❌ Error creating metadata file");
        return;
    }
    fprintf(meta, "Disk Name: %s\n", meta_file);
    fprintf(meta, "Start Offset: 0\n");
    fprintf(meta, "Size: %lld\n", size);
    fprintf(meta, "Files:\n");
    fclose(meta);
    printf("✅ Virtual disk '%s' created with size %lld bytes\n", meta_file, size);
}

void write_file(const char *meta_file, const char *input_file) {
    char command[1024];
    snprintf(command, sizeof(command),
             "./file_write_compressed \"%s\" \"%s\" \"%s\"",
             meta_file, STORAGE_FILE, input_file);

    printf("📤 Writing file '%s' into virtual disk using metadata '%s'...\n", input_file, meta_file);
    int result = system(command);
    if (result == 0) {
        printf("✅ File '%s' successfully written to virtual disk.\n", input_file);
    } else {
        printf("❌ Failed to write file '%s'. Check input file and paths.\n", input_file);
    }
}

void read_file(const char *meta_file, const char *file_name) {
    printf("📁 Cleaned filename before running system: '%s'\n", file_name);

    char command[1024];
    snprintf(command, sizeof(command),
             "./file_read_decompression \"%s\" \"%s\" \"%s\"",
             meta_file, STORAGE_FILE, file_name);

    printf("📥 Reading file '%s' from virtual disk...\n", file_name);
    int result = system(command);
    if (result == 0) {
        printf("✅ File '%s' successfully read and decompressed.\n", file_name);
    } else {
        printf("❌ Failed to read file '%s'. Make sure it exists.\n", file_name);
    }
}

void delete_file(const char *meta_file, const char *file_name) {
    char command[1024];
    snprintf(command, sizeof(command),
             "./delete_file \"%s\" \"%s\"",
             meta_file, file_name);

    printf("🗑️ Deleting file '%s' from virtual disk...\n", file_name);
    int result = system(command);
    if (result == 0) {
        printf("✅ File '%s' deleted successfully.\n", file_name);
    } else {
        printf("❌ Failed to delete file '%s'. Check if it exists.\n", file_name);
    }
}

void list_files(const char *meta_file) {
    char command[1024];
    snprintf(command, sizeof(command), "cat \"%s\"", meta_file);

    printf("📜 Listing files in '%s'...\n", meta_file);
    int result = system(command);
    if (result != 0) {
        printf("❌ Failed to list files. Metadata file not found.\n");
    }
}

int main(int argc, char *argv[]) {
    printf("DEBUG: argc = %d\n", argc);
    for (int i = 0; i < argc; i++) {
        printf("argv[%d] = '%s'\n", i, argv[i]);
    }

    if (argc < 2) {
        printf("Usage: %s <command> [args]\n", argv[0]);
        printf("\nCommands:\n");
        printf("  create_disk <meta_file> <size>\n");
        printf("  write_file <meta_file> <file>\n");
        printf("  read_file <meta_file> <file>\n");
        printf("  delete_file <meta_file> <file>\n");
        printf("  list_files <meta_file>\n");
        return 1;
    }

    const char *cmd = argv[1];
    char cleaned[512] = {0};

    // ✅ Only clean filename if provided
    if (argc >= 4) {
        clean_filename(argv[3], cleaned);
        printf("🧪 Cleaned filename: '%s'\n", cleaned);
    }

    if (strcmp(cmd, "create_disk") == 0 && argc == 4) {
        create_disk(argv[2], atoll(argv[3]));
    } 
    else if (strcmp(cmd, "write_file") == 0 && argc == 4) {
        write_file(argv[2], cleaned);
    } 
    else if (strcmp(cmd, "read_file") == 0 && argc == 4) {
        read_file(argv[2], cleaned);
    } 
    else if (strcmp(cmd, "delete_file") == 0 && argc == 4) {
        delete_file(argv[2], cleaned);
    } 
    else if (strcmp(cmd, "list_files") == 0 && argc == 3) {
        list_files(argv[2]);
    } 
    else {
        printf("❌ Invalid command or wrong arguments.\n");
        printf("💡 Usage examples:\n");
        printf("   ./storage_cli create_disk vdisk_disk1.meta 419430400\n");
        printf("   ./storage_cli write_file vdisk_disk1.meta myfile.txt\n");
        printf("   ./storage_cli read_file vdisk_disk1.meta myfile.txt\n");
        printf("   ./storage_cli delete_file vdisk_disk1.meta myfile.txt\n");
        printf("   ./storage_cli list_files vdisk_disk1.meta\n");
    }

    return 0;
}
