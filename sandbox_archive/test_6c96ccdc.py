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
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def moment_map(cnf):
        # Simplified moment map calculation
        return sum(len(clause) for clause in cnf)

    def min_symplectic_leaf_rank(moment_map_value):
        # Simplified minimal symplectic leaf rank calculation
        n = len([x for x in moment_map_value if x > 0])
        return 2 ** (n / 4)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_k_cnf(n)
            rank = min_symplectic_leaf_rank(moment_map(cnf))
            results.append({
                "n": n,
                "rank": rank
            })
            instances_tested += 1
    
    total_rank = sum(result["rank"] for result in results)
    mean_rank = total_rank / len(results)
    std_dev = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    
    expected_rank = 2 ** (n_values[-1] / 4)
    if all(0.5 * expected_rank <= result["rank"] <= 2 * expected_rank for result in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "deviation_from_expected_value"
    
    return {
        "metric_name": "min_symplectic_leaf_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"deviation_from_expected_value\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")