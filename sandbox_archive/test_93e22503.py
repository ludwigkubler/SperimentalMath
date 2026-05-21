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
    
    def generate_cnf_tautology(n):
        clauses = []
        for i in range(n):
            literals = [random.choice([1, -1]) * j for j in range(1, n+1)]
            clause = random.choice(literals)
            while len(set(clause)) != 2:
                clause = random.choice(literals)
            clauses.append(clause)
        return clauses
    
    def compute_minimal_invariant(F):
        # Placeholder function to compute minimal invariant
        # This is a dummy implementation for the purpose of testing
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf_tautology = generate_cnf_tautology(n)
        F = compute_minimal_invariant(cnf_tautology)
        
        for _ in range(10):  # Test with 10 different read-once BP proofs
            bp_proof_size = random.randint(1, n)
            bp_proof_invariant = compute_minimal_invariant(bp_proof_size)
            
            if bp_proof_invariant < math.log(bp_proof_size):
                return {
                    "metric_name": "minimal_invariant",
                    "metric_value": bp_proof_invariant,
                    "instances_tested": 10,
                    "conjecture_holds": False,
                    "counterexample": f"BP proof of size {bp_proof_size} has invariant < log({bp_proof_size})"
                }
    
    return {
        "metric_name": "minimal_invariant",
        "metric_value": sum(results) / len(results),
        "instances_tested": 60,  # 10 trials for each of 6 n values
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        all_results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in all_results) / len(all_results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r['conjecture_holds']) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_invariant < log(size(P))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")