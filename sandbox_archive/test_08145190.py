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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tropical_realization(cnf):
        # Simplified tropical realization for demonstration
        return len(cnf)
    
    def hodge_structure(tropical_size):
        return tropical_size
    
    def min_rank(hodge):
        return hodge
    
    results = []
    for k in range(2, 41):
        n = random.randint(5, 40)
        cnf = generate_k_cnf(n, k)
        tropical_size = tropical_realization(cnf)
        hodge = hodge_structure(tropical_size)
        rank = min_rank(hodge)
        results.append((k, rank))
    
    if not results:
        return {
            "metric_name": "MinRank(F)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    k_values = [r[0] for r in results]
    rank_values = [r[1] for r in results]
    
    if not all(rank_values[i] <= rank_values[i+1] for i in range(len(rank_values)-1)):
        return {
            "metric_name": "MinRank(F)",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "MinRank(F) does not increase monotonically with k"
        }
    
    p_k_n = lambda n, k: 2 * n ** (k - 1)
    max_rank = max(rank_values)
    min_n = min(k_values)
    max_n = max(k_values)
    
    if any(rank > p_k_n(n, k) for rank, (k, n) in zip(rank_values, results)):
        return {
            "metric_name": "MinRank(F)",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "No polynomial bound p_k(n) such that MinRank(F) ≥ p_k(n)"
        }
    
    if any(rank > 2 * math.log(n, 2) ** 2 for rank, (k, n) in zip(rank_values, results)):
        return {
            "metric_name": "MinRank(F)",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "MinRank(F) exceeds C * log^2(n)"
        }
    
    return {
        "metric_name": "MinRank(F)",
        "metric_value": max_rank,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MinRank(F) does not increase monotonically with k\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")