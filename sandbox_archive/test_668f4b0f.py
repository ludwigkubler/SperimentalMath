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
        for _ in range(10 * n):  # 10 clauses per variable on average
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def grlex_basis(cnf):
        n = len(cnf[0])
        basis = []
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    basis.append((i + 1, lit))
                else:
                    basis.append((-i - 1, -lit))
        return basis
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = [set([tuple(x) for x in clause]) for clause in cnf]
        width = 0
        while True:
            new_clauses = []
            added = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if len(clauses[i] & clauses[j]) == 1:
                        new_clause = (clauses[i] | clauses[j]).difference({tuple(x) for x in clauses[i] & clauses[j]})
                        if len(new_clause) > width:
                            width = len(new_clause)
                        new_clauses.append(new_clause)
                        added = True
            if not added:
                break
        return width
    
    def toric_variants(basis):
        n = max(abs(x[0]) for x in basis)
        variants = set()
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (i, j) not in variants and (j, i) not in variants:
                    variants.add((i, j))
        return len(variants)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    M_phi = []
    w_phi = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times
            cnf = generate_cnf(n)
            basis = grlex_basis(cnf)
            M_phi.append(toric_variants(basis))
            w_phi.append(resolution_width(cnf))
            instances_tested += 1
            n_max = max(n_max, n)
    
    correlation_coefficient = pearson_correlation(M_phi, w_phi)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(M <= w + 10 for M, w in zip(M_phi, w_phi)),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")