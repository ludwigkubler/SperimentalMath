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
    
    def generate_k_clique(n, k):
        if n < k or k <= 0:
            return None
        clique = set(range(k))
        for i in range(k, n):
            if all(random.choice([True, False]) for _ in range(k)):
                clique.add(i)
        return clique
    
    def regular_expression_from_clique(clique):
        if not clique:
            return "ε"
        expr = "(" + " | ".join(f"({i})" for i in clique) + ")"
        for i in clique:
            expr += f".{expr}"
        return expr
    
    def automorphism_group_size(expr):
        # Simplified version of automorphism group calculation
        # This is a placeholder and should be replaced with actual computation
        return len(expr)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n, 20))
    clique = generate_k_clique(n, k)
    if not clique:
        return {
            "metric_name": "automorphism_group_size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k_clique_generation_failed"
        }
    
    expr = regular_expression_from_clique(clique)
    size = automorphism_group_size(expr)
    
    return {
        "metric_name": "automorphism_group_size",
        "metric_value": size,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 300, 10))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
        conjecture_holds = all(r["conjecture_holds"] for r in results if r["metric_value"] is not None)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if conjecture_holds:
            print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
        elif any(r["conjecture_holds"] for r in results):
            print(f"RESULT: FALSIFIED counterexample=\"not_all_seeds_support\" first_failing_seed={next(i for i, r in enumerate(results) if not r['conjecture_holds'])}")
        else:
            print("RESULT: INCONCLUSIVE no_support")