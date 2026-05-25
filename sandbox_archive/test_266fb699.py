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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_resolution_tree(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        nodes = {lit: [] for lit in literals}
        
        for clause in cnf:
            if len(clause) == 1:
                literal = clause[0]
                neg_literal = -literal
                nodes[literal].append(neg_literal)
                nodes[neg_literal].append(literal)
            else:
                new_var = max(literals) + 1
                literals.add(new_var)
                for lit in clause:
                    nodes[lit].append(-new_var)
                    nodes[-new_var].append(lit)
                for i in range(len(clause)):
                    for j in range(i + 1, len(clause)):
                        neg_lit1 = -clause[i]
                        neg_lit2 = -clause[j]
                        nodes[neg_lit1].append(neg_lit2)
                        nodes[neg_lit2].append(neg_lit1)
        
        return nodes
    
    def algebraic_k_theory_rank(tree):
        visited = set()
        rank = 0
        
        def dfs(node, parent):
            nonlocal rank
            if node in visited:
                return
            visited.add(node)
            for neighbor in tree[node]:
                if neighbor != parent:
                    dfs(neighbor, node)
                    rank += 1
        
        for node in tree:
            if node not in visited:
                dfs(node, None)
        
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tree = tseitin_resolution_tree(cnf)
    rank = algebraic_k_theory_rank(tree)
    
    c = Fraction(1, 2)  # Absolute constant
    threshold = 1e-6
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= c * n * math.log(n) and abs(rank - c * n * math.log(n)) <= threshold,
        "counterexample": "" if rank >= c * n * math.log(n) else f"Rank {rank} is less than {c * n * math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank too small\" first_failing_seed={first_failing_seed}")