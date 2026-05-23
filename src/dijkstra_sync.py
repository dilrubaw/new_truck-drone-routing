import heapq
import numpy as np
from models import TDTLInstance

def build_sync_graph(tsp_route: list, instance: TDTLInstance):
    """
    Makale Algoritma 2 (Set A' construction):
    Düğüm çiftleri arasında batarya sınırına uyan senkronizasyon yaylarını kurar.
    """
    n = instance.n
    t_T = instance.truck_time_matrix
    t_D = instance.drone_time_matrix
    Q = instance.Q
    
    # G' grafı: adj_list[i] = [(komşu_j, kenar_maliyeti), ...]
    adj_list = {i: [] for i in tsp_route}
    
    # Rota üzerindeki tüm i ve j çiftlerini kontrol et (i < j)
    for i_idx in range(len(tsp_route) - 1):
        for j_idx in range(i_idx + 1, len(tsp_route)):
            i = tsp_route[i_idx]
            j = tsp_route[j_idx]
            
            # Kamyonun i'den j'ye direkt gitme süresi
            truck_time = t_T[i][j]
            
            # Drone'un TSP rotası üzerindeki i ve j arasındaki düğümleri gezme süresi
            drone_time = 0.0
            current = i
            for k_idx in range(i_idx + 1, j_idx + 1):
                next_node = tsp_route[k_idx]
                drone_time += t_D[current][next_node]
                current = next_node
                
            # Eğer drone'un bu alt rotayı tamamlamaya bataryası yetiyorsa arka izin ver var
            if drone_time <= Q:
                # PARALEL HAREKET: Geçiş süresi ikisinin maksimumudur
                edge_cost = max(truck_time, drone_time)
                adj_list[i].append((j, edge_cost))
            else:
                # Batarya yetmiyorsa, j_idx daha da büyüdükçe süre artacağından döngüden çıkılabilir
                break
                
    return adj_list

def run_dijkstra(adj_list: dict, start: int, end: int):
    """En kısa senkronizasyon yolunu ve atılan adımları bulur."""
    queue = [(0.0, start, [start])]
    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0.0
    
    while queue:
        (cost, current, path) = heapq.heappop(queue)
        
        if current == end:
            return cost, path
            
        if cost > distances[current]:
            continue
            
        for neighbor, edge_cost in adj_list[current]:
            old_cost = distances[neighbor]
            new_cost = cost + edge_cost
            if new_cost < old_cost:
                distances[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
                
    return float('inf'), []