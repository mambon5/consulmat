# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:12:55 2025

@author: ruthv
"""
from ortools.sat.python import cp_model

def schedule_workers(communities, cleaning_times, worker_assignments, workers=35, min_time=7, max_time=8, monthly_hours=40):
    model = cp_model.CpModel()
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    num_days = len(days)
    num_communities = len(communities)
    weeks_per_month = 4  # Assuming a 4-week month
    
    # Variables: X[w][c][d][wk] -> 1 if worker w cleans community c on day d of week wk, else 0
    X = {}
    for w in range(workers):
        for c in worker_assignments[w]:
            for d in range(len(days)):
                for wk in range(weeks_per_month):
                    X[w, c, d, wk] = model.NewBoolVar(f"X_{w}_{c}_{d}_{wk}")
    
    # Ensure each community is cleaned the required number of days per week
    for c, freq in communities.items():
        for wk in range(weeks_per_month):
            model.Add(sum(X[w, c, d, wk] for w in range(workers) for d in range(num_days) if (w, c, d, wk) in X) == freq)
    
    # Total working time constraints per worker per day
    for w in range(workers):
        for d in range(num_days):
            for wk in range(weeks_per_month):
                total_time = sum(X[w, c, d, wk] * cleaning_times[c] for c in worker_assignments[w] if (w, c, d, wk) in X)
                model.Add(total_time >= min_time)
                model.Add(total_time <= max_time)
    
    # Monthly work hour constraint per worker
    for w in range(workers):
        total_monthly_time = sum(X[w, c, d, wk] * cleaning_times[c] for c in worker_assignments[w] for d in range(num_days) for wk in range(weeks_per_month) if (w, c, d, wk) in X)
        model.Add(total_monthly_time <= monthly_hours * weeks_per_month)
    
    # Objective: Minimize the number of different days a worker has to travel
    model.Minimize(sum(X[w, c, d, wk] for w in range(workers) for c in worker_assignments[w] for d in range(num_days) for wk in range(weeks_per_month) if (w, c, d, wk) in X))
    
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule = {f"Week {wk+1}": {day: {w: [] for w in range(workers)} for day in days} for wk in range(weeks_per_month)}
        for w in range(workers):
            for c in worker_assignments[w]:
                for d in range(num_days):
                    for wk in range(weeks_per_month):
                        if (w, c, d, wk) in X and solver.Value(X[w, c, d, wk]) == 1:
                            schedule[f"Week {wk+1}"][days[d]][w].append(f"Community {c+1}")
        return schedule
    else:
        return "No feasible solution found"

# Example Usage
communities = {0: 1, 1: 2, 2: 3, 3: 5, 4: 6, 5: 1, 6: 2, 7: 3, 8: 5, 9: 6}
cleaning_times = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6}
worker_assignments = {w: [w % 10] for w in range(35)}  # Assigning each worker to a specific community
print(schedule_workers(communities, cleaning_times, worker_assignments))
