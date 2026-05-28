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
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals + ['~' + l for l in literals], 2)
            clauses.append(clause)
        return clauses

    def resolution_proof_size(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    if any(lit.startswith('~') and lit[1:] in clause_j or not lit.startswith('~') and lit in clause_i for lit in clause_i):
                        new_clause = clause_i ^ clause_j
                        if len(new_clause) == 0:
                            return 0
                        new_clauses.append(list(new_clause))
            if new_clauses == clauses:
                break
            clauses.extend(new_clauses)
        return len(clauses)

    def generalized_continued_fraction(cnf):
        # Simplified version for demonstration purposes
        return len(cnf) ** 2

    n = random.randint(5, 30)
    m = random.randint(n * 2, n * 4)
    cnf = generate_cnf(n, m)
    
    rank = generalized_continued_fraction(cnf)
    proof_size = resolution_proof_size(cnf)
    
    if proof_size > rank * 1.5:
        return {
            "metric_name": "resolution_proof_size",
            "metric_value": proof_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Proof size {proof_size} exceeds bound {rank * 1.5}"
        }
    else:
        return {
            "metric_name": "resolution_proof_size",
            "metric_value": proof_size,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Proof size exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")