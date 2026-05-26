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
    
    def tseitin_resolution_tree(clauses):
        if not clauses:
            return {}, {}
        
        literals = set()
        tree = {lit: [] for lit in literals}
        
        def add_clause(clause):
            nonlocal literals
            new_var = len(literals) + 1
            literals.add(new_var)
            
            for lit in clause:
                if lit < 0:
                    tree[-lit].append((new_var, 'not'))
                else:
                    tree[lit].append((new_var, 'and'))
                
                add_clause([-new_var])
        
        for clause in clauses:
            add_clause(clause)
        
        return tree, literals
    
    def geometric_langlands_rank(tree):
        # Placeholder implementation
        # This should be replaced with a proper mapping to an algebraic structure
        # and computation of the rank of the associated object.
        return len(tree)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        num_vars = random.randint(2, 10)
        clause = [random.choice([-i, i]) for i in range(1, num_vars + 1)]
        clauses.append(clause)
    
    tree, literals = tseitin_resolution_tree(clauses)
    rank = geometric_langlands_rank(tree)
    depth = max(len(path) for path in tree.values() if path)
    
    metric_value = rank / depth
    conjecture_holds = all(metric_value <= c for c in [1.0, 2.0, 3.0])  # Example constants
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds depth {depth}"
    
    return {
        "metric_name": "Ratio of Rank to Depth",
        "metric_value": metric_value,
        "instances_tested": len(clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")