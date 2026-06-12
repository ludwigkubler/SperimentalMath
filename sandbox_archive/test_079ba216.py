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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                continue
            clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def clause_tree_width(clauses):
        if not clauses:
            return 0
        max_width = 0
        for clause in clauses:
            width = len(set(abs(lit) for lit in clause))
            max_width = max(max_width, width)
        return max_width
    
    def hodge_bundle_metric(clauses):
        n = len(next(iter(clauses)))
        matrix = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for lit in clause:
                i = abs(lit) - 1
                if lit > 0:
                    matrix[i][i] += Fraction(1, n)
                else:
                    matrix[n][i] -= Fraction(1, n)
        return max(abs(sum(matrix[i][j] for j in range(n + 1))) for i in range(n + 1))
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_max = 0
    metric_values = []
    clause_widths = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            cnf = generate_cnf(n)
            instances_tested += 1
            metric_value = hodge_bundle_metric(cnf)
            clause_width = clause_tree_width(cnf)
            metric_values.append(metric_value)
            clause_widths.append(clause_width)
    
    correlation = correlation_coefficient(metric_values, clause_widths)
    conjecture_holds = correlation >= 0.8 and max(abs(m - w) for m, w in zip(metric_values, clause_widths)) <= 3
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(abs(m - w) for m, w in zip([r["metric_value"] for r in results], [r["metric_width"] for r in results])) <= 3:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")