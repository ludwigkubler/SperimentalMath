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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def dpll(formula):
        if not formula:
            return 0
        if '0' not in formula and '1' not in formula:
            return 0
        if '0' not in formula:
            return 1 + dpll(formula.replace('1', '', 1))
        if '1' not in formula:
            return 1 + dpll(formula.replace('0', '', 1))
        return max(1 + dpll(formula.replace('0', '', 1)), 1 + dpll(formula.replace('1', '', 1)))
    
    def simplicial_complex_size(n):
        return sum(math.comb(n, k) for k in range(n+1))
    
    def local_coherence(n):
        return n / math.log2(n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(30):
            formula = generate_boolean_formula(n)
            proof_depth = dpll(formula)
            coherence = local_coherence(n)
            results.append((coherence, proof_depth))
    
    if not results:
        return {
            "metric_name": "local_coherence_vs_proof_depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    coherence_values = [r[0] for r in results]
    proof_depths = [r[1] for r in results]
    
    mean_coherence = sum(coherence_values) / len(coherence_values)
    mean_proof_depth = sum(proof_depths) / len(proof_depths)
    pearson_corr = sum((coherence - mean_coherence) * (depth - mean_proof_depth) for coherence, depth in results) / (len(results) * math.sqrt(sum((coherence - mean_coherence)**2 for coherence in coherence_values)) * math.sqrt(sum((depth - mean_proof_depth)**2 for depth in proof_depths)))
    
    return {
        "metric_name": "local_coherence_vs_proof_depth",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = "Pearson correlation below threshold"
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")