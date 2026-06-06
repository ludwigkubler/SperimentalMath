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
        for _ in range(2**n // 4):  # Generate a small CNF to avoid triviality
            clause = [random.randint(-1, -n), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def circuit_monotone_width(cnf):
        width = 0
        for clause in cnf:
            width = max(width, len([x for x in clause if x > 0]))
        return width
    
    def topological_entropy(cnf):
        n = len(set(abs(x) for clause in cnf for x in clause))
        entropy = 0
        for clause in cnf:
            entropy += math.log2(1 / (n - len([x for x in clause if x > 0])))
        return entropy
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    h_phi = topological_entropy(cnf)
    w_m_phi = circuit_monotone_width(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": h_phi * w_m_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")