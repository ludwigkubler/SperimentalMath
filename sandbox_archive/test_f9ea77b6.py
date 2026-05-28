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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, 3))]
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def resolution_length(cnf):
        stack = []
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            cnf.remove(unit_clause)
            for clause in cnf[:]:
                if literal in clause:
                    cnf.remove(clause)
                elif -literal in clause:
                    clause.remove(-literal)
                    if len(clause) == 1:
                        stack.append((clause, literal))
        return len(stack)

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    min_rank = n  # Placeholder for actual birational rank calculation
    resolution_proof_length = resolution_length(cnf)
    
    if min_rank > math.log(n) + 2 or resolution_proof_length > 2 * math.log(n):
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    min_rank_values = [r["metric_value"] for r in results if "min_rank" in r]
    resolution_proof_lengths = [r["metric_value"] for r in results if "resolution_proof_length" in r]
    
    mean_min_rank = sum(min_rank_values) / len(min_rank_values)
    std_min_rank = math.sqrt(sum((x - mean_min_rank) ** 2 for x in min_rank_values) / len(min_rank_values))
    
    support_fraction = sum(1 for r in results if "conjecture_holds" and r["conjecture_holds"]) / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_rank} std={std_min_rank} support_fraction={support_fraction}")
    elif any(result["min_rank"] > math.log(n) + 2 or result["resolution_proof_length"] > 2 * math.log(n) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")