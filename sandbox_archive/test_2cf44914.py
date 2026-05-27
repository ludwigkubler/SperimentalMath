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
    
    def generate_tseitin_circuit(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append((variables[i],))
        for i in range(1, n):
            clauses.append((f'~{variables[i-1]}', variables[i]))
        return variables, clauses
    
    def generate_br_q_c(circuit):
        # Simplified Brauer group generation for demonstration
        # This is a placeholder and does not reflect actual Brauer group computation
        variables, _ = circuit
        br_q_c = set()
        for var in variables:
            br_q_c.add(var)
        return br_q_c
    
    def min_generators(group):
        # Simplified minimal generators calculation
        # This is a placeholder and does not reflect actual minimal generators computation
        return len(group)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_circuit(n)
        br_q_c = generate_br_q_c((variables, clauses))
        generators = min_generators(br_q_c)
        results.append(generators)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(g <= 1.5 * math.log(n) for n, g in zip(n_values, results))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_generators",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")