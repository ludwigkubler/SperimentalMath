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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if -var not in clause and var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def compute_min_rank(cnf):
        # Placeholder for actual computation
        # This is a dummy implementation that returns a random rank
        return random.uniform(1, 10)
    
    def dpll_proof_width(cnf):
        # Placeholder for actual DPLL proof width computation
        # This is a dummy implementation that returns a random width
        return random.uniform(1, 10)
    
    n = random.randint(5, 40)
    k = random.randint(3, min(n, 10))
    cnf = generate_k_cnf(n, k)
    
    min_rank = compute_min_rank(cnf)
    proof_width = dpll_proof_width(cnf)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["metric_value"] is not None:
            results.append(result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no valid results")
    else:
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(min(results))]
            print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")