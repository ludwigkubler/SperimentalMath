# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import product
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def truth_table(cnf, n):
        tt = []
        for assignment in product([0, 1], repeat=n):
            tt.append(all(lit >= 0 and (assignment[lit // 2] == 1 if lit % 2 == 0 else not assignment[lit // 2]) for lit in cnf))
        return tt
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        clauses = [set(clause) for clause in cnf]
        resolvents = set()
        while True:
            new_resolvents = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    common_lits = clauses[i] & clauses[j]
                    if common_lits:
                        for lit in common_lits:
                            resolvent = (clauses[i] | clauses[j]).difference({lit, -lit})
                            if resolvent not in resolvents and resolvent not in new_resolvents:
                                new_resolvents.append(resolvent)
            if not new_resolvents:
                break
            resolvents.update(new_resolvents)
        return len(resolvents) + 1
    
    def min_lattice_dimension(tt):
        n = len(tt[0])
        lattice = []
        for i in range(2**n):
            row = [tt[j][i] for j in range(len(tt))]
            if all(row) or all(not x for x in row):
                lattice.append(row)
        return len(lattice)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = [[random.randint(1, 2*n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, 5))] for _ in range(n)]
        tt = truth_table(cnf, n)
        lattice_dim = min_lattice_dimension(tt)
        width = resolution_width(cnf)
        results.append({"n": n, "lattice_dim": lattice_dim, "width": width})
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    
    lattice_dims = [r["lattice_dim"] for r in results]
    widths = [r["width"] for r in results]
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    corr_coeff = correlation(lattice_dims, widths)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= corr_coeff < 1.0,
        "counterexample": "" if 0.5 <= corr_coeff < 1.0 else f"corr_coeff={corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] < 1.0) / len(results)
    
    if all(0.5 <= r["metric_value"] < 1.0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction=1")
    elif any(r["metric_value"] < 0.5 or r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] == False)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")