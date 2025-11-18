import angr
import claripy

__all__ = ["angr_fuzz"]

def angr_fuzz(handler, params):

	elf = params["binpath"]
	base_addr  = int(params["base"], 16)
	solve_addr = int(params["solve"], 16)
	avoid_addr = int(params["avoid"], 16)
	FLAG_SIZE  = params["flagsize"] if params["flagsize"] is not 'None' else 32

	handler.Print('i', "Fuzzing binary...\n")

	sym_chars = [claripy.BVS('flag_%d'%i, 8) for i in range(int(FLAG_SIZE))]
	sym_flag  = claripy.Concat(*sym_chars + [claripy.BVV(b'\n')])

	proj = angr.Project(f"{elf}", main_opts={'base_addr':base_addr})
	state = proj.factory.full_init_state(args=[f'./{elf}'], stdin=sym_flag)

	for c in sym_chars:
		# keep chars in readable range
		state.solver.add(c >= ord("!"), c <= ord("~"))

	# simulation manager
	simgr = proj.factory.simulation_manager(state)
	simgr.explore(find=solve_addr, avoid=avoid_addr)

	if (len(simgr.found) > 0):
        	for found in simgr.found:
                	handler.Print('s', f"Output: {found.posix.dumps(0)}\n")
