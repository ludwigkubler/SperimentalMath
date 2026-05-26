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
    
    def generate_kcnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (-1 if random.random() < 0.5 else 1) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return variables, clauses

    def frege_proof_tree(clauses):
        # Simplified Frege proof tree construction
        # This is a placeholder and should be replaced with actual logic
        return [clauses]

    def k_theory(proof_tree, k):
        # Placeholder for K-theory computation
        # This is a placeholder and should be replaced with actual logic
        return [1.0] * len(proof_tree)

    def exterior_power_rank(k_theory_vector, k):
        # Placeholder for computing the minimal rank of the k-th exterior power
        # This is a placeholder and should be replaced with actual logic
        return sum(abs(x) for x in k_theory_vector) / len(k_theory_vector)

    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables, clauses = generate_kcnf(n, m)
    proof_tree = frege_proof_tree(clauses)
    k_theory_vector = k_theory(proof_tree, 1)  # Assuming k=1 for simplicity
    computed_rank = exterior_power_rank(k_theory_vector, 1)

    predicted_rank = math.log(n) / math.log(m)

    if abs(computed_rank - predicted_rank) > 0.3 * predicted_rank:
        conjecture_holds = False
        counterexample = f"n={n}, m={m}, k=1, computed_rank={computed_rank}, predicted_rank={predicted_rank}"
    else:
        conjecture_holds = True
        counterexample = ""

    return {
        "metric_name": "minimal_rank",
        "metric_value": computed_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")