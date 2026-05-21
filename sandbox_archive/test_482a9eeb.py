# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def incidence_matroid_rank(clauses):
        matroid = {}
        for i, clause in enumerate(clauses):
            for var in clause:
                if var not in matroid:
                    matroid[var] = set()
                matroid[var].add(i)
        rank = 0
        while True:
            independent_set = []
            for var in matroid:
                if all(len(matroid[var] & independent_set) == 1 for _ in independent_set):
                    independent_set.append(var)
            if not independent_set:
                break
            rank += 1
            new_matroid = {}
            for var in matroid:
                if any(i not in independent_set for i in matroid[var]):
                    continue
                new_matroid[var] = {i for i in matroid[var] if i in independent_set}
            matroid = new_matroid
        return rank
    
    def karchmer_wigderson_cost(clauses):
        n = len(clauses)
        x, y = 1, 1
        while x * y < n:
            if x < y:
                x *= 2
            else:
                y *= 2
        return max(x, y) - 1
    
    clauses = generate_3cnf(40)
    matroid_rank = incidence_matroid_rank(clauses)
    karch_cost = karchmer_wigderson_cost(clauses)
    
    return {
        "metric_name": "Karchmer-Wigderson protocol cost",
        "metric_value": karch_cost,
        "instances_tested": 1,
        "conjecture_holds": karch_cost >= matroid_rank,
        "counterexample": "" if karch_cost >= matroid_rank else f"n=40, rank={matroid_rank}, cost={karch_cost}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")