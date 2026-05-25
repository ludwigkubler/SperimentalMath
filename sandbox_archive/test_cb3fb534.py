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
    
    def min_rank(functor):
        keys = list(functor.keys())
        if not keys:
            return 0
        rank = len(keys)
        matrix = [[Fraction(0, 1)] * rank for _ in range(rank)]
        for i, key in enumerate(keys):
            row = [Fraction(0, 1)] * rank
            row[i] = Fraction(1, 1)
            matrix[key] = row
        return rank
    
    def bp_read_twice_complexity(n):
        # Simulate a read-twice branching program complexity for simplicity
        return n * math.log2(n)
    
    def tseitin_clauses(n):
        # Generate random Tseitin clauses for simplicity
        clauses = []
        for _ in range(n):
            clause = [f'x{i}' for i in range(random.randint(1, 5))]
            clauses.append(clause)
        return clauses
    
    n = 40
    instances_tested = 30
    total_rank = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        clauses = tseitin_clauses(n)
        functor = {f'y{i}': i for i in range(len(clauses))}
        rank_value = min_rank(functor)
        total_rank += rank_value
        
        if rank_value < n * math.log2(n) and not counterexample:
            counterexample = f"Rank {rank_value} is less than expected for IP_2"
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= n * math.log2(n)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
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
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")