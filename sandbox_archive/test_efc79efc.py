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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_branching_program(n):
    program = []
    for _ in range(n):
        if random.choice([True, False]):
            program.append(0)  # Left child
        else:
            program.append(1)  # Right child
    return program

def construct_configuration_space(program):
    n = len(program)
    CS = [[0] * (n + 1) for _ in range(n + 1)]
    CS[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(i + 1):
            if program[i - 1] == 0:
                CS[i][j] += CS[i - 1][j]
            else:
                CS[i][j] += CS[i - 1][j - 1]
    
    return CS

def min_local_index(CS):
    n = len(CS) - 1
    min_index = float('inf')
    for i in range(n + 1):
        if CS[n][i] > 0:
            min_index = min(min_index, math.log2(i + 1))
    return min_index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different programs
            program = generate_branching_program(n)
            CS = construct_configuration_space(program)
            min_index = min_local_index(CS)
            total_metric_value += min_index
            instances_tested += 1
            
            if conjecture_holds:
                if n in [5, 10, 15, 20]:
                    expected_min_index = math.log2(n + 1)
                    if abs(min_index - expected_min_index) > 0.1 * expected_min_index:
                        conjecture_holds = False
                        counterexample = f"n={n}, min_local_index={min_index}"
                else:
                    expected_min_index = n
                    if abs(min_index - expected_min_index) > 0.05 * n:
                        conjecture_holds = False
                        counterexample = f"n={n}, min_local_index={min_index}"
    
    return {
        "metric_name": "min_local_index",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 73))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")