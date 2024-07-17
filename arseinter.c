#include <stdio.h>
#include <string.h>
#include "a5625.h"
#define SZ 640

unsigned char out[SZ] = {0};
struct snd_chip a5625;

void frame(unsigned char per, unsigned char mode, unsigned char per_two, unsigned char mode_two) {
	a5625.channel[0].compare = per;
	a5625.channel[0].noise = (mode & 0x10) >> 4;
	a5625.channel[0].volume = mode & 0x0F;
	a5625.channel[1].compare = per_two;
	a5625.channel[1].noise = (mode_two & 0x10) >> 4;
	a5625.channel[1].volume = mode_two & 0x0F;
	for (int i=0;i<SZ;i++) {
		snd_clock(&a5625);
		out[i] = a5625.master_out;
	}
}

int main(int argc, char *argv[]) {
	snd_init(&a5625);
	unsigned char buf[4];
	char hbuf[4];
	const unsigned char end[4] = {0xff};
	int sz;
	FILE *f = fopen(argv[1], "rb");
	FILE *o = fopen("arse.out", "wb");
	fseek(f,0,SEEK_END);
	sz = ftell(f);
	rewind(f);
	fread(hbuf,1,4,f);
	if (strncmp(hbuf,"ARSE",4) != 0) {
		fclose(f);
		fprintf(stderr, "Not an ARSE file!\n");
		return 1;
	}
	for (int i=0;i<((sz/4-2));i++) {
		fread(buf,1,4,f);
		printf("%02x %02x %02x %02x\n", buf[0],buf[1],buf[2],buf[3]);
		if (memcmp(buf,end,4) == 0) break;
		frame(buf[0],buf[1],buf[2],buf[3]);
		fwrite(out,1,SZ,o);
	}
	fclose(f);
	fclose(o);
	return 0;
}
