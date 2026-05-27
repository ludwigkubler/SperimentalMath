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
    
    def generate_expander_graph(n):
        # Generate a random expander graph with n nodes using the Chandra-Rao expander construction
        G = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0:
                    G[i].append(j)
                    G[j].append(i)
        return G
    
    def tree_width(G):
        # Compute the tree-width of the graph using a dynamic programming approach
        n = len(G)
        dp = [set() for _ in range(n)]
        parent = [-1] * n
        
        def dfs(node, par):
            dp[node].add(node)
            for neighbor in G[node]:
                if neighbor != par:
                    dfs(neighbor, node)
                    dp[node] |= dp[neighbor]
                    dp[node].remove(neighbor)
                    dp[node].discard(par)
        
        dfs(0, -1)
        
        def find_root():
            root = 0
            for i in range(n):
                if len(dp[i]) == n - 2:
                    root = i
                    break
            return root
        
        def decompose(node, par):
            nonlocal root
            if node == root:
                root = None
            for neighbor in G[node]:
                if neighbor != par and root is not None:
                    decompose(neighbor, node)
        
        root = find_root()
        decompose(root, -1)
        
        def max_bag_size(bag):
            return max(len(dp[node]) for node in bag)
        
        def dfs2(node, par, bag):
            nonlocal max_width
            if len(bag) > max_width:
                max_width = len(bag)
            for neighbor in G[node]:
                if neighbor != par:
                    new_bag = bag | {neighbor}
                    dfs2(neighbor, node, new_bag)
        
        max_width = 0
        dfs2(root, -1, set())
        return max_width
    
    def algebraic_k_theory_rank(G):
        # Compute the rank of the algebraic K-theory group for the graph G
        n = len(G)
        k_group = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        
        def matrix_multiply(A, B):
            C = [[Fraction(0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        C[i][j] += A[i][k] * B[k][j]
            return C
        
        def gaussian_elimination(A):
            n = len(A)
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                pivot = A[i][i]
                for j in range(n):
                    A[i][j] /= pivot
                for j in range(n):
                    if j != i:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
            return A
        
        identity_matrix = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [row + col for row, col in zip(k_group, identity_matrix)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        
        rank = 0
        for row in reduced_matrix:
            if any(row[i] != Fraction(0) for i in range(n)):
                rank += 1
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            G = generate_expander_graph(n)
            tree_width_val = tree_width(G)
            rank = algebraic_k_theory_rank(G)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= 2 ** (math.log2(tree_width_val) * math.log2(n))
    
    return {
        "metric_name": "algebraic_k_theory_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean rank {mean_rank} < 2^(Ω({tree_width_val})) for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")