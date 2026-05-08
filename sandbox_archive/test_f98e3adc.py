# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import math
import random
import sys

def golden_ratio_rotation_discrepancy(truth_table, phi):
    n = len(truth_table)
    s_N = 0
    max_disc = 0
    for i in range(n):
        s_N += (-1) ** truth_table[i] * (math.cos(2 * math.pi * phi * i) + 1j * math.sin(2 * math.pi * phi * i))
        max_disc = max(max_disc, abs(s_N) / math.sqrt(i + 1))
    return max_disc

def beatty_function(n):
    phi = (math.sqrt(5) - 1) / 2
    return [int(phi * i) % 2 for i in range(2**n)]

def parity_truth_table(n):
    truth_table = []
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        truth_table.append(int(binary.count('1') % 2))
    return truth_table

def mod_3_truth_table(n):
    truth_table = []
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        sum_bits = sum(int(bit) for bit in binary)
        truth_table.append(sum_bits % 3 == 0)
    return truth_table

def majority_truth_table(n):
    truth_table = []
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        ones_count = binary.count('1')
        truth_table.append(ones_count > n // 2)
    return truth_table

def and_of_or_tribes_truth_table(n):
    truth_table = []
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        ones_count = binary.count('1')
        if ones_count == 0 or ones_count == n:
            truth_table.append(0)
        else:
            truth_table.append(1)
    return truth_table

def uniform_random_truth_table(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 14, 18, 20]
    results = []
    
    f_phi_truth_table = beatty_function(n)
    f_phi_disc = golden_ratio_rotation_discrepancy(f_phi_truth_table, (math.sqrt(5) - 1) / 2)
    results.append({"n": n, "f_phi_disc": f_phi_disc})
    
    for n in n_values:
        truth_tables = {
            "PARITY_n": parity_truth_table(n),
            "MOD_3_n": mod_3_truth_table(n),
            "MAJORITY_n": majority_truth_table(n),
            "AND-of-OR TRIBES_n": and_of_or_tribes_truth_table(n),
            "uniform_random": uniform_random_truth_table(n)
        }
        
        for name, truth_table in truth_tables.items():
            disc = golden_ratio_rotation_discrepancy(truth_table, (math.sqrt(5) - 1) / 2)
            results.append({"n": n, "name": name, "disc": disc})
    
    metric_name = "golden_ratio_rotation_discrepancy"
    metric_value = sum(result["f_phi_disc"] for result in results if "f_phi_disc" in result)
    instances_tested = len(results)
    conjecture_holds = all(result["f_phi_disc"] >= 20 * median_disc for result in results if "f_phi_disc" in result) and \
                       all(result["disc"] <= n**2 for result in results if "name" in result and result["name"].startswith("PARITY") or
                           result["name"].startswith("MOD_3") or result["name"].startswith("MAJORITY") or
                           result["name"].startswith("AND-of-OR TRIBES"))
    counterexample = "" if conjecture_holds else "f_phi_disc < 20 * median_disc"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")