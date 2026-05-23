import numpy as np

# Yazılımcı 1'in Modülleri
from models import TDTLInstance
from distance_matrix import calculate_tdtl_matrices
from evaluator import calculate_battery_capacity

# Yazılımcı 2'nin Başlangıç/Baseline Modülü
from paper8_ig_sa import generate_paper8_baseline

def run_project_test():
    print("=== TDTL PROJESİ TEST MOTORU BAŞLATILDI ===\n")

    # 1. TEST VERİSİ: Bouman veri kümesini simüle eden 10 düğümlü koordinat matrisi
    sample_coords = np.array([
        [0.0, 0.0],     # Node 0 (Origin / Depot)
        [10.0, 20.0],   # Node 1
        [15.0, 45.0],   # Node 2
        [30.0, 10.0],   # Node 3
        [50.0, 50.0],   # Node 4
        [65.0, 80.0],   # Node 5
        [70.0, 15.0],   # Node 6
        [85.0, 90.0],   # Node 7
        [90.0, 20.0],   # Node 8
        [100.0, 100.0]  # Node 9 (Destination)
    ])

    # 2. INSTANCE OLUŞTURMA: Hız Oranı alpha = 2.0 seçilsin (v_D / v_T = 2)
    instance = TDTLInstance(name="Uniform_10_Nodes", nodes=sample_coords, alpha=2.0)
    print(f"[Yazılımcı 1] Veri Modeli Oluşturuldu: {instance.name}")

    # 3. MATRİS HESAPLAMA: Saf Euclidean mesafeler çıkartılıyor
    instance = calculate_tdtl_matrices(instance)
    print("[Yazılımcı 1] Kamyon ve Drone süre matrisleri Euclidean kurallarına göre hesaplandı.")

    # 4. DİNAMİK BATARYA (Q) HESAPLAMA: Makale Sayfa 16'daki orijinal formül
    Q_value = calculate_battery_capacity(instance)
    print(f"[Yazılımcı 1] Orijinal formüle göre hesaplanan dinamik batarya (Q): {Q_value:.4f}\n")

    # 5. YAZILIMCI 2 BASELINE ALGORİTMASINI TETİKLEME
    print("[Yazılımcı 2] 2-opt TSP ve Dijkstra Senkronizasyon mekanizması başlatılıyor...")
    baseline_result = generate_paper8_baseline(instance)

    # 6. SONUÇLARI EKRANA YAZDIRMA (Doğrulama Adımı)
    print("\n=============================================")
    print("--- PAPER 8 BASELINE ALGORİTMA SONUÇLARI ---")
    print("=============================================")
    print(f"Hesaplanan Hedef Makespan (Süre): {baseline_result['makespan']:.4f}")
    print(f"Kamyonun Uğrayacağı Senkronizasyon Noktaları (Kamyon Rotası): {baseline_result['sync_nodes']}")
    print("\nKamyon Kenarlarına Göre Drone Dağılımları:")
    for edge, drone_nodes in baseline_result['drone_assignments'].items():
        print(f"  -> Kamyon {edge} arasındayken Drone'un uğrayacağı ara müşteriler: {drone_nodes}")
    print("=============================================\n")

if __name__ == "__main__":
    run_project_test()