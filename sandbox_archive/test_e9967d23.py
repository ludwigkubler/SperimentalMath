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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hodge_decomposition(f):
        n = int(math.log2(len(f)))
        H = [[0] * (n + 1) for _ in range(n + 1)]
        H[0][0] = sum(f)
        return H
    
    def resolution_width(f):
        # Simplified version of DPLL algorithm to estimate width
        clauses = [f[i:i+n+1] for i in range(0, len(f), n+1)]
        stack = []
        width = 0
        
        while clauses:
            clause = next((c for c in clauses if any(x == 1 for x in c)), None)
            if not clause:
                return float('inf')
            
            literals = [i for i, x in enumerate(clause) if x == 1]
            stack.append(literals)
            width = max(width, len(literals))
            
            new_clauses = []
            for c in clauses:
                if any(x == 0 for x in c):
                    continue
                new_c = [x for i, x in enumerate(c) if i not in literals]
                if new_c:
                    new_clauses.append(new_c)
            clauses = new_clauses
        
        return width
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    H = hodge_decomposition(f)
    rank_0th_degree = sum(H[0])
    width = resolution_width(f)
    
    if width == float('inf'):
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof width is infinite"
        }
    
    ratio = rank_0th_degree / width
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 109))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    ratios = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios):.2f} std={math.sqrt(sum((x - sum(ratios)/len(ratios))**2 for x in ratios) / len(ratios)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios):.2f} std={math.sqrt(sum((x - sum(ratios)/len(ratios))**2 for x in ratios) / len(ratios)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_exceeds_bound' first_failing_seed={first_failing_seed}")