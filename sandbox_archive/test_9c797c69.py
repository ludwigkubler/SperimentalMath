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
    
    def generate_k_cnf(n, clause_density):
        num_clauses = int(clause_density * n * (n - 1))
        clauses = []
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        
        while len(clauses) < num_clauses:
            clause = random.sample(literals, 2)
            if clause not in clauses and -clause[0] not in clauses and -clause[1] not in clauses:
                clauses.append(clause)
        
        return clauses
    
    def construct_constraint_graph(clauses):
        n = len(clauses) // (n - 1)
        graph = [[0] * n for _ in range(n)]
        
        for clause in clauses:
            lit1, lit2 = abs(clause[0]) - 1, abs(clause[1]) - 1
            if 0 <= lit1 < n and 0 <= lit2 < n:
                graph[lit1][lit2] = 1
                graph[lit2][lit1] = 1
        
        return graph
    
    def isometric_embedding(graph):
        # Simple heuristic embedding for demonstration purposes
        n = len(graph)
        embedding = {}
        
        for i in range(n):
            embedding[i] = (random.random(), random.random())
        
        return embedding
    
    def hyperbolic_volume(embedding):
        n = len(embedding)
        volume = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = math.sqrt((embedding[i][0] - embedding[j][0]) ** 2 + (embedding[i][1] - embedding[j][1]) ** 2)
                if dist > 0:
                    volume += math.log(dist)
        
        return volume
    
    def check_bound(volume, n, c):
        return volume <= n ** (1 + c)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clause_density = random.uniform(0.1, 0.9)
            clauses = generate_k_cnf(n, clause_density)
            graph = construct_constraint_graph(clauses)
            embedding = isometric_embedding(graph)
            volume = hyperbolic_volume(embedding)
            
            results.append({
                "n": n,
                "clause_density": clause_density,
                "volume": volume
            })
    
    total_volumes = sum(result["volume"] for result in results)
    mean_volume = Fraction(total_volumes, len(results))
    std_volume = math.sqrt(sum((result["volume"] - mean_volume) ** 2 for result in results) / len(results))
    
    c = 0.1
    support_fraction = sum(1 for result in results if check_bound(result["volume"], result["n"], c)) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hyperbolic Volume",
        "metric_value": float(mean_volume),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_volumes = sum(result["metric_value"] for result in results)
    mean_volume = Fraction(total_volumes, len(results))
    std_volume = math.sqrt(sum((result["metric_value"] - mean_volume) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_volume} std={std_volume} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")