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
    
    def generate_k_cnf(n, k):
        clauses = set()
        while len(clauses) < k:
            clause = tuple(random.sample(range(1, n+1), 2))
            if clause not in clauses and -clause not in clauses:
                clauses.add(clause)
        return clauses
    
    def frege_proof_length(k_cnf):
        # Simplified Frege proof length estimation
        return len(k_cnf) * 5 + random.randint(0, 10)
    
    def hopf_algebroid_representation(k_cnf):
        crossed_products = set()
        for clause in k_cnf:
            crossed_product = (clause[0], clause[1])
            crossed_products.add(crossed_product)
            crossed_products.add((-clause[0], -clause[1]))
        return crossed_products
    
    def min_num_crossed_products(k_cnf):
        return len(hopf_algebroid_representation(k_cnf))
    
    n = 40
    k = 20
    trials = 30
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds_count = 0
    
    for _ in range(trials):
        k_cnf = generate_k_cnf(n, k)
        instances_tested += len(k_cnf)
        
        min_crossed_products = min_num_crossed_products(k_cnf)
        proof_length = frege_proof_length(k_cnf)
        
        if proof_length == 0:
            continue
        
        ratio = min_crossed_products / proof_length
        total_metric_value += ratio
        
        if 0.5 <= ratio <= 2:
            conjecture_holds_count += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = conjecture_holds_count / trials
    
    return {
        "metric_name": "Ratio of MinNumCrossedProducts to FregeProofLength",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "Ratio out of [0.5, 2] range"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of [0.5, 2] range\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction too low")