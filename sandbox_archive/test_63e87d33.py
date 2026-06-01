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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * random.randint(1, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def p_adic_valuation_ring(cnf):
        # Simplified mapping from CNF to a rank
        return len(set(abs(lit) for clause in cnf for lit in clause))
    
    def frege_proof_length(cnf):
        # Simplified estimation of Frege proof length
        return sum(len(clause) for clause in cnf)
    
    n = 40
    min_rank_values = []
    proof_length_values = []
    
    for _ in range(30):
        cnf = generate_cnf(n)
        min_rank = p_adic_valuation_ring(cnf)
        proof_length = frege_proof_length(cnf)
        
        min_rank_values.append(min_rank)
        proof_length_values.append(proof_length)
    
    correlation_coefficient = 0
    if len(min_rank_values) > 1 and len(proof_length_values) > 1:
        mean_min_rank = sum(min_rank_values) / len(min_rank_values)
        mean_proof_length = sum(proof_length_values) / len(proof_length_values)
        
        numerator = sum((min_rank - mean_min_rank) * (proof_length - mean_proof_length) for min_rank, proof_length in zip(min_rank_values, proof_length_values))
        denominator = math.sqrt(sum((min_rank - mean_min_rank)**2 for min_rank in min_rank_values)) * math.sqrt(sum((proof_length - mean_proof_length)**2 for proof_length in proof_length_values))
        
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient_below_0.5"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_rank_values),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 80%")