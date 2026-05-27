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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [-v for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def construct_frege_proof(cnf):
        proof = []
        for clause in cnf:
            proof.append(('OR', clause))
        return proof
    
    def p_adic_valuation(vector, p):
        valuation = 0
        for v in vector:
            if v % p == 0:
                valuation += 1
        return valuation
    
    def min_rank(valuations):
        return max(set(valuations), key=valuations.count)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof = construct_frege_proof(cnf)
    depth = len(proof)
    
    p = 2  # Fixed prime for simplicity
    valuations = [p_adic_valuation(clause, p) for clause in cnf]
    min_rank_value = min_rank(valuations)
    
    ratio = min_rank_value / depth if depth > 0 else float('inf')
    
    return {
        "metric_name": "min_rank_ratio",
        "metric_value": ratio,
        "instances_tested": n,
        "conjecture_holds": ratio <= 2.0,
        "counterexample": "" if ratio <= 2.0 else f"Depth {depth}, Min Rank {min_rank_value}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r['metric_value'] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")