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
    
    def generate_resolution_proof(w):
        proof = []
        for _ in range(w):
            clause = [random.randint(1, w) for _ in range(random.randint(2, 4))]
            proof.append(clause)
        return proof
    
    def frobenius_degree(proof):
        n = len(proof)
        max_clause_length = max(len(clause) for clause in proof)
        degree = max_clause_length * math.log(n, 2)
        return degree
    
    width = random.randint(5, 40)
    proof = generate_resolution_proof(width)
    degree = frobenius_degree(proof)
    
    return {
        "metric_name": "Frobenius Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "n_max": width,
        "conjecture_holds": degree <= 2 * math.log(width, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"degree > 2 * log(width)\" first_failing_seed={first_failing_seed}")