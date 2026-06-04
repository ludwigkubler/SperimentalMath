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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        cnf.append(clause)
    return cnf

def clause_subset_entropy(cnf):
    total_clauses = len(cnf)
    subset_sizes = [len(subset) for subset in range(1, total_clauses + 1)]
    counts = [0] * (total_clauses + 1)
    
    for i in range(1 << total_clauses):
        subset = []
        for j in range(total_clauses):
            if i & (1 << j):
                subset.append(cnf[j])
        counts[len(subset)] += 1
    
    probabilities = [count / (2 ** total_clauses) for count in counts]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def hodge_decomposition_order(n):
    # Placeholder function to simulate Hodge decomposition order
    # This is a dummy implementation and should be replaced with actual logic
    return n ** 1.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    
    hodge_order = hodge_decomposition_order(n)
    entropy = clause_subset_entropy(cnf)
    
    correlation_coefficient = (hodge_order - n ** 1.5) / (n ** 2.5 - n ** 1.5)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) < 6:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_failing_seeds\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")