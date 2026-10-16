# Multithreading Module Simulator

An Operating Systems project that demonstrates the main ideas of multithreading through a console menu. Every demo runs real Python threads and prints what happens, so the results can be shown live.

## Features

| # | Demo | What it shows |
|---|---|---|
| 1 | Thread creation | `start()` and `join()`, and how much faster independent tasks finish when run as threads |
| 2 | Race condition | A shared counter gives a wrong result without a lock and the correct result with a `Lock` |
| 3 | Producer-Consumer | A bounded buffer shared safely using two `Semaphore`s and a `Lock` |
| 4 | Thread pool | `ThreadPoolExecutor` with 1 worker compared to many workers |
| 5 | Deadlock with threads | Two threads taking locks in opposite order get stuck (detected with a timeout); a fixed lock order avoids it |

## Requirements
- Python 3.8 or newer (standard library only, no external packages)

## How to run
```
python multithreading_simulator.py
```

## Menu
```
1. Thread creation (sequential vs multithreaded)
2. Race condition (without lock vs with lock)
3. Producer-Consumer (semaphores)
4. Thread pool (1 worker vs many workers)
5. Deadlock with threads (and how to avoid it)
0. Exit
```
Press Enter at any question to use the default value.

## Demo steps
1. Option **1**: 4 tasks of 0.5 s take about 2 s one after another and about 0.5 s as threads.
2. Option **2**: without the lock the final count is lower than expected (lost updates); with the lock it is exact.
3. Option **3**: producers and consumers run together; the buffer never goes above its capacity and every produced item is consumed.
4. Option **4**: 8 tasks finish about 4 times faster with 4 workers than with 1.
5. Option **5**: with opposite lock order each thread holds one lock and waits for the other, so a timeout reports DEADLOCK (one thread gives up, which lets the other finish). With the same order for both threads everything finishes normally.

## Concepts in brief
- **Thread:** a unit of execution inside a process. Threads share memory, which is why they are fast to start and also why they need synchronization.
- **Race condition:** the result depends on the timing of threads. Two threads read the same old value, both add 1, and one update is lost.
- **Critical section and Lock (mutex):** the code that touches shared data. A lock lets only one thread inside at a time.
- **Semaphore:** a counter used for signalling. In Producer-Consumer, `empty` counts free slots and `full` counts filled slots, so producers wait when the buffer is full and consumers wait when it is empty.
- **Thread pool:** a fixed set of worker threads that take tasks from a queue, which avoids creating a new thread for every task.
- **Deadlock:** threads wait for each other's locks forever. Fix: always acquire locks in one fixed global order.

## Notes
- The speedups in demos 1 and 4 come from tasks that wait (simulated with `sleep`). In CPython the Global Interpreter Lock (GIL) means threads do not speed up heavy CPU-only calculations; processes are used for that.
- In demo 2, a tiny `time.sleep(0)` is placed between reading and writing the counter to force a thread switch there, so the race condition shows up reliably.

## Files
- `multithreading_simulator.py` - complete source code
- `README_multithreading.md` - this documentation
