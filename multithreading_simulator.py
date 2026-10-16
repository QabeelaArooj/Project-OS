"""
Multithreading Module Simulator
===============================
Console based project that demonstrates the core ideas of multithreading:
  1. Thread creation        -> start / join, sequential vs multithreaded time
  2. Race condition         -> shared counter without a lock vs with a Lock
  3. Producer-Consumer      -> bounded buffer using Semaphores + Lock
  4. Thread pool            -> ThreadPoolExecutor with 1 worker vs many workers
  5. Deadlock with threads  -> opposite lock order (timeout detects it) vs
                               a fixed global lock order (deadlock avoided)

Run:  python multithreading_simulator.py
"""

import threading
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor

print_lock = threading.Lock()


def log(msg):
    """Thread-safe print so lines from different threads do not mix."""
    with print_lock:
        print(msg)


# ---------------------------------------------------------------
# 1. THREAD CREATION
# ---------------------------------------------------------------
def _task(name, duration):
    log(f"  [{name}] started")
    time.sleep(duration)
    log(f"  [{name}] finished")


def demo_basic_threads(n, duration):
    print("\n--- Sequential run (one task after another) ---")
    t0 = time.perf_counter()
    for i in range(n):
        _task(f"Task-{i + 1}", duration)
    sequential = time.perf_counter() - t0

    print("\n--- Multithreaded run (all tasks at the same time) ---")
    threads = [threading.Thread(target=_task, args=(f"Thread-{i + 1}", duration))
               for i in range(n)]
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()                      # wait for every thread to finish
    threaded = time.perf_counter() - t0

    print(f"\nSequential : {sequential:.2f}s")
    print(f"Threaded   : {threaded:.2f}s")
    print(f"Speedup    : {sequential / threaded:.1f}x")
    return sequential, threaded


# ---------------------------------------------------------------
# 2. RACE CONDITION
# ---------------------------------------------------------------
def run_counter(n_threads, increments, use_lock):
    """Every thread adds 1 to a shared counter `increments` times.
    time.sleep(0) sits between the read and the write so that a thread
    switch can happen there, which makes the race easy to see."""
    counter = 0
    lock = threading.Lock()

    def work():
        nonlocal counter
        for _ in range(increments):
            if use_lock:
                with lock:                 # critical section protected
                    tmp = counter
                    time.sleep(0)
                    counter = tmp + 1
            else:                          # critical section NOT protected
                tmp = counter
                time.sleep(0)
                counter = tmp + 1

    threads = [threading.Thread(target=work) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter


def demo_race_condition(n_threads, increments):
    expected = n_threads * increments
    unsafe = run_counter(n_threads, increments, use_lock=False)
    safe = run_counter(n_threads, increments, use_lock=True)

    print(f"\nExpected final value : {expected}")
    print(f"WITHOUT lock         : {unsafe}   "
          + ("<- WRONG, updates were lost (race condition)"
             if unsafe != expected else "(no loss this time, run again)"))
    print(f"WITH lock            : {safe}   "
          + ("<- correct" if safe == expected else "<- unexpected!"))
    return expected, unsafe, safe


# ---------------------------------------------------------------
# 3. PRODUCER-CONSUMER (bounded buffer)
# ---------------------------------------------------------------
def demo_producer_consumer(n_prod, n_cons, items_each, capacity):
    buffer = deque()
    empty = threading.Semaphore(capacity)   # free slots in the buffer
    full = threading.Semaphore(0)           # filled slots in the buffer
    mutex = threading.Lock()                # protects the buffer itself
    stats = {"max_size": 0, "consumed": 0}

    def put(item):
        empty.acquire()                     # wait for a free slot
        with mutex:
            buffer.append(item)
            stats["max_size"] = max(stats["max_size"], len(buffer))
        full.release()                      # signal: one more item

    def producer(pid):
        for k in range(items_each):
            item = f"P{pid}-item{k + 1}"
            log(f"  Producer {pid} produced {item}")
            put(item)
            time.sleep(0.05)

    def consumer(cid):
        while True:
            full.acquire()                  # wait for an item
            with mutex:
                item = buffer.popleft()
            empty.release()                 # signal: one more free slot
            if item is None:                # sentinel: no more work
                break
            with mutex:
                stats["consumed"] += 1
            log(f"  Consumer {cid} consumed {item}")
            time.sleep(0.08)

    producers = [threading.Thread(target=producer, args=(i + 1,)) for i in range(n_prod)]
    consumers = [threading.Thread(target=consumer, args=(i + 1,)) for i in range(n_cons)]
    for t in consumers + producers:
        t.start()
    for t in producers:
        t.join()
    for _ in consumers:                     # one stop signal per consumer
        put(None)
    for t in consumers:
        t.join()

    produced = n_prod * items_each
    print(f"\nProduced : {produced}")
    print(f"Consumed : {stats['consumed']}")
    print(f"Buffer capacity {capacity}, largest size reached {stats['max_size']} "
          f"(never above the capacity)")
    return produced, stats["consumed"], stats["max_size"]


# ---------------------------------------------------------------
# 4. THREAD POOL
# ---------------------------------------------------------------
def _fetch(i, delay):
    time.sleep(delay)                       # simulates a slow I/O job
    return i, i * i


def run_pool(workers, tasks, delay):
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda i: _fetch(i, delay), range(1, tasks + 1)))
    return results, time.perf_counter() - t0


