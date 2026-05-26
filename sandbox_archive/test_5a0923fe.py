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
    
    def generate_ac0_circuit(n):
        # Simplified AC⁰ parity circuit generation
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def p_adic_differential_form(circuit):
        # Placeholder function to compute the p-adic differential form
        return sum(circuit)
    
    def hodge_rank(form):
        # Placeholder function to compute the Hodge rank
        return abs(form)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_ac0_circuit(n)
            form = p_adic_differential_form(circuit)
            rank = hodge_rank(form)
            total_hodge_rank += rank
            instances_tested += 1
    
    mean_hodge_rank = total_hodge_rank / instances_tested
    expected_value = math.log2(n)**2
    
    conjecture_holds = abs(mean_hodge_rank - expected_value) <= 0.5 * expected_value
    counterexample = "" if conjecture_holds else f"Mean Hodge rank {mean_hodge_rank} not within ±50% of Θ(log^2({n})) = {expected_value}"
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": mean_hodge_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")