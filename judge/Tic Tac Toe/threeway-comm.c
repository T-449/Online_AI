#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/socket.h>
#include <poll.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <assert.h>
#include <signal.h>


#define  BUFF_SIZE 5
char buff[BUFF_SIZE];

int pid[3];
int fd[3][2];
char* process_names[3] = {"zero","one","judge"}; 
char* process_path[3] = {"./zero","./one","./judge"}; 


volatile int is_alarm_active;


void Exit(int exitCode) {
	if(pid[0]) kill(pid[0], SIGKILL);
	if(pid[1]) kill(pid[1], SIGKILL);
	if(pid[2]) kill(pid[2], SIGKILL);
	exit(exitCode);
}
void alarm_handler(int signum) {
	printf("Timeout\n");
	dprintf(fd[2][1],"timeout\n");
	fsync(fd[2][1]);
	waitpid(pid[2],NULL,NULL);
	Exit(0);
}

static int read_until_newline(int fd, char *buffer, size_t max_num_bytes, int timeout) {
	int num_read=0;

	alarm(timeout);
	while(num_read<max_num_bytes) {
		int num_available=0;
		int err = ioctl(fd, FIONREAD, &num_available);
		if(err) continue;
		

		if(num_available) {
			int rc = read(fd,buffer,1);
			if(rc==1) {
				num_read++;
				if(*buffer=='\n') return num_read;
				buffer++;
			} else if (rc==-1) {
				perror("read error");
				return -1;
			}	
		}
		
	}
	alarm(0);

	return num_read;
}



static int read_numbytes(int fd, char *buffer, size_t num_bytes, int timeout) {
	int num_available=0;
	
	alarm(timeout);
	while(num_available<num_bytes) {
		int temp = num_available;
		int err = ioctl(fd, FIONREAD, &num_available);
		if(err) num_available=temp;
		
	}
	alarm(0);

	int rc = read(fd,buffer,num_bytes);
	if(rc==-1) {
		perror("read");
		return 0;
	} else return rc;


}

void spawn_process(int index) {
	pid[index] = fork();
	
	if(pid[index]==-1) {
		printf("exec %s failed\n",process_names[index]);
		Exit(-1);
	}
	
	if(pid[index]==0) {
		close(fd[index][1]);
		dup2(fd[index][0],0);
		dup2(fd[index][0],1);
		int ret = execlp(process_path[index],process_names[index],NULL);
		printf("execlp error at %s\n",process_names[index]);
		Exit(-1);
	}

	close(fd[index][0]);
}


void handle_messages(int index,int read_bytes) {
	if(read_bytes==0) {
		printf("Judge Read Error\n");
		Exit(-1);
	} 

	buff[read_bytes-1]='\0';
	
	printf("%s\n",buff);
	if(strcmp(buff,"ok")==0) return;
	if(strcmp(buff,"end")==0) {
		printf("Game Terminated\n");
		waitpid(pid[2], NULL, NULL);
		Exit(0);
	} else {
		assert(printf("unrecognized message\n : %s\n",buff) && 0);
		Exit(0);
	}
}



int main(int argc, char* argv []) {
	assert(argc == 4);
	process_path[0] = argv[1];
	process_path[1] = argv[2];
	process_path[2] = argv[3];
	signal(SIGALRM,alarm_handler);

	printf("%s %s %s\n",process_path[0],process_path[1],process_path[2]);
	socketpair(AF_UNIX,SOCK_STREAM,0,fd[0]);
	socketpair(AF_UNIX,SOCK_STREAM,0,fd[1]);
	socketpair(AF_UNIX,SOCK_STREAM,0,fd[2]);
	

	spawn_process(0);
	spawn_process(1);
	spawn_process(2);
	
	//init
	int r = read_until_newline(fd[2][1],buff,1024,10);
	dprintf(fd[0][1],buff,r);
	
	r = read_until_newline(fd[2][1],buff,1024,10);
	dprintf(fd[1][1],buff,r);
      
      	while (1) {
		int r = read_until_newline(fd[0][1],buff,1024,2);
		dprintf(fd[2][1],"ok\n");
		write(fd[2][1],buff,r);
	
		r = read_until_newline(fd[2][1],buff,1024,10);
		handle_messages(0,r);
		r = read_until_newline(fd[2][1],buff,1024,10);
		write(fd[1][1],buff,r);
		
		
		r = read_until_newline(fd[1][1],buff,1024,2);
		dprintf(fd[2][1],"ok\n");
		write(fd[2][1],buff,r);

		r = read_until_newline(fd[2][1],buff,1024,10000);
		handle_messages(1,r);	
		r = read_until_newline(fd[2][1],buff,1024,10000);
		write(fd[0][1],buff,r);
							
	}







		

		

	
}
