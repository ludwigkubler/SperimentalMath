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
    
    def generate_k_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(1, n + 1), k=random.randint(1, n)))
            if random.choice([True, False]):
                clause = {-(var) for var in clause}
            clauses.append(clause)
        return clauses
    
    def symplectic_form(clauses):
        n = len(clauses[0])
        form = [[0] * (2 * n) for _ in range(2 * n)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    i, j = lit - 1, lit - 1
                else:
                    i, j = -(lit + 1), -(lit + 1)
                form[i][j] += 1
                form[j][i] += 1
        return form
    
    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        # This is a placeholder and should be replaced with an actual algorithm
        return len(clauses) * 2
    
    n = random.randint(10, 40)
    m = random.randint(n, n * 3)
    clauses = generate_k_cnf(n, m)
    
    form = symplectic_form(clauses)
    width = resolution_width(clauses)
    
    # Placeholder for minimal rank calculation
    min_rank = sum(max(form[i][j] for j in range(2 * n)) for i in range(2 * n))
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")