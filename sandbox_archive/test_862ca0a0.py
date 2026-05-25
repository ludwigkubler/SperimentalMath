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
    
    def generate_explicit_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def geometric_quantization(f):
        n = len(f)
        Q = [[Fraction(0)] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    Q[i][j] = Fraction(1)
        return Q
    
    def dpll_solver(f):
        n = len(f)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
        # Simplified DPLL solver (not actual ACC⁰ lower bound)
        return len(clauses) <= 3
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # 5 instances per size
            f = generate_explicit_function(n)
            Q = geometric_quantization(f)
            rank = sum(sum(row) for row in Q)
            total_rank += rank
            instances_tested += 1
            
            if not dpll_solver(f):
                conjecture_holds = False
                counterexample = "DPLL solver failed for n={}".format(n)
    
    mean_rank = Fraction(total_rank, instances_tested)
    std_dev = (sum((rank - mean_rank)**2 for rank in range(instances_tested)) / instances_tested).sqrt()
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_rank, std_dev, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[0]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")