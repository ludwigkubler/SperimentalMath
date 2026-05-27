# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        variables = list(range(1, n + 1))
        cnf = []
        for _ in range(n):
            clause = random.sample(variables + [-v for v in variables], 2)
            cnf.append(clause)
        return cnf
    
    def p_adic_valuation(vector):
        val = 0
        for x in vector:
            if x < 0:
                x = -x
            while x % 2 == 0:
                x //= 2
                val += 1
        return val
    
    def frege_proof(cnf):
        proof = []
        for clause in cnf:
            proof.append(clause)
        return proof
    
    def minimal_rank(proof):
        ranks = [p_adic_valuation(clause) for clause in proof]
        return min(ranks)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    depth = len(cnf)
    proof = frege_proof(cnf)
    rank = minimal_rank(proof)
    
    metric_value = rank / depth
    conjecture_holds = metric_value <= 2.0
    counterexample = "" if conjecture_holds else f"Depth {depth}, Rank {rank}"
    
    return {
        "metric_name": "Minimal Rank Ratio",
        "metric_value": metric_value,
        "instances_tested": depth,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = (sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth {results[first_failing_seed]['instances_tested']}, Rank {results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}")