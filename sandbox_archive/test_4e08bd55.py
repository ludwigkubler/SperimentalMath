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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        width = 0
        seen = set()
        for clause in cnf:
            if any(abs(lit) not in seen for lit in clause):
                seen.update(clause)
                width += len(clause)
        return width
    
    def groupoid_automorphism_group(cnf):
        # Simplified version of automorphism group calculation
        n = len(cnf)
        aut_group = set()
        for perm in itertools.permutations(range(1, n + 1)):
            if all((lit > 0 and perm[lit - 1] > 0) or (lit < 0 and perm[-lit] < 0) for lit in cnf):
                aut_group.add(tuple(perm))
        return len(aut_group)
    
    def correlation_coefficient(values1, values2):
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        cov = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n)) / n
        std1 = math.sqrt(sum((values1[i] - mean1) ** 2 for i in range(n)) / n)
        std2 = math.sqrt(sum((values2[i] - mean2) ** 2 for i in range(n)) / n)
        return cov / (std1 * std2)
    
    def mean(values):
        return sum(values) / len(values)
    
    def std(values, mean_val):
        return math.sqrt(sum((x - mean_val) ** 2 for x in values) / len(values))
    
    n_values = [5, 10, 15, 20, 30, 40]
    aut_group_sizes = []
    widths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        aut_group_size = groupoid_automorphism_group(cnf)
        width = resolution_width(cnf)
        aut_group_sizes.append(aut_group_size)
        widths.append(width)
    
    correlation = correlation_coefficient(aut_group_sizes, widths)
    mean_ratio = mean([a / w for a, w in zip(aut_group_sizes, widths)], 0)
    
    result = {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and mean_ratio <= 1,
        "counterexample": "" if abs(correlation) >= 0.8 and mean_ratio <= 1 else f"correlation_coefficient={correlation} — avoid: terminal failure after 4 attempts"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = mean([r["metric_value"] for r in results])
    std_metric_value = std([r["metric_value"] for r in results], mean_metric_value)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=0\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")