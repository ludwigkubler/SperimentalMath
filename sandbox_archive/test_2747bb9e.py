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
    
    def read_twice_branching_program(width):
        if width == 1:
            return [[0]]
        program = []
        for _ in range(width - 1):
            choices = [random.randint(0, 1) for _ in range(len(program[-1]))]
            new_state = [state + choice for state, choice in zip(program[-1], choices)]
            program.append(new_state)
        return program
    
    def groupoid_cohomology(program):
        n = len(program[0])
        cohomology = 0
        for i in range(n):
            for j in range(i + 1, n):
                if program[0][i] != program[0][j]:
                    cohomology += 1
        return cohomology
    
    def spearman_rank_correlation(x, y):
        x_sorted = sorted(zip(x, y))
        ranks_x = {value: rank for rank, (value, _) in enumerate(x_sorted)}
        ranks_y = {value: rank for rank, (_, value) in enumerate(x_sorted)}
        n = len(x)
        sum_diff_ranks_squared = sum((ranks_x[x[i]] - ranks_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_ranks_squared) / (n * (n**2 - 1))
    
    def log_width(width):
        return math.log(width, 2)
    
    width_values = [5, 10, 15, 20, 30, 40]
    cohomology_values = []
    for width in width_values:
        for _ in range(5):  # Sample 5 instances per width
            program = read_twice_branching_program(width)
            cohomology = groupoid_cohomology(program)
            cohomology_values.append(cohomology)
    
    if not cohomology_values or not width_values:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_width_values = [log_width(width) for width in width_values]
    correlation = spearman_rank_correlation(cohomology_values, log_width_values)
    median_cohomology = sorted(cohomology_values)[len(cohomology_values) // 2]
    mean_cohomology = sum(cohomology_values) / len(cohomology_values)
    std_cohomology = math.sqrt(sum((x - mean_cohomology) ** 2 for x in cohomology_values) / len(cohomology_values))
    
    expected_median = mean_cohomology + std_cohomology
    lower_bound = max(0, median_cohomology - std_cohomology)
    upper_bound = median_cohomology + std_cohomology
    
    conjecture_holds = correlation > 0.7 and lower_bound <= expected_median <= upper_bound
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": correlation,
        "instances_tested": len(cohomology_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"correlation={correlation}, median_cohomology={median_cohomology}, expected_median={expected_median}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
        sys.exit(0)
    
    mean_correlation = sum(r["metric_value"] for r in results) / len(results)
    std_correlation = math.sqrt(sum((r["metric_value"] - mean_correlation) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")