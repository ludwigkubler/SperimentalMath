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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                polarity = random.choice([-1, 1])
                if (var, polarity) not in clause and (-var, -polarity) not in clause:
                    clause.add((var, polarity))
            clauses.append(clause)
        return clauses
    
    def is_unsat_3cnf(clauses):
        n = max(abs(var) for var, _ in clauses)
        assignment = [random.choice([-1, 1]) for _ in range(n)]
        for clause in clauses:
            if all(assignment[abs(var)-1] * polarity != -1 for var, polarity in clause):
                return False
        return True
    
    def walsh_hadamard_transform(clauses, n):
        p_F = [0] * (2**n)
        for x in range(2**n):
            for C in clauses:
                product = 1
                for var, polarity in C:
                    if (x >> (var-1)) & 1 == 0:
                        product *= -polarity
                p_F[x] += product
        return [val / len(clauses) for val in p_F]
    
    def spectral_entropy(p_F):
        norm = sum(val**2 for val in p_F)
        q_F = [val**2 / norm for val in p_F]
        H_F = -sum(q * math.log2(q) if q != 0 else 0 for q in q_F)
        return H_F
    
    def tree_resolution(clauses, n):
        # Simplified version of tree-DPLL with VSIDS-free static order
        assignment = [None] * (n + 1)
        stack = []
        while True:
            if not stack:
                return len(assignment) - 1
            x = stack[-1]
            if assignment[x] is None:
                assignment[x] = 1
                for C in clauses:
                    if all(assignment[abs(var)] * polarity != -1 for var, polarity in C):
                        break
                else:
                    continue
                stack.append(x)
            elif assignment[x] == 1:
                assignment[x] = -1
                stack.pop()
            else:
                stack.pop()
    
    n_values = [10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        m = int(4.3 * n)
        for _ in range(30):
            clauses = generate_3cnf(n, m)
            if not is_unsat_3cnf(clauses):
                continue
            p_F = walsh_hadamard_transform(clauses, n)
            H_F = spectral_entropy(p_F)
            t_star = tree_resolution(clauses, n)
            R = math.log2(t_star) * math.log2(1 + n + n**2 + n**3) / (n * H_F)
            results.append(R)
    
    if not results:
        return {
            "metric_name": "R",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    min_R = min(results)
    pearson_corr = sum((x - mean) * (y - mean_pearson) for x, y in zip(results, range(len(results)))) / len(results)
    mean_R = sum(results) / len(results)
    std_R = math.sqrt(sum((x - mean_R)**2 for x in results) / len(results))
    
    return {
        "metric_name": "R",
        "metric_value": mean_R,
        "instances_tested": len(results),
        "conjecture_holds": min_R >= 0.05 and pearson_corr >= 0.5,
        "counterexample": "" if min_R >= 0.05 else f"min_R={min_R}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_R = sum(trial["metric_value"] for trial in results if trial["instances_tested"] > 0) / len(results)
    std_R = math.sqrt(sum((trial["metric_value"] - mean_R)**2 for trial in results if trial["instances_tested"] > 0) / len(results))
    support_fraction = sum(trial["conjecture_holds"] for trial in results if trial["instances_tested"] > 0) / len(results)
    
    if all(trial["conjecture_holds"] for trial in results):
        print(f"RESULT: SUPPORTED mean={mean_R} std={std_R} support_fraction={support_fraction}")
    elif any(trial["counterexample"] != "" for trial in results):
        first_failing_seed = next(seed for seed, trial in zip(seeds, results) if trial["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(trial['counterexample'] for trial in results if trial['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")