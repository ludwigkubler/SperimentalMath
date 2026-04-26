import random
import math
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def cheeger_constant(G, n):
        edges = sum(len(neighbors) for neighbors in G) // 2
        min_cut = float('inf')
        for node in range(n):
            cut_size = sum(1 for neighbor in G[node] if random.random() < 0.5)
            min_cut = min(min_cut, cut_size)
        return 2 * min_cut / n
    
    def tseitin_formula(G, n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for node in range(n):
            clauses.append([literals[node]])
            for neighbor in G[node]:
                if neighbor < node:
                    continue
                clauses.append([-literals[node], literals[neighbor]])
                clauses.append([-literals[neighbor], literals[node]])
        return clauses
    
    def resolution_width(clauses, n):
        literals = set()
        for clause in clauses:
            literals.update(clause)
        literals = sorted(literals)
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clauses = [c[0] for c in clauses if len(c) == 1]
            pure_literals = {l: (all(l not in a for a in clauses) or all(-l not in a for a in clauses)) for l in literals}
            
            if unit_clauses:
                literal = unit_clauses[0]
                assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(new_clauses, assignment)
            
            if pure_literals:
                literal = next(l for l, p in pure_literals.items() if p)
                assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(new_clauses, assignment)
            
            literal = literals[0]
            remaining_literals = literals[1:]
            assignment[literal] = True
            if dpll(clauses, assignment):
                return True
            assignment[literal] = False
            for l in remaining_literals:
                assignment[l] = True
                if dpll(clauses, assignment):
                    return True
                assignment[l] = False
            return False
        
        max_width = 0
        for _ in range(100):  # Sample multiple assignments to estimate width
            assignment = {l: random.choice([True, False]) for l in literals}
            queue = [c for c in clauses if any(l in c or -l in c for l in assignment)]
            current_width = len(queue)
            while queue:
                clause = queue.pop()
                literal = next(l for l in clause if l in assignment and not assignment[l])
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        new_clauses.append([l for l in c if l != literal])
                    elif -literal in c:
                        new_clauses.append([l for l in c if l != -literal])
                queue.extend(new_clauses)
                current_width = max(current_width, len(queue))
            max_width = max(max_width, current_width)
        return max_width
    
    n = 20
    d = 3
    G = [[] for _ in range(n)]
    for i in range(n):
        neighbors = random.sample(range(n), d - 1)
        while any(j in G[j] for j in neighbors):
            neighbors = random.sample(range(n), d - 1)
        G[i].extend(neighbors)
        for neighbor in neighbors:
            if neighbor < i:
                continue
            G[neighbor].append(i)
    
    h = cheeger_constant(G, n)
    clauses = tseitin_formula(G, n)
    width = resolution_width(clauses, n)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 1 / h,
        "counterexample": "" if width >= 1 / h else f"Width {width} < 1/φ={1/h}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {json.dumps(result)}")
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")