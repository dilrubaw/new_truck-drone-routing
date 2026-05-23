from models import TDTLInstance
from two_opt import run_2opt_tsp
from dijkstra_sync import build_sync_graph, run_dijkstra

def generate_paper8_baseline(instance: TDTLInstance):
    """
    Paper 8 standartlarında koda dökülmüş ilk uygun çözümü (pi_s, pi_t) üretir.
    """
    # Adım 1: TSP Rotasını Çıkar
    tsp_route = run_2opt_tsp(instance)
    
    # Adım 2: Senkronizasyon Grafını Kur (Batarya Kontrollü)
    adj_list = build_sync_graph(tsp_route, instance)
    
    # Adım 3: Dijkstra ile En Kısa Makespan Yolunu Seç
    baseline_makespan, sync_nodes = run_dijkstra(adj_list, instance.origin, instance.destination)
    
    if baseline_makespan == float('inf'):
        raise ValueError("Hata: Bu batarya kapasitesi (Q) ile uygun bir senkronizasyon rotası bulunamadı!")
        
    # Adım 4: Çıktıyı Makale Standart Matrisine Dönüştür (pi_s ve pi_t)
    # pi_s: Düğümlerin ziyaret sırası
    pi_s = tsp_route[:]
    
    # pi_t: Kaynak Tipi [0: İkisi birden/Rendezvous, 1: Sadece Drone, 2: Sadece Kamyon]
    pi_t = []
    sync_set = set(sync_nodes)
    
    for node in pi_s:
        if node in sync_set:
            pi_t.append(0) # Senkronizasyon noktası (Kamyon ve Drone buluşuyor)
        else:
            pi_t.append(1) # Sadece drone'un uğradığı ara düğüm
            
    # Yapısal Dönüşüm Detayları için Sözlük Oluştur
    drone_assignments = {}
    for i in range(len(sync_nodes) - 1):
        A = sync_nodes[i]
        B = sync_nodes[i+1]
        
        # TSP rotasında A ile B arasında kalanlar drone'a atanmıştır
        a_idx = tsp_route.index(A)
        b_idx = tsp_route.index(B)
        drone_assignments[(A, B)] = tsp_route[a_idx+1 : b_idx]
        
    return {
        "makespan": baseline_makespan,
        "pi_s": pi_s,
        "pi_t": pi_t,
        "sync_nodes": sync_nodes,
        "drone_assignments": drone_assignments
    }