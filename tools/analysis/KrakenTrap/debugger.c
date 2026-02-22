#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>

void run_target(const char* prog_name) {
	printf("Running: %s\n", prog_name);

	// with the traceme request, the other args are ignored. i think...
	if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
		perror("ptrace");
		return;
	}
	// int execl(const char *path, const char *arg...
	execl(prog_name, prog_name, 0);
}

void run_debugger(pid_t child_pid) {
	printf("Child PID: %d\n", child_pid);
	int wait_status;
	unsigned icounter = 0;
	wait(&wait_status);

	// WIFSTOPPED checks if process stopped (not terminated)
	// returns non-zero (true) if stopped
	while (WIFSTOPPED(wait_status)) {
		icounter++;
		struct user_regs_struct regs;
		ptrace(PTRACE_GETREGS, child_pid, 0, &regs);
		unsigned instr = ptrace(PTRACE_PEEKTEXT, child_pid, regs.rip, 0);
		printf("ICOUNTER: %u.\tEIP: 0x%11x.\tINSTR: 0x%11x\n", icounter, regs.rip, instr);
		if (ptrace(PTRACE_SINGLESTEP, child_pid, 0, 0) < 0) {
			perror("ptrace");
			return;
		}
		wait(&wait_status);
	}
	printf("child executed %u instructions\n", icounter);
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




