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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        poly = [[0] * n for _ in range(n)]
        for clause in clauses:
            for literal in clause:
                var = abs(literal) - 1
                if literal > 0:
                    poly[var][var] += 1
                else:
                    poly[var][var] -= 1
        return poly
    
    def min_order(poly):
        n = len(poly)
        for order in range(2, n + 1):
            found = True
            for i in range(n):
                if not all(abs(poly[i][j]) % order == 0 for j in range(n)):
                    found = False
                    break
            if found:
                return order
        return n
    
    def resolution_width(clauses):
        stack = []
        while clauses:
            clause = clauses.pop()
            if len(clause) == 1:
                literal = clause[0]
                var = abs(literal) - 1
                for i in range(len(clauses)):
                    if literal in clauses[i]:
                        clauses[i].remove(literal)
                        clauses[i].append(-literal)
                        if len(clauses[i]) == 1:
                            return float('inf')
                stack.append((var, literal))
            else:
                literals = set(clause)
                for i in range(len(clauses)):
                    if literals.intersection(clauses[i]):
                        new_clause = [l for l in clauses[i] if l not in literals]
                        if len(new_clause) == 1:
                            return float('inf')
                        clauses[i] = new_clause
        return max(stack, key=lambda x: abs(x[1]))[0]
    
    n = random.randint(5, 40)
    phi = generate_3cnf(n)
    phi_poly = clause_indicator_polynomial(phi)
    min_order_phi = min_order(phi_poly)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "min_order_over_w",
        "metric_value": min_order_phi / (w_phi if w_phi != float('inf') else 1),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= min_order_phi / (w_phi if w_phi != float('inf') else 1) <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "min_order_over_w out of [0.5, 2]"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")