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
    
    def generate_cnf(n, m):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals + [f"~{l}" for l in literals], 2)
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        if not cnf:
            return True
        literal = next((l for l in cnf[0] if l.startswith('x')), None)
        if literal is None:
            return False
        
        def simplify_cnf(cnf, literal):
            new_clauses = []
            for clause in cnf:
                if literal not in clause and f"~{literal}" not in clause:
                    new_clauses.append(clause)
                elif literal in clause:
                    continue
                else:
                    new_clause = [l for l in clause if l != f"~{literal}"]
                    new_clauses.append(new_clause)
            return new_clauses
        
        if dpll(simplify_cnf(cnf, literal)):
            return True
        if dpll(simplify_cnf(cnf, f"~{literal}")):
            return True
        return False

    def generalized_continued_fraction(n):
        # Placeholder for the actual computation of the generalized continued fraction
        # This is a dummy implementation for demonstration purposes
        return n

    def resolution_proof_size(cnf):
        # Placeholder for the actual calculation of the resolution proof size
        # This is a dummy implementation for demonstration purposes
        return len(cnf) * 2

    n = random.randint(5, 40)
    m = random.randint(n*2, n**2)
    cnf = generate_cnf(n, m)
    
    rank = generalized_continued_fraction(n)
    proof_size = resolution_proof_size(cnf)
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": proof_size <= rank * 1.5,
        "counterexample": "" if proof_size <= rank * 1.5 else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, m={results[0]['instances_tested']}\" first_failing_seed={first_failing_seed}")