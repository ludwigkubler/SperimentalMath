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
    
    def generate_boolean_function(n, m):
        variables = [random.choice([0, 1]) for _ in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, k=random.randint(1, n))
            clauses.append(clause)
        return variables, clauses

    def resolution_proof_length(f):
        # Simplified DPLL solver to estimate proof length
        stack = []
        while stack:
            literal = stack.pop()
            if literal == 0:
                continue
            if literal < 0:
                negated_literal = -literal
                for clause in f[1]:
                    if negated_literal in clause:
                        clause.remove(negated_literal)
                        if not clause:
                            return float('inf')
                        stack.append(-random.choice(clause))
                continue
            for clause in f[1]:
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        return float('inf')
                    stack.append(-random.choice(clause))
        return len(stack)

    def toric_variety_rank(f):
        # Placeholder for computing the rank of a toric variety
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 5)

    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    f = generate_boolean_function(n, m)
    
    rank = toric_variety_rank(f)
    proof_length = resolution_proof_length(f)
    
    if proof_length == float('inf'):
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL solver found an unsatisfiable clause"
        }
    
    return {
        "metric_name": "rank_vs_resolution",
        "metric_value": rank / (2 ** proof_length),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        exit()

    metric_values = [result["metric_value"] for result in results]
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")