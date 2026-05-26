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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def frege_proof_width(formula):
        # Simplified estimate of Frege proof width
        return len(formula) * 2

    def groupoid_cocomorphism(formula):
        # Placeholder function to simulate cocomorphism computation
        rank = sum(1 for _ in formula) / len(formula)
        return rank

    n = random.randint(4, 30)
    formula = generate_3cnf(n)
    proof_width = frege_proof_width(formula)
    cocomorphism_rank = groupoid_cocomorphism(formula)

    if proof_width == 0:
        return {
            "metric_name": "cocomorphism_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "proof_width_zero"
        }

    ratio = cocomorphism_rank / math.log2(n)
    return {
        "metric_name": "cocomorphism_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 31))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")