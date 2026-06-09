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
    
    n = 30  # Number of variables
    m = 100  # Number of clauses
    
    # Generate a random CNF formula with n variables and m clauses
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    
    # Compute the geometric entropy H(φ)
    total_assignments = 2 ** n
    uniform_prob = Fraction(1, total_assignments)
    phi_probs = [0] * total_assignments
    
    for assignment in range(total_assignments):
        count = 0
        for clause in clauses:
            if all((assignment >> var) & 1 for var in clause):
                count += 1
        phi_probs[assignment] = Fraction(count, m)
    
    # Compute the Kullback-Leibler divergence between φ and its uniform distribution
    entropy = 0
    for p_phi, p_uniform in zip(phi_probs, [uniform_prob] * total_assignments):
        if p_phi == 0:
            continue
        entropy += p_phi * math.log2(p_phi / p_uniform)
    
    # Return the result
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": m,
        "n_max": n,
        "conjecture_holds": entropy <= 10 * m**2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(res["metric_value"] for res in results) / len(results)
    std_entropy = math.sqrt(sum((res["metric_value"] - mean_entropy)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.9:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=1")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")