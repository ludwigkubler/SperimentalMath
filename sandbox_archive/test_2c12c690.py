import random
import math
from itertools import combinations, product

def generate_3cnf(n: int, m: int) -> list:
    literals = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = {random.choice(literals), random.choice(literals)}
        while len(clause) != 3:
            clause.add(random.choice(literals))
        clauses.append(clause)
    return clauses

def is_clause_compatible(c1, c2):
    return not (c1 & c2)

def construct_simplicial_complex(clauses):
    simplices = {frozenset([i]) for i in range(1, len(clauses) + 1)}
    edges = set()
    for i, j in combinations(range(len(clauses)), 2):
        if is_clause_compatible(clauses[i], clauses[j]):
            edges.add(frozenset([i + 1, j + 1]))
    simplicial_complex = {'vertices': simplices, 'edges': edges}
    return simplicial_complex

def find_minimal_covering(simplicial_complex):
    vertices = list(simplicial_complex['vertices'])
    edges = list(simplicial_complex['edges'])
    
    def is_covered(cover):
        for edge in edges:
            if not any(vertex in cover for vertex in edge):
                return False
        return True
    
    min_cover_size = float('inf')
    best_cover = None
    
    for r in range(1, len(vertices) + 1):
        for cover in combinations(vertices, r):
            if is_covered(cover):
                if len(cover) < min_cover_size:
                    min_cover_size = len(cover)
                    best_cover = cover
                    break
        if min_cover_size == r:
            break
    
    return min_cover_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10 + (seed % 4) * 3  # Sweep n ∈ {5,8,11,14}
    m = 2 * n
    
    clauses = generate_3cnf(n, m)
    simplicial_complex = construct_simplicial_complex(clauses)
    
    category = find_minimal_covering(simplicial_complex)
    
    # Naive DPLL implementation to compute decision tree depth
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = list(unit_clause)[0]
            if literal in assignment and assignment[literal] != (literal > 0):
                return False
            assignment[literal] = literal > 0
            return dpll([c for c in clauses if literal not in c], assignment)
        
        literal = next((l for l in range(1, n + 1) if l not in assignment), None)
        assignment[literal] = True
        if dpll(clauses, assignment):
            return True
        assignment[literal] = False
        if dpll(clauses, assignment):
            return True
        del assignment[literal]
        return False
    
    def decision_tree_depth(clauses):
        assignment = {}
        depth = 0
        
        def backtrack(depth):
            nonlocal assignment
            if not clauses:
                return depth
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = list(unit_clause)[0]
                if literal in assignment and assignment[literal] != (literal > 0):
                    return -1
                assignment[literal] = literal > 0
                depth += 1
                result = backtrack(depth)
                if result == -1:
                    del assignment[literal]
                    return -1
                else:
                    return result
            
            literal = next((l for l in range(1, n + 1) if l not in assignment), None)
            assignment[literal] = True
            depth += 1
            result = backtrack(depth)
            if result == -1:
                del assignment[literal]
                depth -= 1
                assignment[literal] = False
                depth += 1
                result = backtrack(depth)
                if result == -1:
                    del assignment[literal]
                    return -1
                else:
                    return result
        
        return backtrack(depth)
    
    decision_tree_depth_value = decision_tree_depth(clauses)
    
    conjecture_holds = category <= decision_tree_depth_value
    counterexample = "" if conjecture_holds else f"category={category}, depth={decision_tree_depth_value}"
    
    return {
        "metric_name": "Decision Tree Depth",
        "metric_value": decision_tree_depth_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        result = f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE mapping_undefined"
    
    print(result)