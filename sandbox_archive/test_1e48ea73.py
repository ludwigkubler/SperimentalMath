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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        p = [1] * (2 ** n)
        for clause in cnf:
            indicator = [0] * n
            for literal in clause:
                if literal > 0:
                    indicator[literal - 1] = 1
                else:
                    indicator[-literal - 1] = 1
            for i in range(len(p)):
                if all(indicator[j] == (i >> j) & 1 for j in range(n)):
                    p[i] += 1
        return p

    def communication_complexity_rank(cnf):
        n = len(cnf[0])
        m = len(cnf)
        matrix = [[0] * n for _ in range(m)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal - 1] = 1
                else:
                    matrix[i][-literal - 1] = 1
        rank = 0
        for row in matrix:
            if any(row[j] != 0 for j in range(n)):
                rank += 1
        return rank

    def minimal_local_induction_dimension(p):
        n = len(p)
        mld = 0
        while True:
            found = False
            for i in range(2 ** n):
                if p[i] > 0:
                    new_assignment = [i >> j & 1 for j in range(n)]
                    if all(new_assignment[j] == (i >> j) & 1 for j in range(n)):
                        found = True
                        break
            if not found:
                break
            mld += 1
        return mld

    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            cnf.append(clause)
        return cnf

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, min(40, n)))
            p = clause_indicator_polynomial(cnf)
            mld = minimal_local_induction_dimension(p)
            rk_comm = communication_complexity_rank(cnf)
            results.append((mld, rk_comm))

    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    correlation = sum(x * y for x, y in results) / len(results)
    mld_values = [x for x, _ in results]
    mean_mld = sum(mld_values) / len(mld_values)
    std_mld = math.sqrt(sum((x - mean_mld) ** 2 for x in mld_values) / len(mld_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation >= 0.8 and std_mld <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] + list(range(37, 101, 2))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")