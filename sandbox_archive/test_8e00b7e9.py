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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def poset_dimension(clauses):
        variables = set(abs(v) for v in sum(clauses, []))
        poset = {v: set() for v in variables}
        
        for clause in clauses:
            for i in range(3):
                for j in range(i + 1, 3):
                    if clause[i] > 0 and clause[j] < 0 or clause[i] < 0 and clause[j] > 0:
                        poset[abs(clause[i])].add(abs(clause[j]))
                        poset[abs(clause[j])].add(abs(clause[i]))
        
        def dfs(v, visited):
            if v in visited:
                return len(visited)
            visited.add(v)
            return max(dfs(w, visited) for w in poset[v] if w not in visited) + 1
        
        return max(dfs(v, set()) for v in variables)
    
    def karchmer_wigderson_communication_complexity(poset):
        n = len(poset)
        if n == 0:
            return 0
        min_clauses = float('inf')
        
        def dfs(node, visited, path):
            nonlocal min_clauses
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            
            if len(path) > min_clauses:
                return
            
            for neighbor in poset[node]:
                dfs(neighbor, visited, path)
            
            if len(path) < min_clauses:
                min_clauses = len(path)
            
            path.pop()
            visited.remove(node)
        
        for start_node in poset:
            dfs(start_node, set(), [])
        
        return min_clauses
    
    n = random.randint(5, 40)
    cnf = generate_3cnf(n)
    dimension = poset_dimension(cnf)
    communication_complexity = karchmer_wigderson_communication_complexity({i: {j for j in range(1, n + 1) if i != j} for i in range(1, n + 1)})
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": communication_complexity == dimension,
        "counterexample": "" if communication_complexity == dimension else f"Graph with n={n}, A=[{', '.join(map(str, cnf))}]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unexpected_behavior")