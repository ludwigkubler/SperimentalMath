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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def symplectic_leaf_count(clauses):
        leaves = set()
        for clause in clauses:
            leaves.update(abs(lit) for lit in clause)
        return len(leaves)
    
    def rank_variance(clauses):
        n = len(set(abs(lit) for lit in sum(clauses, [])))
        if n < 2:
            return 0
        mean = sum(len(clause) for clause in clauses) / n
        variance = sum((len(clause) - mean) ** 2 for clause in clauses) / (n - 1)
        return variance
    
    instances_tested = 0
    total_symplectic_leaves_count = 0
    total_rank_variance = 0
    n_max = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        k = random.randint(1, min(n * (n - 1) // 2, 10))
        clauses = generate_kcnf(n, k)
        symplectic_leaves_count = symplectic_leaf_count(clauses)
        rank_variance_value = rank_variance(clauses)
        
        instances_tested += 1
        total_symplectic_leaves_count += symplectic_leaves_count
        total_rank_variance += rank_variance_value
        
        n_max = max(n_max, n)
    
    mean_symplectic_leaves_count = total_symplectic_leaves_count / instances_tested
    mean_rank_variance = total_rank_variance / instances_tested
    
    correlation_coefficient = (instances_tested * sum(s * r for s, r in zip(total_symplectic_leaves_count, total_rank_variance)) -
                               sum(total_symplectic_leaves_count) * sum(total_rank_variance)) / \
                              math.sqrt((instances_tested * sum(s ** 2 for s in total_symplectic_leaves_count) - sum(total_symplectic_leaves_count) ** 2) *
                                        (instances_tested * sum(r ** 2 for r in total_rank_variance) - sum(total_rank_variance) ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.5
    counterexample = f"Correlation coefficient {correlation_coefficient} is less than 0.5" if not conjecture_holds else ""
    
    return {
        "metric_name": "SymplecticLeavesCount * RankVariance",
        "metric_value": mean_symplectic_leaves_count * mean_rank_variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")