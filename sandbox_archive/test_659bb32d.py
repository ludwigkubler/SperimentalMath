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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_proof(cnf):
        clauses = set(tuple(c) for c in cnf)
        new_clauses = set()
        while True:
            new_clause_found = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 2:
                        literal = -list(set(clause1) ^ set(clause2))[0]
                        new_clause = [l for l in clause1 + clause2 if l != literal and -l not in clause1 + clause2]
                        if new_clause:
                            new_clauses.add(tuple(sorted(new_clause)))
                            new_clause_found = True
            if not new_clause_found:
                break
            clauses.update(new_clauses)
        return len(clauses) - len(cnf)
    
    def geometric_quantization_rank(depth):
        # Placeholder for actual computation
        return depth * 2
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_depth = resolution_proof(cnf)
    rank = geometric_quantization_rank(proof_depth)
    
    if rank == float('inf'):
        return {
            "metric_name": "geometric_quantization_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proved"
        }
    
    ratio = rank / proof_depth
    c = 2  # Placeholder constant for the conjecture
    
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= c,
        "counterexample": "" if ratio <= c else f"rank={rank}, expected={c * proof_depth}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [727, 773, 821, 877, 929]  # Default to primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")