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
    
    def generate_truth_table(n):
        return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]
    
    def polynomial_hierarchy_depth(truth_table):
        n = len(truth_table)
        m = 1
        while True:
            new_table = [[truth_table[i][j] ^ truth_table[i^k][j^k] for j in range(n)] for i, k in itertools.combinations(range(n), 2)]
            if all(new_table[i][j] == truth_table[i][j] for i in range(n) for j in range(n)):
                return m
            truth_table = new_table
            m += 1
    
    def monotone_dnf_formula(truth_table):
        n = len(truth_table)
        dnf = []
        for i in range(2**n):
            if truth_table[i][i] == 1:
                clause = [j for j in range(n) if (i & (1 << j)) != 0]
                dnf.append(clause)
        return dnf
    
    n_max = 40
    results = []
    
    for k in range(1, min(20, n_max//5 + 1)):
        for _ in range(30):
            n = random.randint(k*5, min(n_max, (k+1)*5))
            truth_table = generate_truth_table(n)
            dnf = monotone_dnf_formula(truth_table)
            depth = polynomial_hierarchy_depth(truth_table)
            if depth > (n**k) / 2:
                return {
                    "metric_name": "polynomial_hierarchy_depth",
                    "metric_value": depth,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"k={k}, n={n}"
                }
            results.append(depth)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    return {
        "metric_name": "polynomial_hierarchy_depth",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": std <= 0.1 * (n_max**k) / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='k={results[0]['counterexample'].split(',')[0]}, n={results[0]['counterexample'].split(',')[1]}' first_failing_seed={first_failing_seed}")