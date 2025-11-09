#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define BLOCK_SIZE 4096 //4KB of block size

void createStoragePool(const char*filename,long long size){
    FILE *f=fopen(filename,"wb");
    if(!f){
        perror("Error while creating the storage pool");
        exit(1);
    }
    char buffer[BLOCK_SIZE];
    memset(buffer,0,BLOCK_SIZE);
    
    long long written=0;
    while(written<size){
        long long towrite=(size-written>BLOCK_SIZE)?BLOCK_SIZE:(size-written);
        fwrite(buffer,1,towrite,f);
        written+=towrite;
    }
    fclose(f);
    printf("Storage pool '%s' created (%lld bytes)\n",filename,size);

}
int main(){
    long long poolSize=1024*1024*1024;
    createStoragePool("storage.bin",poolSize);
    return 0;
}