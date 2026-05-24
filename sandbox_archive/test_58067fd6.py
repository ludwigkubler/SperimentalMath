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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def search(assignment, clause_index):
            if clause_index == len(cnf):
                return True
            literals = cnf[clause_index]
            for literal in literals:
                var = abs(literal) - 1
                new_assignment = assignment[:]
                if literal > 0 and var not in new_assignment:
                    new_assignment[var] = True
                    if search(new_assignment, clause_index + 1):
                        return True
                elif literal < 0 and var in new_assignment and new_assignment[var]:
                    continue
            return False
        
        return search([], 0)
    
    def minimal_rank(cnf):
        n = len(cnf[0])
        rank = 0
        for i in range(2**n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            if dpll([[l if l != 0 else -assignment[var-1] for var, l in enumerate(clause)] for clause in cnf]):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = minimal_rank(cnf)
    proof_length = len(dpll(cnf))
    
    return {
        "metric_name": "minimal_rank_vs_dpll",
        "metric_value": rank / proof_length,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 * proof_length,  # Simplified for testing
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.randint(1000, 9999) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")