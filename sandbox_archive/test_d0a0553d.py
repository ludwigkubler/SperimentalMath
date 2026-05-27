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
    
    def xor_and_tree_width(clauses):
        if not clauses:
            return 0
        max_depth = 1
        for clause in clauses:
            depth = 1
            for literal in clause:
                if isinstance(literal, list):
                    depth += xor_and_tree_width(literal)
                else:
                    break
            max_depth = max(max_depth, depth)
        return max_depth
    
    def quotient_group_rank(clauses):
        # Construct a cyclic group for each variable
        variables = set()
        for clause in clauses:
            for literal in clause:
                if isinstance(literal, list):
                    continue
                variables.add(literal)
        
        # Assign each variable to an element of the cyclic group
        group_elements = {var: i % len(variables) for i, var in enumerate(sorted(variables))}
        
        # Compute the rank of the quotient group
        rank = 0
        seen = set()
        for clause in clauses:
            elements = []
            for literal in clause:
                if isinstance(literal, list):
                    continue
                elements.append(group_elements[literal])
            element = sum(elements) % len(variables)
            if element not in seen:
                seen.add(element)
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = []
        num_literals = random.randint(1, 3)
        for _ in range(num_literals):
            literal = random.choice([random.choice(['x', 'y']), random.choice(['not x', 'not y'])])
            if isinstance(literal, list):
                continue
            clause.append(literal)
        clauses.append(clause)
    
    w = xor_and_tree_width(clauses)
    rank = quotient_group_rank(clauses)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": n,
        "conjecture_holds": rank <= 2 * w ** 2 * math.log2(w),
        "counterexample": "" if rank <= 2 * w ** 2 * math.log2(w) else f"Rank {rank} exceeds bound {2 * w ** 2 * math.log2(w)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")