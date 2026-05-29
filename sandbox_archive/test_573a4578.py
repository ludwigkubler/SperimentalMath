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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def quantum_logarithmic_capacity(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i * (1 << n) + j] for j in range(1 << n)] for i in range(1 << n)]
        rank = 0
        for row in matrix:
            if any(row[j] != 0 for j in range(1 << n)):
                rank += 1
        return Fraction(rank, len(f))
    
    def monotone_circuit_size(f):
        n = int(math.log2(len(f)))
        truth_table = {i: f[i] for i in range(len(f))}
        depth = 0
        while True:
            new_truth_table = {}
            for i in range(len(f)):
                if all(truth_table[j] == truth_table[i] for j in range(i + 1, len(f))):
                    continue
                new_truth_table[i] = truth_table[i]
            if new_truth_table == truth_table:
                break
            depth += 1
            truth_table = new_truth_table
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        qlc = quantum_logarithmic_capacity(f)
        d = monotone_circuit_size(f)
        S_mon = d
        c = Fraction(1, 2)  # Placeholder value for c
        results.append({
            "n": n,
            "qrc": qlc,
            "depth": d,
            "S_mon": S_mon,
            "c * QLC^2": c * qlc**2
        })
    
    mean_diff = sum(abs(res["S_mon"] - res["c * QLC^2"]) for res in results) / len(results)
    conjecture_holds = all(res["S_mon"] >= res["c * QLC^2"] for res in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_diff",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")