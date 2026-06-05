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
    
    def diophantine_set(clauses):
        n = len(clauses)
        mod = 2**n - 1
        equations = [0] * (2**n)
        
        for clause in clauses:
            equation = 0
            for literal in clause:
                index = abs(literal) - 1
                coefficient = -1 if literal < 0 else 1
                equation += coefficient * mod_inverse(index + 1, mod)
                equation %= mod
            equations[equation] += 1
        
        return equations
    
    def mod_inverse(a: int, m: int) -> int:
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        raise ValueError("Modular inverse does not exist")
    
    def resolution_proof_depth(clauses):
        n = len(clauses)
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        
        def resolve(clause1, clause2):
            new_clauses = []
            for literal in clause1:
                if -literal in clause2:
                    remaining_literals = [l for l in clause2 if l != -literal]
                    new_clause = tuple(sorted(remaining_literals))
                    if new_clause not in clauses_set:
                        new_clauses.append(new_clause)
                        clauses_set.add(new_clause)
            return new_clauses
        
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    new_clauses.extend(resolve(clauses[i], clauses[j]))
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        
        return len(clauses) - n
    
    def tseitin_formula(n: int):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(1, n + 1):
            clause = [i]
            for j in range(i + 1, n + 1):
                clause.append(-j)
            clauses.append(clause)
        
        for i in range(1, n + 1):
            clause = [-i]
            for j in range(1, n + 1):
                if j != i:
                    clause.append(j)
            clauses.append(clause)
        
        return clauses
    
    def minimal_index_of_diophantine_equivalence(equations):
        max_count = max(equations)
        min_index = float('inf')
        for equation, count in enumerate(equations):
            if count == max_count:
                min_index = min(min_index, equation)
        return min_index
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        clauses = tseitin_formula(n)
        equations = diophantine_set(clauses)
        d_phi = resolution_proof_depth(clauses)
        id_phi = minimal_index_of_diophantine_equivalence(equations)
        
        if d_phi == 0 or id_phi == 0:
            continue
        
        ratio = Fraction(id_phi, d_phi).limit_denominator()
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= mean_ratio <= 1.5,
        "counterexample": "" if 0.5 <= mean_ratio <= 1.5 else f"Ratio out of range: {mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] <= 1.5) / len(results)
    
    if all(0.5 <= r["metric_value"] <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")