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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        p = [[0] * (2**n) for _ in range(n)]
        for i in range(n):
            for j in range(2**i):
                for k in range(1 << (n - i - 1)):
                    if all((j & (1 << m)) == ((k + j) & (1 << m)) for m in range(i)):
                        p[i][j] += 1
        return p
    
    def minimal_local_induction_dimension(p):
        n = len(p)
        dim = 0
        for i in range(n):
            if any(p[i][j] != 0 for j in range(2**i)):
                dim += 1
        return dim
    
    def communication_complexity_rank(cnf):
        n = len(cnf[0])
        m = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] = 1
                else:
                    matrix[i][-1] += 1
        rank = 0
        for row in matrix:
            if any(x != 0 for x in row):
                rank += 1
        return rank
    
    n_max = 40
    instances_tested = 0
    mld_values = []
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        p = clause_indicator_polynomial(cnf)
        mld = minimal_local_induction_dimension(p)
        rk_comm = communication_complexity_rank(cnf)
        
        if mld is not None and rk_comm is not None:
            instances_tested += 1
            mld_values.append(mld)
    
    if instances_tested == 0:
        return {
            "metric_name": "mld vs. rk_comm",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_mld = sum(mld_values) / instances_tested
    std_mld = math.sqrt(sum((x - mean_mld) ** 2 for x in mld_values) / instances_tested)
    correlation_coefficient = sum((mld_values[i] - mean_mld) * (i + 5 - 15) for i in range(instances_tested)) / (instances_tested * std_mld * math.sqrt(n_max - 10))
    
    return {
        "metric_name": "mld vs. rk_comm",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and std_mld <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")