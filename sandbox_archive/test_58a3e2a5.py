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

def generate_random_3cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            lit = random.randint(-n, n)
            if -lit not in clause and lit != 0:
                clause.add(lit)
        clauses.append(tuple(sorted(clause)))
    return clauses

def free_probability_tensor_product(clauses):
    n = max(abs(lit) for clause in clauses for lit in clause)
    M = [[0] * (2**n) for _ in range(2**n)]
    
    def add_clause(clause):
        for i in range(1 << n):
            for j in range(1 << n):
                if all((i >> k & 1) ^ (j >> k & 1) == int(lit > 0) for lit in clause):
                    M[i][j] += 1
    
    for clause in clauses:
        add_clause(clause)
    
    # Normalize the matrix
    total = sum(sum(row) for row in M)
    for i in range(2**n):
        for j in range(2**n):
            M[i][j] /= total
    
    return M

def noncommutative_information_entropy(M, n):
    entropy = 0.0
    for i in range(1 << n):
        for j in range(1 << n):
            if M[i][j] > 0:
                entropy -= M[i][j] * math.log2(M[i][j])
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n**2, n**3)
    clauses = generate_random_3cnf(n, m)
    
    M = free_probability_tensor_product(clauses)
    entropy = noncommutative_information_entropy(M, n)
    
    max_log_fact_n = math.log(math.factorial(n)) ** 0.5
    conjecture_holds = entropy <= max_log_fact_n
    
    return {
        "metric_name": "noncommutative_information_entropy",
        "metric_value": entropy,
        "instances_tested": len(clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Entropy {entropy} > {max_log_fact_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")