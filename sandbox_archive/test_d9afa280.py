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

def golden_ratio_rotation_discrepancy(truth_table, phi):
    n = len(truth_table)
    max_disc = 0
    s_N = 0
    for i in range(n):
        s_N += (-1) ** truth_table[i] * math.exp(2j * math.pi * phi * i)
        disc = abs(s_N) / math.sqrt(i + 1)
        if disc > max_disc:
            max_disc = disc
    return max_disc

def generate_truth_table(func, n):
    return [func(i) for i in range(2**n)]

def parity(x):
    return sum(int(bit) for bit in bin(x)[2:]) % 2

def mod_3(x):
    return x % 3

def majority(x):
    bits = bin(x)[2:].zfill(10)
    return sum(int(bit) > 5 for bit in bits)

def and_of_or_tribes(x):
    n = len(bin(x)[2:])
    tribes = [x >> i & ((1 << (n - i)) - 1) for i in range(n)]
    return all(any(tribe & (1 << j) for j in range(n)) for tribe in tribes)

def beatty_function(x, phi):
    return int(phi * x) % 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 14, 18, 20]
    results = []
    
    for n in n_values:
        f_phi = generate_truth_table(lambda x: beatty_function(x, (math.sqrt(5) - 1) / 2), n)
        parity_n = generate_truth_table(parity, n)
        mod_3_n = generate_truth_table(mod_3, n)
        majority_n = generate_truth_table(majority, n)
        and_of_or_tribes_n = generate_truth_table(and_of_or_tribes, n)
        uniform_random = [random.randint(0, 1) for _ in range(2**n)]
        
        f_phi_disc = golden_ratio_rotation_discrepancy(f_phi, (math.sqrt(5) - 1) / 2)
        parity_n_disc = golden_ratio_rotation_discrepancy(parity_n, (math.sqrt(5) - 1) / 2)
        mod_3_n_disc = golden_ratio_rotation_discrepancy(mod_3_n, (math.sqrt(5) - 1) / 2)
        majority_n_disc = golden_ratio_rotation_discrepancy(majority_n, (math.sqrt(5) - 1) / 2)
        and_of_or_tribes_n_disc = golden_ratio_rotation_discrepancy(and_of_or_tribes_n, (math.sqrt(5) - 1) / 2)
        uniform_random_disc = golden_ratio_rotation_discrepancy(uniform_random, (math.sqrt(5) - 1) / 2)
        
        results.append({
            "n": n,
            "f_phi_disc": f_phi_disc,
            "parity_n_disc": parity_n_disc,
            "mod_3_n_disc": mod_3_n_disc,
            "majority_n_disc": majority_n_disc,
            "and_of_or_tribes_n_disc": and_of_or_tribes_n_disc,
            "uniform_random_disc": uniform_random_disc
        })
    
    total_disc = sum(result["f_phi_disc"] for result in results)
    avg_disc = total_disc / len(results)
    std_dev = math.sqrt(sum((result["f_phi_disc"] - avg_disc) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["f_phi_disc"] >= 20 * median_disc and result["parity_n_disc"] <= n**2 and result["mod_3_n_disc"] <= n**2 and result["majority_n_disc"] <= n**2 and result["and_of_or_tribes_n_disc"] <= n**2 for result in results)
    counterexample = "" if conjecture_holds else "f_phi_disc < 4.47 or ACC^0 candidate exceeds 8000"
    
    return {
        "metric_name": "Golden-Ratio Rotation Discrepancy",
        "metric_value": avg_disc,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    avg_disc = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_disc) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_disc} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f_phi_disc < 4.47 or ACC^0 candidate exceeds 8000\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")