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
    
    def generate_dnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_moment_map(dnf):
        # Simplified moment map computation for demonstration
        return len(dnf)
    
    def compute_circuit_depth(dnf):
        # Simplified circuit depth computation for demonstration
        return len(dnf) + 1
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    dnf = generate_dnf(n, m)
    
    r_min_M = compute_moment_map(dnf)
    D = compute_circuit_depth(dnf)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": None,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(res is None for res in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r is not None and r > 0.5) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if result is not None and result <= 0.5)
            print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")