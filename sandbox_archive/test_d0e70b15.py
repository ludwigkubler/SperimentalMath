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
    
    def generate_k_sat_instance(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def compute_clause_tree_width(clauses):
        # Simplified heuristic for clause tree width
        return len(set(abs(c) for c in sum(clauses, [])))

    def construct_incidence_algebra(clauses):
        n = max(abs(c) for c in sum(clauses, []))
        algebra = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            x, y = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                algebra[x][y] += 1
                algebra[y][x] += 1
            elif clause[0] < 0 and clause[1] < 0:
                algebra[-x][-y] += 1
                algebra[-y][-x] += 1
        return algebra

    def p_adic_metric_complexity(algebra):
        n = len(algebra) - 1
        if n == 0:
            return 0
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value)

    def measure_correlation(clauses, metric_values):
        if not clauses or not metric_values:
            return 0
        n = len(clauses)
        x_sum = sum(clause_tree_width for clause_tree_width in compute_clause_tree_width(clauses) for _ in range(n))
        y_sum = sum(metric_value for metric_value in metric_values for _ in range(n))
        xy_sum = sum(clause_tree_width * metric_value for clause_tree_width, metric_value in zip(compute_clause_tree_width(clauses), metric_values) for _ in range(n))
        x_squared_sum = sum(clause_tree_width ** 2 for clause_tree_width in compute_clause_tree_width(clauses) for _ in range(n))
        y_squared_sum = sum(metric_value ** 2 for metric_value in metric_values for _ in range(n))
        n_total = n * len(clauses)
        numerator = n_total * xy_sum - x_sum * y_sum
        denominator = math.sqrt((n_total * x_squared_sum - x_sum ** 2) * (n_total * y_squared_sum - y_sum ** 2))
        if denominator == 0:
            return 0
        return numerator / denominator

    n_max = 40
    instances_tested = 30
    p_adic_complexities = []
    clause_tree_widths = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        k = random.randint(1, 2 * n)
        clauses = generate_k_sat_instance(n, k)
        algebra = construct_incidence_algebra(clauses)
        p_adic_complexity = p_adic_metric_complexity(algebra)
        clause_tree_width = compute_clause_tree_width(clauses)

        if p_adic_complexity < 50:
            continue

        p_adic_complexities.append(p_adic_complexity)
        clause_tree_widths.append(clause_tree_width)

    correlation_coefficient = measure_correlation(clause_tree_widths, p_adic_complexities)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else "Correlation coefficient is below threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3**j + 5**k for i, j, k in itertools.product(range(5), range(5), range(5))]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient is below threshold\" first_failing_seed={first_failing_seed}")