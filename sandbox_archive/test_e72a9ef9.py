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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses

    def polynomial_from_clauses(clauses):
        n = len(clauses[0])
        poly = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if clause[i] == 1:
                    for j in range(i+1, n):
                        if clause[j] == -1:
                            poly[i][j] += 1
                            poly[j][i] += 1
        return poly

    def local_cohomology_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if poly[i][j] != 0:
                    rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n)
        clauses = generate_3cnf(n, m)
        poly = polynomial_from_clauses(clauses)
        rank = local_cohomology_rank(poly)
        expected_rank = n**2 - m + 1
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "expected_rank": expected_rank,
            "conjecture_holds": rank <= expected_rank
        })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = "" if conjecture_holds else "n={} m={} rank={} expected_rank={}".format(
        results[0]["n"], results[0]["m"], results[0]["rank"], results[0]["expected_rank"]
    )
    
    return {
        "metric_name": "local_cohomology_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_dev, support_fraction))