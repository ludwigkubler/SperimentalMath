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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            if circuit[i] == 1:
                width += 1
        return width
    
    def hodge_structure_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            if circuit[i] == 1:
                rank += 1
        return rank
    
    instances_tested = 0
    total_h = 0
    total_w = 0
    max_n = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(6):
            circuit = generate_circuit(n)
            w = monotone_width(circuit)
            h = hodge_structure_rank(circuit)
            total_h += h
            total_w += w
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_h = Fraction(total_h, instances_tested)
    mean_w = Fraction(total_w, instances_tested)
    correlation_coefficient = (mean_h * mean_w) / (mean_h**2 + mean_w**2)
    
    conjecture_holds = math.sqrt(mean_w**(2/3)) <= correlation_coefficient <= math.sqrt(mean_w)
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient} outside bounds"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": max_n,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")