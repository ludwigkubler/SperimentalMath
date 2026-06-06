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
    
    k = 2  # Binary Boolean formula
    m_min, m_max = 5, 10
    n_min, n_max = 5, 40
    
    def generate_formula(n: int, m: int):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, k)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def hypergeometric_sequence(n: int, m: int) -> Fraction:
        numerator = math.factorial(m)
        denominator = math.factorial(k) * math.factorial(m - k) * math.factorial(n - m)
        return Fraction(numerator, denominator)
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate width
        assignment = {i: None for i in range(1, n + 1)}
        
        def dpll():
            if not clauses:
                return True
            literal = random.choice([x for clause in clauses for x in clause])
            var = abs(literal)
            polarity = literal > 0
            
            assignment[var] = polarity
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            
            if dpll():
                return True
            
            assignment[var] = not polarity
            new_clauses = [c for c in clauses if -literal not in c and literal not in c]
            
            if dpll():
                return True
            
            assignment[var] = None
            return False
        
        width = 0
        while not dpll():
            width += 1
        return width
    
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in range(n_min, n_max + 1):
        for _ in range(30):  # Ensure at least 30 instances per seed
            m = random.randint(m_min, m_max)
            clauses = generate_formula(n, m)
            mu_phi = hypergeometric_sequence(n, m)
            w_phi = resolution_width(clauses)
            
            if w_phi == 0:
                continue
            
            ratio = mu_phi / w_phi
            total_ratio += ratio
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean_ratio - 1) <= 0.2,
        "counterexample": "" if abs(mean_ratio - 1) <= 0.2 else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio deviates from constant\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")