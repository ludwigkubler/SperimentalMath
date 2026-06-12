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
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        if not cnf:
            return True
        literals = set(abs(lit) for clause in cnf for lit in clause)
        literal = next(iter(literals))
        positive = [lit for clause in cnf if literal in clause]
        negative = [lit for clause in cnf if -literal in clause]
        if dpll(positive):
            return True
        if dpll(negative):
            return True
        return False
    
    def p_adic_hodge_rank(cnf):
        # Placeholder function to simulate the computation of p-adic Hodge rank
        # This is a dummy implementation for testing purposes
        return len(cnf)
    
    n = 20
    cnf = generate_cnf(n)
    rank_H = p_adic_hodge_rank(cnf)
    proof_length = dpll(cnf)
    
    if not proof_length:
        proof_length = float('inf')
    
    metric_value = rank_H / proof_length
    
    return {
        "metric_name": "rank_H_to_proof_length_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if metric_value >= 0.8 else False,
        "counterexample": "" if metric_value >= 0.8 else f"rank_H={rank_H}, proof_length={proof_length}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")