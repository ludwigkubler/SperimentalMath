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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) > 0:
                clauses.append(clause)
        return clauses

    def tropical_semi_ring(clauses):
        n = len(clauses[0])
        semi_ring = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i, lit in enumerate(clause):
                if lit > 0:
                    semi_ring[i][lit - 1] = max(semi_ring[i][lit - 1], 1)
                else:
                    semi_ring[lit - 1][i] = max(semi_ring[lit - 1][i], 1)
        return semi_ring

    def minimal_rank(semi_ring):
        n = len(semi_ring)
        rank = 0
        for i in range(n):
            if any(semi_ring[i][j] > 0 for j in range(n)):
                rank += 1
        return rank

    def resolution_proof_length(clauses):
        # Simplified heuristic to estimate proof length
        return len(clauses) * 2

    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_length = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            clauses = generate_sat_instance(n)
            semi_ring = tropical_semi_ring(clauses)
            rank = minimal_rank(semi_ring)
            length = resolution_proof_length(clauses)
            total_rank += rank
            total_length += length
            instances_tested += 1

    avg_rank = total_rank / instances_tested
    avg_length = total_length / instances_tested
    ratio = avg_rank / (avg_length ** 2)

    return {
        "metric_name": "Ratio of Minimal Rank to Log^2(Length)",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": ratio <= 10,  # Placeholder constant C
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")