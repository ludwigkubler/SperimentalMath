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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def communication_complexity_rank_variance(cnf):
        n = len(cnf[0])
        rank_var = 0
        for i in range(n):
            count = sum(1 for clause in cnf if (i + 1) in clause or -(i + 1) in clause)
            rank_var += count * (n - count)
        return rank_var / n

    def minimal_root_system_length(cnf):
        # Placeholder function to simulate root system length calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)

    instances_tested = 0
    total_L = 0
    total_w = 0
    n_max = 1

    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        L = minimal_root_system_length(cnf)
        w = communication_complexity_rank_variance(cnf)

        if L == 0 or w == 0:
            continue

        instances_tested += 1
        total_L += L
        total_w += w
        n_max = max(n_max, n)

    mean_L = total_L / instances_tested if instances_tested > 0 else 0
    mean_w = total_w / instances_tested if instances_tested > 0 else 0

    correlation_coefficient = (instances_tested * sum(L * w for L, w in zip([mean_L] * instances_tested, [mean_w] * instances_tested)) - 
                              (mean_L * mean_w) * instances_tested) / ((instances_tested - 1) * math.sqrt((mean_L**2 * instances_tested - sum(L**2 for L in [mean_L] * instances_tested)) * 
                                                                                   (mean_w**2 * instances_tested - sum(w**2 for w in [mean_w] * instances_tested))))

    conjecture_holds = 0.8 <= abs(correlation_coefficient) <= 1
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": abs(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient outside [0.8, 1]\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")