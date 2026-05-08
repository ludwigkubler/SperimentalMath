# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_read_twice_branching_program(n):
    program = []
    for i in range(2**n):
        if i % 2 == 0:
            program.append((i, (1, 0)))
        else:
            program.append((i, (0, 1)))
    return program

def generate_read_once_branching_program(n):
    program = []
    for i in range(2**n):
        if i % 2 == 0:
            program.append((i, (1,)))
        else:
            program.append((i, (0,)))
    return program

def fourier_coefficient_sum(program, n):
    sum_coeffs = 0
    for state, (a, b) in program:
        sum_coeffs += abs(a) + abs(b)
    return sum_coeffs

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    ip2_twice = generate_read_twice_branching_program(n)
    ip2_once = generate_read_once_branching_program(n)
    
    ip2_twice_sum = fourier_coefficient_sum(ip2_twice, n)
    ip2_once_sum = fourier_coefficient_sum(ip2_once, n)
    
    metric_name = "Fourier Coefficient Sum"
    metric_value_twice = ip2_twice_sum
    metric_value_once = ip2_once_sum
    
    conjecture_holds_twice = metric_value_twice >= math.sqrt(n)
    conjecture_holds_once = metric_value_once <= math.log(n, 2)
    
    counterexample_twice = "" if conjecture_holds_twice else "read-twice program"
    counterexample_once = "" if conjecture_holds_once else "read-once program"
    
    return {
        "metric_name": metric_name,
        "metric_value": {"twice": metric_value_twice, "once": metric_value_once},
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds_twice and conjecture_holds_once,
        "counterexample": f"read-twice: {counterexample_twice}, read-once: {counterexample_once}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_twice_sum = sum(r["metric_value"]["twice"] for r in results)
    total_once_sum = sum(r["metric_value"]["once"] for r in results)
    mean_twice = total_twice_sum / len(results)
    mean_once = total_once_sum / len(results)
    std_twice = math.sqrt(sum((r["metric_value"]["twice"] - mean_twice) ** 2 for r in results) / len(results))
    std_once = math.sqrt(sum((r["metric_value"]["once"] - mean_once) ** 2 for r in results) / len(results))
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean_twice={mean_twice} std_twice={std_twice} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"read-twice or read-once program\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE support_fraction too low"
    
    print(result)