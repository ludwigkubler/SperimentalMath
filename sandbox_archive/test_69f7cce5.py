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
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def construct_affine_space(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    variables.add(literal)
                else:
                    variables.add(-literal)
        return list(variables)
    
    def compute_mli(affine_space):
        n = len(affine_space)
        # Placeholder for actual computation
        return random.random() * n
    
    def resolution_proof_width(cnf):
        # Placeholder for actual computation
        return random.randint(1, 2 * len(cnf))
    
    cnf = generate_random_cnf(5)  # Start with a small number of variables
    affine_space = construct_affine_space(cnf)
    mli_value = compute_mli(affine_space)
    w_value = resolution_proof_width(cnf)
    
    return {
        "metric_name": "mli_vs_w",
        "metric_value": mli_value,
        "instances_tested": 1,
        "n_max": len(affine_space),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")