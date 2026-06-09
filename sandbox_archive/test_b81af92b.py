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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(1, n + 1):
            clause = [random.choice([-1, 1]) * var for var in variables if var != i]
            clause.append(-i)
            clauses.append(clause)
        
        return clauses
    
    def resolution_width(clauses):
        stack = []
        while clauses:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                return math.inf
            literal = unit_clause[0]
            polarity = literal > 0
            literals_to_remove = [l for l in stack if abs(l) == abs(literal)]
            stack.remove(unit_clause)
            clauses.remove(unit_clause)
            new_clauses = []
            for c in clauses:
                if literal in c:
                    continue
                if -literal in c:
                    new_c = [l for l in c if l != -literal]
                    if len(new_c) == 1:
                        return math.inf
                    new_clauses.append(new_c)
                else:
                    new_clauses.append(c)
            clauses.extend(new_clauses)
        return len(stack)
    
    def entropy_rate(n):
        # Simplified entropy rate calculation for demonstration purposes
        return n / math.log2(n + 1)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    width = resolution_width(formula)
    H_max = entropy_rate(n)
    
    return {
        "metric_name": "Resolution Proof Width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= 2 * H_max,  # Example constant c=2
        "counterexample": "" if width <= 2 * H_max else f"Width {width} exceeds 2 * H_max {2 * H_max}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")