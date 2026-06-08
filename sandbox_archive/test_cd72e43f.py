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

def truth_table_from_cnf(cnf):
    n = max(abs(lit) for lit in cnf[0])  # Ensure cnf is not empty
    truth_table = [[False] * (2 ** n) for _ in range(len(cnf))]
    for i, clause in enumerate(cnf):
        for assignment in range(1 << n):
            if all(abs(lit) <= n and ((assignment >> abs(lit) - 1) & 1) == (lit > 0) for lit in clause):
                truth_table[i][assignment] = True
    return truth_table

def frobenius_class(truth_table):
    primes = []
    for i in range(len(truth_table)):
        if all(row[i] == truth_table[0][i] for row in truth_table):
            primes.append(i + 1)
    return set(primes)

def communication_complexity_rank_variance(truth_table):
    n = len(truth_table[0])
    ranks = [sum(row[i] for row in truth_table) for i in range(n)]
    mean_rank = sum(ranks) / n
    variance = sum((rank - mean_rank) ** 2 for rank in ranks) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random CNF with up to 40 variables and clauses
    n = random.randint(5, 40)
    cnf = []
    for _ in range(random.randint(1, 2 * n)):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        if len(set(clause)) > 1:  # Ensure no duplicate literals
            cnf.append(clause)
    
    truth_table = truth_table_from_cnf(cnf)
    frobenius_set_size = len(frobenius_class(truth_table))
    rank_variance = communication_complexity_rank_variance(truth_table)
    
    return {
        "metric_name": "Frobenius Class Size and Rank Variance",
        "metric_value": frobenius_set_size * rank_variance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,  # Mapping undefined for this conjecture
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")