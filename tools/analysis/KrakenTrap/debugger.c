#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/user.h>

void run_target(const char* prog_name) {
	printf("Analyzing: %s\n", prog_name);
}

void run_debugger(pid_t child_pid) {
	printf("Child PID: %d\n", child_pid);
}

int main(int argc, char** argv) {

	pid_t child_pid;

	if (argc < 2) {
		fprintf(stderr, "Expected a program name as argument.\n");
		return -1;
	}

	child_pid = fork();
	if (child_pid == 0) {
		run_target(argv[1]);
	} else if (child_pid > 0) {
		run_debugger(child_pid);
	} else {
		perror("fork");
		return -1;
	}

	return 0;

}




