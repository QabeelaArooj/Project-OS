"""
Deadlock Management Simulator
=============================
Console based project covering:
  1. Deadlock Avoidance  -> Banker's Algorithm (safety + resource request)
  2. Deadlock Detection  -> Matrix detection algorithm + Wait-For Graph cycle
  3. Deadlock Recovery   -> Process termination (cheapest victim first)

Run:  python deadlock_simulator.py
"""


class DeadlockSystem:
    def __init__(self, available, maximum, allocation):
        self.n = len(maximum)            # number of processes
        self.m = len(available)          # number of resource types
        self.available = list(available)
        self.maximum = [list(r) for r in maximum]
        self.allocation = [list(r) for r in allocation]
        self.terminated = set()

    # ---------- helpers ----------
    def need(self):
        return [[self.maximum[i][j] - self.allocation[i][j]
                 for j in range(self.m)] for i in range(self.n)]

    @staticmethod
    def _le(a, b):
        return all(x <= y for x, y in zip(a, b))

    def validate(self):
        """Returns an error message if the data is inconsistent, else None."""
        for i in range(self.n):
            for j in range(self.m):
                if self.allocation[i][j] > self.maximum[i][j]:
                    return (f"P{i}: allocation of resource {chr(65 + j)} "
                            f"exceeds its maximum claim.")
        return None

    # ---------- 1. AVOIDANCE: Banker's safety algorithm ----------
    def is_safe(self):
        need = self.need()
        work = self.available[:]
        finish = [i in self.terminated for i in range(self.n)]
        sequence = []
        progress = True
        while progress:
            progress = False
            for i in range(self.n):
                if not finish[i] and self._le(need[i], work):
                    work = [work[j] + self.allocation[i][j] for j in range(self.m)]
                    finish[i] = True
                    sequence.append(i)
                    progress = True
        return all(finish), sequence

    # ---------- 1b. AVOIDANCE: Resource-Request algorithm ----------
    def request_resources(self, pid, req):
        need = self.need()
        if pid in self.terminated:
            return False, f"P{pid} has already been terminated."
        if not self._le(req, need[pid]):
            return False, "Error: the process requested more than its maximum claim."
        if not self._le(req, self.available):
            return False, f"P{pid} must wait (resources not available)."

        # Pretend to allocate
        for j in range(self.m):
            self.available[j] -= req[j]
            self.allocation[pid][j] += req[j]

        safe, seq = self.is_safe()
        if safe:
            return True, ("Request GRANTED. New safe sequence: "
                          + " -> ".join(f"P{i}" for i in seq))

        # Rollback
        for j in range(self.m):
            self.available[j] += req[j]
            self.allocation[pid][j] -= req[j]
        return False, "Request DENIED: granting it would leave the system in an UNSAFE state."

    # ---------- 2. DETECTION ----------
    def detect_deadlock(self):
        """Matrix detection algorithm (Request = remaining Need).
        Returns the list of deadlocked processes."""
        request = self.need()
        work = self.available[:]
        finish = []
        for i in range(self.n):
            holds_nothing = all(a == 0 for a in self.allocation[i])
            finish.append(i in self.terminated or holds_nothing)

        progress = True
        while progress:
            progress = False
            for i in range(self.n):
                if not finish[i] and self._le(request[i], work):
                    work = [work[j] + self.allocation[i][j] for j in range(self.m)]
                    finish[i] = True
                    progress = True
        return [i for i in range(self.n) if not finish[i]]

    def wait_for_graph(self):
        """P_i -> P_j if P_i needs a resource that is not available
        and P_j currently holds that resource type."""
        need = self.need()
        graph = {i: [] for i in range(self.n) if i not in self.terminated}
        for i in graph:
            if self._le(need[i], self.available):
                continue                       # not blocked
            for r in range(self.m):
                if need[i][r] > self.available[r]:
                    for j in graph:
                        if j != i and self.allocation[j][r] > 0 and j not in graph[i]:
                            graph[i].append(j)
        return graph

    @staticmethod
    def find_cycle(graph):
        """DFS cycle detection. Returns the cycle as a list or None."""
        visited, stack, path = set(), set(), []

        def dfs(node):
            visited.add(node)
            stack.add(node)
            path.append(node)
            for nxt in graph.get(node, []):
                if nxt not in visited:
                    cyc = dfs(nxt)
                    if cyc:
                        return cyc
                elif nxt in stack:
                    return path[path.index(nxt):] + [nxt]
            stack.remove(node)
            path.pop()
            return None

        for p in graph:
            if p not in visited:
                cyc = dfs(p)
                if cyc:
                    return cyc
        return None

    # ---------- 3. RECOVERY ----------
    def recover(self):
        """Terminate deadlocked processes one at a time (fewest resources
        held first) until the deadlock is gone."""
        log = []
        deadlocked = self.detect_deadlock()
        while deadlocked:
            victim = min(deadlocked, key=lambda p: (sum(self.allocation[p]), p))
            released = self.allocation[victim][:]
            for j in range(self.m):
                self.available[j] += released[j]
                self.allocation[victim][j] = 0
                self.maximum[victim][j] = 0
            self.terminated.add(victim)
            log.append(f"Terminated P{victim}, released resources: {released}")
            deadlocked = self.detect_deadlock()
        return log


