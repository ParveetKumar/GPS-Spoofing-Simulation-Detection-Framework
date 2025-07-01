import math

def free_space_path_loss(frequency_ghz, distance_km):
    return 20 * math.log10(distance_km) + 20 * math.log10(frequency_ghz) + 92.45

def calculate_link_budget(P_t, G_t, G_r, frequency_ghz, distance_km, L_m):
    L_fs = free_space_path_loss(frequency_ghz, distance_km)
    P_r = P_t + G_t + G_r - L_fs - L_m
    return P_r

def calculate_CNo(P_r_dBW, system_temp_K=290):
    k = 1.38e-23  # Boltzmann constant
    N0 = 10 * math.log10(k * system_temp_K)
    return P_r_dBW - N0, N0

# Example: points in the transmission chain
transmission_points = [
    {"name": "Space Segment", "P_t": 13, "G_t": 13, "G_r": 0, "freq": 1.57542, "dist": 500, "L_m": 1},
    {"name": "Mid Orbit",      "P_t": 13, "G_t": 13, "G_r": 0, "freq": 1.57542, "dist": 10000, "L_m": 1.5},
    {"name": "Earth Receiver", "P_t": 13, "G_t": 13, "G_r": -3, "freq": 1.57542, "dist": 20200, "L_m": 2},
]

for point in transmission_points:
    P_r = calculate_link_budget(point["P_t"], point["G_t"], point["G_r"],
                                 point["freq"], point["dist"], point["L_m"])
    CNo, N0 = calculate_CNo(P_r)
    print(f"\n--- {point['name']} ---")
    print(f"Received Power: {P_r:.2f} dBW")
    print(f"Noise Density:  {N0:.2f} dBW/Hz")
    print(f"C/N0:           {CNo:.2f} dB-Hz")


def required_spoofing_power(P_r_real, spoof_distance_km, freq_ghz, G_t, G_r, L_m, margin_dB=10):
    P_r_spoof = P_r_real + margin_dB
    L_fs_spoof = free_space_path_loss(freq_ghz, spoof_distance_km)
    P_t_spoof = P_r_spoof - G_t - G_r + L_fs_spoof + L_m
    return P_t_spoof

# Example: Spoof from 0.1 km (100 m) away
spoof_distance_km =5
G_t_spoofer = 5
G_r_receiver = -3
L_m_spoofer = 1
margin_dB = 10

P_r_real = calculate_link_budget(13, 13, -3, 1.57542, 20200, 2)  # Earth receiver

P_t_needed = required_spoofing_power(P_r_real, spoof_distance_km, 1.57542,
                                      G_t_spoofer, G_r_receiver, L_m_spoofer, margin_dB)

print(f"\nRequired spoofing transmit power: {P_t_needed:.2f} dBW")
