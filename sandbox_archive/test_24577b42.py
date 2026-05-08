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

def duval_factorization(s):
    n = len(s)
    i, j, k = 0, 0, 1
    factors = []
    while i < n:
        if s[i] == s[j]:
            k += 1
        else:
            if k > 1:
                factors.append(k)
            i += k
            j = i
            k = 1
    if k > 0:
        factors.append(k)
    return factors

def popcount(x):
    count = 0
    while x:
        count += x & 1
        x >>= 1
    return count

def generate_and_gate(literals):
    return all(lit for lit in literals)

def generate_depth2_acc0_circuit(n):
    and_gates = []
    for _ in range(n**2):
        literals = [random.choice([f"x{i}", f"not x{i}"]) for i in range(1, math.ceil(math.log2(n)) + 3)]
        and_gates.append(generate_and_gate(literals))
    return and_gates

def generate_mod_3_n(n):
    return lambda x: popcount(x) % 3 == 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12]
    results = []
    
    for n in n_values:
        circuit = generate_depth2_acc0_circuit(n)
        tt_circuit = [circuit[i] for i in range(2**n)]
        lyndon_count_circuit = sum(len(factors) for factors in duval_factorization(''.join(str(int(bit)) for bit in tt_circuit)))
        
        mod_3_n = generate_mod_3_n(n)
        tt_mod_3_n = [mod_3_n(i) for i in range(2**n)]
        lyndon_count_mod_3_n = sum(len(factors) for factors in duval_factorization(''.join(str(int(bit)) for bit in tt_mod_3_n)))
        
        results.append({
            "n": n,
            "lyndon_count_circuit": lyndon_count_circuit,
            "lyndon_count_mod_3_n": lyndon_count_mod_3_n
        })
    
    mean_lyndon_count_circuit = sum(result["lyndon_count_circuit"] for result in results) / len(results)
    mean_lyndon_count_mod_3_n = sum(result["lyndon_count_mod_3_n"] for result in results) / len(results)
    support_fraction = all(result["lyndon_count_circuit"] <= 2**n / math.sqrt(n) and result["lyndon_count_mod_3_n"] >= 2**n / 8 for n, _, _ in results)
    
    conjecture_holds = support_fraction
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Lyndon Factor Count",
        "metric_value": mean_lyndon_count_circuit,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")