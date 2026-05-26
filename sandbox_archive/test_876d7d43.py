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

def free_probability_tensor_product(clauses):
    n = len(clauses[0])
    M = [[Fraction(1, 2) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    
    for clause in clauses:
        for lit, sign in zip(clause, [1] * n):
            for k in range(n):
                M[k][k] = Fraction(1, 2)
                if (lit >> k & 1) ^ (j >> k & 1) == int(lit > 0):
                    M[k][k] += Fraction(sign, 2)
    
    return M

def noncommutative_information_entropy(M):
    n = len(M)
    entropy = 0
    for i in range(n):
        for j in range(n):
            if M[i][j] != 0:
                entropy -= M[i][j] * math.log2(M[i][j])
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    M = free_probability_tensor_product(clauses)
    entropy = noncommutative_information_entropy(M)
    
    return {
        "metric_name": "noncommutative_information_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= math.log(math.factorial(n)) ** 0.5,
        "counterexample": "" if entropy <= math.log(math.factorial(n)) ** 0.5 else f"High entropy {entropy} for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"High entropy found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")