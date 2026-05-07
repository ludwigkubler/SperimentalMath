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

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if (exp % 2) == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def generate_truth_table(n, depth, size):
    inputs = [i for i in range(2**n)]
    gates = []
    for _ in range(size):
        gate_type = random.choice(['AND', 'OR'])
        if gate_type == 'AND':
            a, b = random.sample(inputs, 2)
            gates.append((a, b, lambda x, y: x & y))
        else:
            a, b = random.sample(inputs, 2)
            gates.append((a, b, lambda x, y: x | y))
    return inputs, gates

def compute_A_f(truth_table):
    A_f = set()
    for input_val in truth_table:
        if input_val == 1:
            A_f.add(input_val)
    return A_f

def count_3AP(A_f, n):
    count = 0
    for x in A_f:
        for z in A_f:
            y = (x + z) // 2
            if (x + z) % 2 == 0 and y in A_f:
                count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14]
    results = []
    
    for n in n_values:
        inputs, gates = generate_truth_table(n, 3, n**2)
        A_f = compute_A_f(inputs)
        R_3 = count_3AP(A_f, n) * (2**n) / max(len(A_f)**3, 1)
        
        if len(gates) > 0:
            results.append(R_3)
    
    min_ACC0_R3 = min(results) if results else float('inf')
    S_n_fan_in = math.ceil(n**(1/3))
    S_n_truth_table = [i for i in range(2**n)]
    S_n_A_f = set()
    for i in range(S_n_fan_in):
        S_n_A_f.update([j for j in range(2**n) if (j & (1 << i)) == 0])
    R_3_S_n = count_3AP(S_n_A_f, n) * (2**n) / max(len(S_n_A_f)**3, 1)
    
    conjecture_holds = min_ACC0_R3 >= 0.8 and R_3_S_n <= 0.6
    counterexample = "" if conjecture_holds else "min ACC⁰ R₃ < 0.8 or Sipser R₃ > 0.6"
    
    return {
        "metric_name": "R₃",
        "metric_value": min_ACC0_R3,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_R3 = sum(results) / len(results)
    std_R3 = math.sqrt(sum((x - mean_R3)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_R3} std={std_R3} support_fraction={support_fraction}")
    elif any(r < 0.8 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"min ACC⁰ R₃ < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE min_Sipser_R₃ > 0.6")