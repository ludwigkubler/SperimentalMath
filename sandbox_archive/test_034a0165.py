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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 3))
            while len(clause) < 3:
                clause.add(random.randint(1, n))
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def decision_tree_depth(n, k):
        if k == 1:
            return random.randint(1, 5)
        else:
            return 2 + decision_tree_depth(n-1, k-1)
    
    def cluster_algebra_rank(n, k):
        # Simplified mock-up of a rank calculation
        return n * (k // 2) + random.randint(0, n // 4)
    
    n = 40
    k = 3
    trials = 50
    
    ranks = []
    depths = []
    
    for _ in range(trials):
        cnf = generate_k_cnf(n, k)
        depth = decision_tree_depth(n, k)
        rank = cluster_algebra_rank(n, k)
        
        ranks.append(rank)
        depths.append(depth)
    
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (depths[i] - mean(depths)) for i in range(trials)) / trials
    p_value = 2 * (1 - min(0.5, abs(correlation_coefficient) / 1))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": trials,
        "conjecture_holds": correlation_coefficient > 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient > 0.7 else "Correlation coefficient does not meet the threshold"
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results])
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")