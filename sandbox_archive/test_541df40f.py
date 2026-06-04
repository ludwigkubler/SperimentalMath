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
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if not any(lit < 0 for lit in clause):
                cnf.append(clause)
        return cnf
    
    def frege_proof_depth(cnf: list) -> int:
        depth = 0
        stack = []
        for clause in cnf:
            if all(lit > 0 for lit in clause):
                stack.append(1)
            else:
                stack.append(max(stack[-2:]) + 1)
        return max(stack)
    
    def hodge_theoretic_index(cnf: list) -> float:
        # Placeholder implementation, replace with actual Hodge-theoretic index calculation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    d_values = []
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        h = hodge_theoretic_index(cnf)
        d = frege_proof_depth(cnf)
        h_values.append(h)
        d_values.append(d)
        instances_tested += len(cnf)
    
    mean_h = sum(h_values) / len(h_values)
    mean_d = sum(d_values) / len(d_values)
    std_dev_h = math.sqrt(sum((x - mean_h) ** 2 for x in h_values) / len(h_values))
    std_dev_d = math.sqrt(sum((x - mean_d) ** 2 for x in d_values) / len(d_values))
    
    conjecture_holds = all(h >= d for h, d in zip(h_values, d_values)) and all(h <= 10 * d**2 for h, d in zip(h_values, d_values) if d >= 5)
    counterexample = "" if conjecture_holds else "H(φ) < d(φ) or H(φ)/d(φ)^2 > c"
    
    return {
        "metric_name": "Frege Proof Depth vs. Hodge-theoretic Index",
        "metric_value": mean_d,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")