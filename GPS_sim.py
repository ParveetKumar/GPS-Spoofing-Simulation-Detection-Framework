# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def trilaterate(sat_positions, distances):
#     P0 = sat_positions[0]
#     d0 = distances[0]

#     A = []
#     b = []
#     for i in range(1, len(sat_positions)):
#         Pi = sat_positions[i]
#         di = distances[i]
#         A_row = 2 * (Pi - P0)
#         A.append(A_row)
#         b_val = d0**2 - di**2 - np.dot(P0, P0) + np.dot(Pi, Pi)
#         b.append(b_val)

#     x, residuals, rank, _ = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)
#     return x

# # Speed of light in m/s
# c = 299_792_458

# # Satellite positions (in meters)
# satellites = np.array([
#     [15600000, 7540000, 20140000],
#     [18760000, 2750000, 18610000],
#     [17610000, 14630000, 13480000],
#     [19170000, 6100000, 18390000]
# ])

# # True receiver position (ground truth)
# true_position = np.array([15000000, 5000000, 60350])

# # Simulate true distances from satellites to receiver
# true_distances = np.linalg.norm(satellites - true_position, axis=1)

# # Add Gaussian noise (e.g., std = 10 meters)
# noise_std = 10  # Adjust this to simulate more or less noise
# noise = np.random.normal(0, noise_std, size=true_distances.shape)
# simulated_distances = true_distances + noise

# # Estimate position from noisy measurements
# estimated_position = trilaterate(satellites, simulated_distances)

# # Print results
# print("True position:     ", true_position)
# print("Estimated position:", estimated_position)
# print("Position error:    ", np.linalg.norm(estimated_position - true_position), "meters")

# # Optional 3D Visualization
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(satellites[:,0], satellites[:,1], satellites[:,2], c='blue', label='Satellites')
# ax.scatter(true_position[0], true_position[1], true_position[2], c='yellow', label='True Position')
# ax.scatter(estimated_position[0], estimated_position[1], estimated_position[2], c='red', label='Estimated Position')
# ax.set_xlabel('X (m)')
# ax.set_ylabel('Y (m)')
# ax.set_zlabel('Z (m)')
# ax.set_title("Trilateration Simulation")
# ax.legend()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def trilaterate(sat_positions, distances):
    P0 = sat_positions[0]
    d0 = distances[0]

    A = []
    b = []
    for i in range(1, len(sat_positions)):
        Pi = sat_positions[i]
        di = distances[i]
        A_row = 2 * (Pi - P0)
        A.append(A_row)
        b_val = d0**2 - di**2 - np.dot(P0, P0) + np.dot(Pi, Pi)
        b.append(b_val)

    x, residuals, rank, _ = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)
    return x

# Constants
c = 299792458  # Speed of light in m/s
earth_radius = 6371000  # Earth radius in meters

# More realistic GPS satellite positions (in meters) - approximately 20,000 km altitude
# These are in ECEF (Earth-Centered, Earth-Fixed) coordinates
satellites = np.array([
    [20_000_000, 0, 0],               # Satellite along x-axis
    [0, 20_000_000, 0],               # Satellite along y-axis
    [0, 0, 20_000_000],               # Satellite along z-axis
    [14_142_135, 14_142_135, 0],      # Satellite in xy-plane
    [14_142_135, 0, 14_142_135],      # Satellite in xz-plane
    [0, 14_142_135, 14_142_135]       # Satellite in yz-plane
])

# True receiver position on Earth's surface (latitude ~40°, longitude ~-75°)
# Converted to ECEF coordinates
lat = np.radians(40.0)
lon = np.radians(-75.0)
true_position = np.array([
    earth_radius * np.cos(lat) * np.cos(lon),
    earth_radius * np.cos(lat) * np.sin(lon),
    earth_radius * np.sin(lat)
])

# Simulate true distances from satellites to receiver
true_distances = np.linalg.norm(satellites - true_position, axis=1)

# Add realistic GPS measurement noise (1-10 meters is typical for civilian GPS)
noise_std = 5  # meters
noise = np.random.normal(0, noise_std, size=true_distances.shape)
simulated_distances = true_distances + noise

# Estimate position from noisy measurements
estimated_position = trilaterate(satellites[:4], simulated_distances[:4])  # Use first 4 satellites

# Print results
print("True position:     ", true_position)
print("Estimated position:", estimated_position)
print("Position error:    ", np.linalg.norm(estimated_position - true_position), "meters")

# Convert back to lat/lon for verification
x, y, z = estimated_position
estimated_lon = np.degrees(np.arctan2(y, x))
estimated_lat = np.degrees(np.arctan2(z, np.sqrt(x**2 + y**2)))
print(f"Estimated lat/lon: {estimated_lat:.6f}°, {estimated_lon:.6f}°")

# Optional 3D Visualization
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot Earth surface
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_earth, y_earth, z_earth, color='blue', alpha=0.1)

# Plot satellites and positions
ax.scatter(satellites[:,0], satellites[:,1], satellites[:,2], c='black', label='GPS Satellites', s=50)
ax.scatter(true_position[0], true_position[1], true_position[2], c='yellow', label='True Position', s=100)
ax.scatter(estimated_position[0], estimated_position[1], estimated_position[2], c='Red', label='Estimated Position', s=100)

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title("GPS Trilateration Simulation")
ax.legend()
plt.tight_layout()
plt.show()