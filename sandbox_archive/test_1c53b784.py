# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        p = [[0] * (2**n) for _ in range(len(cnf))]
        for j in range(2**n):
            assignment = [1 if (j >> i) & 1 else -1 for i in range(n)]
            for clause in cnf:
                if all(assignment[i-1] == c for c, i in zip(clause, range(1, len(clause)+1))):
                    p[clauses.index(clause)][j] = 1
        return p
    
    def minimal_local_induction_dimension(p):
        n = len(p)
        mld = 0
        for j in range(n):
            if sum(p[j]) == 0:
                continue
            mld += 1
        return mld
    
    def communication_complexity_rank(cnf):
        n = len(cnf[0])
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for j in range(2**n):
            assignment = [1 if (j >> i) & 1 else -1 for i in range(n)]
            for k in range(2**n):
                new_assignment = [assignment[i] * (-1)**((k >> i) & 1) for i in range(n)]
                matrix[j][k] = any(all(new_assignment[i-1] == c for c, i in zip(clause, range(1, len(clause)+1))) for clause in cnf)
        rank = 0
        for j in range(2**n):
            if sum(matrix[j]) > 0:
                rank += 1
        return rank
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y)
        return cov / (var_x * var_y) ** 0.5
    
    n_max = 40
    instances_tested = 30
    mld_values = []
    rk_comm_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        p = clause_indicator_polynomial(cnf)
        mld = minimal_local_induction_dimension(p)
        rk_comm = communication_complexity_rank(cnf)
        mld_values.append(mld)
        rk_comm_values.append(rk_comm)
    
    correlation_coefficient = correlation(mld_values, rk_comm_values)
    mean_mld = sum(mld_values) / instances_tested
    std_mld = (sum((x - mean_mld)**2 for x in mld_values) / instances_tested) ** 0.5
    
    conjecture_holds = correlation_coefficient >= 0.8 and std_mld <= 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mld = sum(r["metric_value"] for r in results) / len(results)
    std_mld = (sum((r["metric_value"] - mean_mld)**2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mld} std={std_mld} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")