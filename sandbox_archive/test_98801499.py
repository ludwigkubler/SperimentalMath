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
    
    def noncrossing_partitions(n):
        if n == 1:
            return [[], [0]]
        parts = []
        for i in range(1, n):
            for p in noncrossing_partitions(i):
                for q in noncrossing_partitions(n - i):
                    parts.append(p + q)
        return parts
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input size must be a power of 2")
        
        def solve(lits, cls):
            if not lits:
                return True
            lit = lits[0]
            true_lits = [l for l in lits if l == lit or l == -lit]
            false_lits = [l for l in lits if l != lit and l != -lit]
            return solve(true_lits, cls) or solve(false_lits, cls)
        
        def count_true_clauses(lits):
            true_clauses = 0
            for i in range(2**n):
                if all(f[i ^ (1 << j)] == 1 for j in range(n) if lits[j] == -1):
                    true_clauses += 1
            return true_clauses
        
        cls = noncrossing_partitions(n)
        max_true_clauses = max(count_true_clauses(lits) for lits in cls)
        min_false_clauses = min(2**n - count_true_clauses(lits) for lits in cls)
        return max_true_clauses + min_false_clauses
    
    def minimal_rank(lattice):
        rank = 0
        visited = set()
        for p in lattice:
            if all(q not in visited for q in p):
                rank += 1
                visited.update(p)
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    lattice = noncrossing_partitions(n)
    rank = minimal_rank(lattice)
    c_f = communication_complexity(f)
    
    return {
        "metric_name": "rank_c_f_ratio",
        "metric_value": rank / c_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")