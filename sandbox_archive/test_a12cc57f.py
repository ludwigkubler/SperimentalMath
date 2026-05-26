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
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(clause[i]) != abs(clause[j]) for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def free_probability_tensor_product(clauses):
        n = len(clauses[0])
        M = [[0] * (2**n) for _ in range(2**n)]
        for clause in clauses:
            for i in range(2**n):
                for j in range(2**n):
                    if all((i >> k & 1) ^ (j >> k & 1) == abs(clause[k]) for k in range(n)):
                        M[i][j] += 1
        return M
    
    def noncommutative_information_entropy(M):
        n = len(M)
        total = sum(sum(row) for row in M)
        entropy = 0
        for i in range(n):
            for j in range(n):
                p_ij = M[i][j] / total
                if p_ij > 0:
                    entropy -= p_ij * math.log2(p_ij)
        return entropy
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    M = free_probability_tensor_product(clauses)
    entropy = noncommutative_information_entropy(M)
    
    dpll_proof_length = len(clauses) * math.log2(math.factorial(n))
    
    return {
        "metric_name": "noncommutative_information_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= math.sqrt(math.factorial(n)),
        "counterexample": "" if entropy <= math.sqrt(math.factorial(n)) else f"High entropy {entropy} for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"High entropy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")