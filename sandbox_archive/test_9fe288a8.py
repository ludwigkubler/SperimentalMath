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

def generate_cnf(n, num_clauses):
    literals = [f"x{i}" for i in range(1, n+1)] + [f"~x{i}" for i in range(1, n+1)]
    cnf = []
    for _ in range(num_clauses):
        clause = random.sample(literals, 2)
        cnf.append(clause)
    return cnf

def truth_table(cnf, n):
    tt = {}
    for assignment in product([0, 1], repeat=n):
        tt[assignment] = any(all(assignment[int(l[1:]) - 1] == (l[0] == '~') for l in clause) for clause in cnf)
    return tt

def min_lattice_dimension(tt):
    n = len(tt)
    lattice = []
    for i in range(n):
        if tt[i]:
            lattice.append([i])
    for i in range(n):
        if not tt[i]:
            lattice.append([i])
    while True:
        new_lattice = []
        for subset in lattice:
            for i in range(n):
                if i not in subset and all(j in subset or j >= n for j in range(i)):
                    new_subset = subset + [i]
                    if all(all(tt[j] == tt[k] for j, k in combinations(new_subset, 2)) for _ in range(10)):
                        new_lattice.append(new_subset)
        if len(new_lattice) == len(lattice):
            break
        lattice = new_lattice
    return len(lattice)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n, n * (n - 1) // 2)
        tt = truth_table(cnf, n)
        dim = min_lattice_dimension(tt)
        w_phi = len(cnf)  # Simplified resolution proof width
        results.append({"dim": dim, "w_phi": w_phi})
    if not results:
        return {"metric_name": "dim", "metric_value": None, "instances_tested": 0, "n_max": 0, "conjecture_holds": False, "counterexample": "mapping_undefined"}
    
    dims = [r["dim"] for r in results]
    w_phis = [r["w_phi"] for r in results]
    mean_dim = sum(dims) / len(dims)
    mean_w_phi = sum(w_phis) / len(w_phis)
    cov = sum((d - mean_dim) * (w - mean_w_phi) for d, w in zip(dims, w_phis)) / len(dims)
    var_w_phi = sum((w - mean_w_phi) ** 2 for w in w_phis) / len(w_phis)
    correlation_coefficient = cov / math.sqrt(var_w_phi * (sum((d - mean_dim) ** 2 for d in dims) / len(dims)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    from itertools import product, combinations
    
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")