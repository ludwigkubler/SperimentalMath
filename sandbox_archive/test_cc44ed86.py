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
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(40)]
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        p = []
        for i in range(2**n):
            indicator = [int((i >> j) & 1) for j in range(n)]
            if all(indicator[j] == c[j] for c in cnf):
                p.append(indicator)
        return p
    
    def minimal_local_induction_dimension(p):
        n = len(p[0])
        mld = 0
        for i in range(2**n):
            indicator = [int((i >> j) & 1) for j in range(n)]
            if all(indicator[j] == p[j][k] for j in range(n) for k in range(len(p))):
                mld += 1
        return mld
    
    def communication_complexity_rank(cnf):
        n = len(cnf[0])
        matrix = [[int(cnf[i][j]) for j in range(n)] for i in range(40)]
        rank = 0
        for i in range(n):
            if any(matrix[j][i] == 1 for j in range(40)):
                rank += 1
        return rank
    
    mld_values = []
    rk_comm_values = []
    
    for _ in range(30):
        cnf = generate_cnf(20)
        p = clause_indicator_polynomial(cnf)
        mld = minimal_local_induction_dimension(p)
        rk_comm = communication_complexity_rank(cnf)
        
        if mld is None or rk_comm is None:
            return {
                "metric_name": "mld",
                "metric_value": 0,
                "instances_tested": 1,
                "n_max": 20,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mld_values.append(mld)
        rk_comm_values.append(rk_comm)
    
    correlation = sum((mld - mean_mld) * (rk_comm - mean_rk_comm) for mld, rk_comm in zip(mld_values, rk_comm_values)) / len(mld_values)
    mean_mld = sum(mld_values) / len(mld_values)
    std_mld = math.sqrt(sum((mld - mean_mld)**2 for mld in mld_values) / len(mld_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": 20,
        "conjecture_holds": correlation >= 0.8 and std_mld <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_correlation = sum(r["metric_value"] for r in results) / len(results)
    std_correlation = math.sqrt(sum((r["metric_value"] - mean_correlation)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_group_size")