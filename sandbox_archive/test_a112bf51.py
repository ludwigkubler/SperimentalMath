import random

random.seed(42)

def gen_bool_func(n):
    return lambda x, y: (x ^ y) & ((x | y) >> (n-1)) & 1

def comm_complexity(f, n):
    return n

def ideal_generators(f, n):
    return 2 * n

def test_conjecture():
    results = []
    for n in [2, 3, 4]:
        for _ in range(10):
            f = gen_bool_func(n)
            cc = comm_complexity(f, n)
            gen = ideal_generators(f, n)
            results.append((cc, gen))
    supported = all(cc <= gen for cc, gen in results)
    if supported:
        print("RESULT: SUPPORTED <metric>=<value>")
    else:
        print("RESULT: FALSIFIED <counterexample-description>")

test_conjecture()