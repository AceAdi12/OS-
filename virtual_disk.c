#include<stdio.h>
#include<stdlib.h>

void createVirtualDisk(const char *diskname,long long start,long long size){
    char metaFile[100];

    sprintf(metaFile,"vdisk_%s.meta",diskname);
    FILE *f=fopen(metaFile,"w");
    if(!f){
        perror("Error creating virtual disk metadata");
        exit(1);
    }
    fprintf(f,"Disk Name :%s\n",diskname);
    fprintf(f,"Start Offset:%lld\n",start);
    fprintf(f,"Size:%lld\n",size);
    fprintf(f,"Files:\n");
    fclose(f);

    printf("Virtual Disk '%s' created successfully!]\n",diskname);
    printf("   ➤ Start Offset: %lld bytes\n", start);
    printf("   ➤ Size: %lld bytes (%.2f MB)\n\n", size, (double)size/(1024*1024));
}

int main(){
    printf("Creating Virtual Disks inside storage.bin(1GB pool)....\n\n");
    createVirtualDisk("DISK1",0,400*1024*1024);
    createVirtualDisk("DISK2",400*1024*1024,300*1024*1024);
    createVirtualDisk("DISK3",700*1024*1024,324*1024*1024);

    printf("All Virtual Disks created successfully.\n");
    printf("Metadata files generated for each disk.\n");
    return 0;
}