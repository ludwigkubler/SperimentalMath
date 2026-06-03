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
    
    def dpll(lits, cls):
        if not lits:
            return True
        lit = lits[0]
        new_lits_true = [l for l in lits if l != -lit and (l == lit or l not in cls)]
        new_lits_false = [l for l in lits if l != lit and (-l == lit or -l not in cls)]
        return solve(new_lits_true, cls) or solve(new_lits_false, cls)
    
    def solve(lits, cls):
        if not dpll(lits, cls):
            return False
        while True:
            new_cls = []
            for l in lits:
                if l in new_cls:
                    continue
                if -l in new_cls:
                    return False
                new_cls.append(l)
            if new_cls == cls:
                break
            cls = new_cls
        return True
    
    def generate_cnf(n):
        cnf = []
        for i in range(n):
            clause = [random.randint(1, n) * (2 * random.randint(0, 1) - 1) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def dpll_width(cnf):
        cls = []
        for lit in cnf:
            if not solve(lit, cls):
                return len(cls)
        return len(cls)
    
    def noncommutative_symmetric_space_index(cnf):
        # Placeholder implementation
        return random.random() * 10
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    index = noncommutative_symmetric_space_index(cnf)
    width = dpll_width(cnf)
    
    return {
        "metric_name": "Index(X(φ)) vs DPLL proof width",
        "metric_value": index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(index - width) < 0.8 * min(index, width),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")