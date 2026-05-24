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
    
    def generate_k_cnf(k, n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(k)]
            if sum(clause) == 0:
                clause[random.randint(0, k - 1)] *= -1
            clauses.append(clause)
        return clauses
    
    def tropicalize(cnf):
        rank = len(cnf)
        return rank
    
    def resolution_length(cnf):
        stack = cnf[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(abs(clause[i]) == abs(clause[j]) and clause[i] != clause[j] for clause in stack):
                        new_clause = [abs(clause) for clause in stack if not (abs(clause[i]) == abs(clause[j]) and clause[i] != clause[j])]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    n = random.randint(5, 40)
    k = 3
    cnf = generate_k_cnf(k, n)
    rank = tropicalize(cnf)
    length = resolution_length(cnf)
    
    if rank == 0:
        return {
            "metric_name": "resolution_to_rank_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = length / rank**2
    return {
        "metric_name": "resolution_to_rank_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,
        "counterexample": "" if ratio <= 2 else f"Ratio {ratio} exceeds quadratic bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results)
    std_dev = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")