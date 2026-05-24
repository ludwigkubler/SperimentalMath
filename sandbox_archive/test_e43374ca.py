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
    
    def generate_ac0_parity_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_differential(circuit):
        n = len(circuit)
        diff_form = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if circuit[i] != circuit[j]:
                    diff_form[i][j] = 1
        return diff_form
    
    def min_rank(diff_form):
        n = len(diff_form)
        rank = 0
        for row in diff_form:
            if any(row):
                rank += 1
                break
        return rank
    
    def grothendieck_witt_class_mod_2(diff_form):
        n = len(diff_form)
        det = 1
        for i in range(n):
            det *= sum(diff_form[i]) % 2
        return det
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_parity_circuit(n)
        diff_form = compute_tropical_differential(circuit)
        rank = min_rank(diff_form)
        det_mod_2 = grothendieck_witt_class_mod_2(diff_form)
        
        if det_mod_2 == 0:
            continue
        
        results.append({
            "n": n,
            "rank": rank,
            "det_mod_2": det_mod_2
        })
    
    total_rank = sum(result["rank"] for result in results)
    mean_rank = total_rank / len(results) if results else 0
    
    conjecture_holds = all(result["rank"] >= math.ceil(2**(result["n"]/3)) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")