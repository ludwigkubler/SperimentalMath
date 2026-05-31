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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_curve(f):
        q = 2
        n = len(f)
        T_f = []
        for i in range(2**n):
            x = bin(i)[2:].zfill(n)
            y = bin(sum(x[j] * f[i ^ (1 << j)] for j in range(n)))[2:].zfill(n)
            T_f.append((x, y))
        return T_f
    
    def compute_minimal_local_index(T_f):
        mli = 0
        for x, y in T_f:
            mli += sum(1 for i in range(len(x)) if x[i] != y[i])
        return mli / len(T_f)
    
    def compute_communication_complexity(f):
        n = len(f)
        C_f = 0
        for i in range(2**n):
            x = bin(i)[2:].zfill(n)
            y = bin(sum(x[j] * f[i ^ (1 << j)] for j in range(n)))[2:].zfill(n)
            C_f += sum(1 for i in range(len(x)) if x[i] != y[i])
        return C_f / len(T_f)
    
    n_max = 40
    instances_tested = 30
    
    results = []
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        T_f = compute_tropical_curve(f)
        mli = compute_minimal_local_index(T_f)
        C_f = compute_communication_complexity(f)
        
        results.append({
            "n": n,
            "mli": mli,
            "C_f": C_f
        })
    
    mean_mli = sum(result["mli"] for result in results) / len(results)
    mean_C_f = sum(result["C_f"] for result in results) / len(results)
    support_fraction = sum(abs(result["mli"] - result["C_f"]) <= 3 for result in results) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mli_vs_Cf",
        "metric_value": mean_mli,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_mli = sum(result["metric_value"] for result in results) / len(results)
    std_mli = math.sqrt(sum((result["metric_value"] - mean_mli)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_mli} std={std_mli} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - result["instances_tested"]) > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - result["instances_tested"]) > 10)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support n_tested={len(results)}")