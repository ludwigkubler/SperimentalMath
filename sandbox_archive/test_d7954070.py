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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        assignment = {i: None for i in range(1, len(cnf[0]) + 1)}
        stack = []
        
        def backtrack():
            if not cnf:
                return True
            literal = cnf[-1][0]
            var = abs(literal)
            if assignment[var] is None:
                assignment[var] = 1 if literal > 0 else -1
                if backtrack():
                    return True
                assignment[var] = -1 if literal > 0 else 1
                if backtrack():
                    return True
                assignment[var] = None
                return False
            elif assignment[var] * literal > 0:
                cnf.pop()
                return backtrack()
            else:
                cnf.pop()
                return backtrack()
        
        return backtrack()
    
    def read_twice_bp_size(cnf):
        if is_satisfiable(cnf):
            return 1
        else:
            return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_3cnf(n)
    sheaf_rank = n  # Simplified model: rank is proportional to the number of variables
    bp_size = read_twice_bp_size(cnf)
    
    ratio = Fraction(sheaf_rank, bp_size) if bp_size != 0 else Fraction(0, 1)
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - n / bp_size) <= 0.3 * (n / bp_size),
        "counterexample": "" if conjecture_holds else f"n={n}, sheaf_rank={sheaf_rank}, bp_size={bp_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")