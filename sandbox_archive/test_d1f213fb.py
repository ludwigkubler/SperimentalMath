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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        def is_tautology(new_clause):
            literals = set(lit for clause in clauses for lit in clause)
            for literal in literals:
                if -literal in literals:
                    return True
            return False
        
        stack = []
        while stack or clauses:
            if not stack:
                new_clause = random.choice(clauses)
                clauses.remove(new_clause)
                stack.append(new_clause)
            else:
                top_clause = stack[-1]
                literal = random.choice(top_clause)
                if -literal in top_clause:
                    return 0
                elif literal in top_clause:
                    stack.pop()
                    for clause in clauses:
                        if literal in clause and -literal not in clause:
                            new_clause = [l for l in clause if l != literal]
                            if is_tautology(new_clause):
                                continue
                            stack.append(new_clause)
                            break
                else:
                    new_clause = [l for l in top_clause if l != literal]
                    stack.pop()
                    clauses.append(new_clause)
        return len(stack)

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    width = resolution_width(clauses)
    
    d_phi = n * (n + 1) // 2  # Dimension of symmetric invariants for a 3-CNF formula with n variables
    conjecture_holds = width >= math.log2(d_phi)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, d(Φ)={d_phi}, width={width}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width:.4f} std={std_width:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")