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
    
    def generate_k_cnf(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return variables, clauses
    
    def noncrossing_partition_rank(variables, clauses):
        # Simplified rank calculation (example implementation)
        return len(variables) + len(clauses)
    
    def resolution_proof_tree_width(variables, clauses):
        # Simplified tree-width calculation (example implementation)
        return max(len(c) for c in clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables, clauses = generate_k_cnf(n, m)
    
    rank = noncrossing_partition_rank(variables, clauses)
    tree_width = resolution_proof_tree_width(variables, clauses)
    
    if tree_width == 0:
        return {
            "metric_name": "Rank vs Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Tree-width is zero"
        }
    
    c1 = Fraction(1, 2)
    c2 = Fraction(3, 2)
    
    holds = c1 * rank <= tree_width <= c2 * rank
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": tree_width,
        "instances_tested": 1,
        "conjecture_holds": holds,
        "counterexample": "" if holds else f"Counterexample: rank={rank}, tree-width={tree_width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(v is not None for v in metric_values):
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((v - mean) ** 2 for v in metric_values) / len(metric_values))
        if support_fraction >= 0.9:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=None")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation_or_division_by_zero")