def demo_thread_pool(tasks, workers, delay=0.2):
    _, one = run_pool(1, tasks, delay)
    results, many = run_pool(workers, tasks, delay)
    print(f"\n{tasks} simulated I/O tasks, {delay}s each")
    print(f"1 worker       : {one:.2f}s")
    print(f"{workers} workers      : {many:.2f}s   (speedup {one / many:.1f}x)")
    print("Results (task -> square): "
          + ", ".join(f"{i}->{sq}" for i, sq in results))
    return one, many, results


# ---------------------------------------------------------------
# 5. DEADLOCK WITH THREADS
# ---------------------------------------------------------------
def lock_demo(ordered):
    """ordered=False: T1 takes A then B, T2 takes B then A  -> deadlock.
    ordered=True : both threads take A then B               -> no deadlock.
    acquire(timeout=...) is used so the demo can report the deadlock
    instead of hanging forever."""
    lock_a, lock_b = threading.Lock(), threading.Lock()
    barrier = threading.Barrier(2)          # makes both hold their first lock
    outcome = {}

    def task(name, first, second, sync):
        (first_name, first_lock), (second_name, second_lock) = first, second
        first_lock.acquire()
        log(f"  {name} holds lock {first_name}")
        if sync:
            barrier.wait()
        time.sleep(0.1)
        log(f"  {name} wants lock {second_name}")
        if second_lock.acquire(timeout=1.0):
            log(f"  {name} got lock {second_name}, work done")
            second_lock.release()
            outcome[name] = True
        else:
            log(f"  {name} TIMED OUT waiting for {second_name} -> DEADLOCK")
            outcome[name] = False
        first_lock.release()

    A, B = ("A", lock_a), ("B", lock_b)
    if ordered:
        t1 = threading.Thread(target=task, args=("T1", A, B, False))
        t2 = threading.Thread(target=task, args=("T2", A, B, False))
    else:
        t1 = threading.Thread(target=task, args=("T1", A, B, True))
        t2 = threading.Thread(target=task, args=("T2", B, A, True))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return all(outcome.values())


def demo_deadlock():
    print("\n--- Opposite lock order (T1: A then B, T2: B then A) ---")
    bad = lock_demo(ordered=False)
    print("\n--- Same lock order (both: A then B) ---")
    good = lock_demo(ordered=True)
    print("\nResult: opposite order -> "
          + ("no deadlock" if bad else "DEADLOCK")
          + " | same order -> "
          + ("no deadlock" if good else "DEADLOCK"))
    print("Rule: always take locks in one fixed global order.")
    return bad, good


# ======================= CONSOLE UI =======================

def read_int(prompt, default, low, high):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            value = int(raw)
            if low <= value <= high:
                return value
        except ValueError:
            pass
        print(f"  Invalid input. Enter a number from {low} to {high}, "
              f"or press Enter for {default}.")


def read_float(prompt, default, low, high):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            value = float(raw)
            if low <= value <= high:
                return value
        except ValueError:
            pass
        print(f"  Invalid input. Enter a number from {low} to {high}, "
              f"or press Enter for {default}.")


MENU = """
============== MULTITHREADING MODULE SIMULATOR ==============
 1. Thread creation (sequential vs multithreaded)
 2. Race condition (without lock vs with lock)
 3. Producer-Consumer (semaphores)
 4. Thread pool (1 worker vs many workers)
 5. Deadlock with threads (and how to avoid it)
 0. Exit
=============================================================
(Press Enter at any question to use the default value.)"""


def main():
    while True:
        print(MENU)
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            n = read_int("Number of threads", 4, 1, 10)
            d = read_float("Seconds of work per thread", 0.5, 0.1, 2.0)
            demo_basic_threads(n, d)
        elif choice == "2":
            n = read_int("Number of threads", 4, 2, 10)
            inc = read_int("Increments per thread", 1000, 10, 5000)
            demo_race_condition(n, inc)
        elif choice == "3":
            p = read_int("Number of producers", 2, 1, 5)
            c = read_int("Number of consumers", 2, 1, 5)
            k = read_int("Items per producer", 5, 1, 20)
            cap = read_int("Buffer capacity", 3, 1, 10)
            demo_producer_consumer(p, c, k, cap)
        elif choice == "4":
            tasks = read_int("Number of tasks", 8, 1, 30)
            workers = read_int("Number of workers", 4, 2, 10)
            demo_thread_pool(tasks, workers)
        elif choice == "5":
            demo_deadlock()
        else:
            print("\nInvalid option, please try again.")


if __name__ == "__main__":
    main()
