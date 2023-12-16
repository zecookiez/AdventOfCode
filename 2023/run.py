import solutions
from solutions import *
from time import time

sol_methods = []
for name in solutions.__all__:
    sol_methods.append(locals()[name])

def run_all(verbose = False):
    start_time = time()
    times = []
    for day, method in enumerate(sol_methods, 1):
        t0 = time()
        p1, p2 = method.main(".")
        t1 = time()
        if verbose:
            print(f"DAY: {day}")
            print(f"PART 1: {p1}")
            print(f"PART 2: {p2}")
            print(f"TIME: {t1 - t0}\n")
        else:
            print(f"DAY: {day:02} | TIME: {1000 * (t1 - t0):.2f}ms")
        times.append((1000 * (t1 - t0), day))
    print(f"TOTAL TIME (with logging): {1000 * (time() - start_time):.2f}ms\n")
    times.sort(reverse = True)
    print("Days with the most time:")
    for elapsed, day in times:
        print(f"DAY: {day:02} | TIME: {elapsed:.2f}ms")

if __name__ == "__main__":
    run_all()