# ======================= CONSOLE UI =======================

def read_int(prompt, low=0, high=None):
    while True:
        try:
            value = int(input(prompt))
            if value < low or (high is not None and value > high):
                raise ValueError
            return value
        except ValueError:
            rng = f"{low}-{high}" if high is not None else f"{low} or more"
            print(f"  Invalid input. Please enter a number ({rng}).")


def read_vector(prompt, size):
    while True:
        parts = input(prompt).split()
        try:
            vec = [int(x) for x in parts]
            if len(vec) != size or any(v < 0 for v in vec):
                raise ValueError
            return vec
        except ValueError:
            print(f"  Enter exactly {size} non-negative numbers separated by spaces.")


def print_table(title, rows, m):
    header = "      " + "  ".join(f"{chr(65 + j):>3}" for j in range(m))
    print(f"\n{title}")
    print(header)
    for i, row in enumerate(rows):
        print(f"  P{i:<2} " + "  ".join(f"{v:>3}" for v in row))


def show_state(s):
    print_table("Allocation:", s.allocation, s.m)
    print_table("Max:", s.maximum, s.m)
    print_table("Need (Max - Allocation):", s.need(), s.m)
    print("\nAvailable: " + "  ".join(f"{chr(65 + j)}={v}" for j, v in enumerate(s.available)))
    if s.terminated:
        print("Terminated: " + ", ".join(f"P{p}" for p in sorted(s.terminated)))


def enter_data():
    n = read_int("Number of processes: ", 1, 20)
    m = read_int("Number of resource types: ", 1, 10)
    print("\nAvailable resources (instances of each type):")
    available = read_vector(f"  Available [{m} values]: ", m)
    maximum, allocation = [], []
    for i in range(n):
        while True:
            mx = read_vector(f"  P{i} Max        [{m} values]: ", m)
            al = read_vector(f"  P{i} Allocation [{m} values]: ", m)
            if all(a <= x for a, x in zip(al, mx)):
                break
            print("  Allocation cannot exceed Max. Please re-enter.")
        maximum.append(mx)
        allocation.append(al)
    return DeadlockSystem(available, maximum, allocation)


def sample_safe():
    return DeadlockSystem(
        available=[3, 3, 2],
        maximum=[[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
        allocation=[[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
    )


def sample_deadlock():
    return DeadlockSystem(
        available=[0, 0],
        maximum=[[1, 1], [1, 1], [2, 0]],
        allocation=[[1, 0], [0, 1], [1, 0]],
    )


MENU = """
================ DEADLOCK MANAGEMENT SIMULATOR ================
 1. Enter data manually
 2. Load sample data (SAFE state)
 3. Load sample data (DEADLOCK state)
 4. Show current state
 5. Safety check (Banker's Algorithm)
 6. Request resources (Avoidance)
 7. Detect deadlock (Detection + Wait-For Graph)
 8. Recover from deadlock (Process Termination)
 0. Exit
==============================================================="""


def main():
    system = None
    while True:
        print(MENU)
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice == "1":
            system = enter_data()
            err = system.validate()
            print(err or "\nData saved.")
            continue
        if choice == "2":
            system = sample_safe()
            print("\nSafe sample data loaded.")
            continue
        if choice == "3":
            system = sample_deadlock()
            print("\nDeadlock sample data loaded.")
            continue
        if choice not in {"4", "5", "6", "7", "8"}:
            print("\nInvalid option, please try again.")
            continue
        if system is None:
            print("\nPlease enter data or load a sample first (option 1, 2 or 3).")
            continue

        if choice == "4":
            show_state(system)

        elif choice == "5":
            safe, seq = system.is_safe()
            if safe:
                print("\nSystem is SAFE. Safe sequence: "
                      + " -> ".join(f"P{i}" for i in seq))
            else:
                print("\nSystem is UNSAFE, there is a risk of deadlock!")

        elif choice == "6":
            pid = read_int(f"\nProcess number (0-{system.n - 1}): ", 0, system.n - 1)
            req = read_vector(f"P{pid} request [{system.m} values]: ", system.m)
            ok, msg = system.request_resources(pid, req)
            print(("\n[OK] " if ok else "\n[NO] ") + msg)

        elif choice == "7":
            deadlocked = system.detect_deadlock()
            if deadlocked:
                print("\nDEADLOCK detected! Deadlocked processes: "
                      + ", ".join(f"P{p}" for p in deadlocked))
            else:
                print("\nNo deadlock detected.")
            graph = system.wait_for_graph()
            print("\nWait-For Graph:")
            for p, targets in graph.items():
                waits = ", ".join(f"P{t}" for t in targets) or "-"
                print(f"  P{p} waits for -> {waits}")
            cycle = system.find_cycle(graph)
            if cycle:
                print("Cycle found: " + " -> ".join(f"P{p}" for p in cycle))
            else:
                print("No cycle found in the graph.")

        elif choice == "8":
            if not system.detect_deadlock():
                print("\nNo deadlock in the system, recovery is not needed.")
            else:
                for line in system.recover():
                    print("  " + line)
                print("\nDeadlock resolved. New state:")
                show_state(system)


if __name__ == "__main__":
    main()
