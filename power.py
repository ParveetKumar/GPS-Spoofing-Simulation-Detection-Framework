import math

def free_space_path_loss(frequency_ghz, distance_km):
    return 20 * math.log10(distance_km) + 20 * math.log10(frequency_ghz) + 92.45

def calculate_link_budget(P_t, G_t, G_r, frequency_ghz, distance_km, L_m):
    L_fs = free_space_path_loss(frequency_ghz, distance_km)
    P_r = P_t + G_t + G_r - L_fs - L_m
    return P_r

def calculate_CNo(P_r_dBW, system_temp_K=290):
    k = 1.38e-23  # Boltzmann constant
    N0 = 10 * math.log10(k * system_temp_K)  # in dBW/Hz
    CNo = P_r_dBW - N0
    return CNo, N0

# GPS L1 parameters
P_t = 13             # dBW
G_t = 13             # dB
G_r = -3             # dB (typical GPS receiver)
frequency = 1.57542  # GHz
distance = 20200     # km
L_m = 2              # dB (losses)
T_sys = 290          # K (standard)

# Link budget
P_r = calculate_link_budget(P_t, G_t, G_r, frequency, distance, L_m)

# C/N0
CNo, N0 = calculate_CNo(P_r, T_sys)

print(f"Received Power (P_r): {P_r:.2f} dBW")
print(f"Noise Power Density (N0): {N0:.2f} dBW/Hz")
print(f"Carrier-to-Noise Density Ratio (C/N0): {CNo:.2f} dB-Hz")
