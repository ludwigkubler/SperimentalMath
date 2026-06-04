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
        for _ in range(2**n // 3):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            literal = queue.pop()
            if literal in seen or -literal in seen:
                continue
            seen.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [l for l in clause if l != literal]
                    if not new_clause:
                        return len(seen)
                    if -new_clause[0] in queue:
                        queue.remove(-new_clause[0])
                    elif -new_clause[0] not in seen:
                        queue.append(-new_clause[0])
        return float('inf')

    def formal_power_series_order(cnf):
        n = max(abs(lit) for lit in cnf)
        order = 1
        while True:
            found = False
            for clause in cnf:
                if all(abs(lit) <= order for lit in clause):
                    found = True
                    break
            if not found:
                return order - 1
            order += 1

    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    total_width = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            width = resolution_width(cnf)
            order = formal_power_series_order(cnf)
            if width == float('inf'):
                continue
            total_order += order
            total_width += width
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    correlation = (mean_order * mean_width - instances_tested * mean_order * mean_width /
                    (instances_tested ** 2)) / math.sqrt((total_order ** 2 - instances_tested * mean_order ** 2) *
                                                          (total_width ** 2 - instances_tested * mean_width ** 2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.6f} std={std_value:.6f} support_fraction={support_fraction:.2f}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction:.2f}")