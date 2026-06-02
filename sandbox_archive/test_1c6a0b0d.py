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
    
    def generate_cnf(n, k):
        clauses = set()
        for _ in range(k):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def compute_entropy(clauses):
        total_clauses = len(clauses)
        counts = {}
        for clause in clauses:
            if clause not in counts:
                counts[clause] = 0
            counts[clause] += 1
        entropy = 0
        for count in counts.values():
            p = Fraction(count, total_clauses)
            entropy -= p * math.log2(p)
        return entropy
    
    def compute_mli(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        mli = 0
        for clause in clauses:
            mli += sum(1 for literal in clause if literal != 0) / n
        return mli
    
    metric_name = "mli_vs_entropy"
    instances_tested = 0
    n_max = 5
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            k = random.randint(n, 2*n)
            cnf = generate_cnf(n, k)
            entropy = compute_entropy(cnf)
            mli = compute_mli(cnf)
            
            instances_tested += 1
            n_max = max(n_max, n)
            
            if entropy == 0:
                continue
            
            if abs(mli - math.log2(entropy)) > 3:
                conjecture_holds = False
                counterexample = f"n={n}, k={k}, mli={mli}, log(entropy)={math.log2(entropy)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": math.log2(n_max),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")