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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(x == -y for x, y in zip(clause, reversed(clause))):
                clauses.append(clause)
        return clauses
    
    def characteristic_polynomial(clause):
        n = len(clause)
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        poly[0][0] = 1
        for x in clause:
            new_poly = [[0] * (n + 1) for _ in range(n + 1)]
            for i in range(n + 1):
                for j in range(n + 1):
                    new_poly[i][j] += poly[i - abs(x)][j]
            poly = new_poly
        return poly
    
    def automorphic_forms(poly):
        n = len(poly) - 1
        forms = set()
        for i in range(1, n + 1):
            if all(poly[j][i] == poly[n - j][n - i] for j in range(n + 1)):
                forms.add(tuple(poly[i]))
        return len(forms)
    
    def resolution_width(cnf):
        clauses = cnf[:]
        queue = []
        while True:
            new_clauses = set()
            for clause in queue:
                if any(abs(lit) not in [abs(x) for x in clause] for lit in clause):
                    return len(queue)
                new_clauses.update([x for x in clause if abs(x) not in [abs(y) for y in queue]])
            queue = list(new_clauses)
    
    n_max = 0
    instances_tested = 0
    total_n = 0
    total_w = 0
    
    for n in range(5, 41):
        cnf = generate_cnf(n)
        poly = characteristic_polynomial(cnf)
        N = automorphic_forms(poly)
        w = resolution_width(cnf)
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_n += N
        total_w += w
    
    mean_N = total_n / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(N * w for N, w in zip([mean_N] * instances_tested, [mean_w] * instances_tested)) - instances_tested * mean_N * mean_w) / math.sqrt((instances_tested * sum(N**2 for N in [mean_N] * instances_tested) - instances_tested * mean_N**2) * (instances_tested * sum(w**2 for w in [mean_w] * instances_tested) - instances_tested * mean_w**2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_N <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_N <= 3 else f"correlation_coefficient={correlation_coefficient}, mean_N={mean_N}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 or r["metric_value"] > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")