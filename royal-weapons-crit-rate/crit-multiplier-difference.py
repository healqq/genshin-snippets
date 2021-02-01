from mpl_toolkits.mplot3d import Axes3D
import os
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from index import get_effective_crit_value

def get_crit_multi(crit_damage, crit_value):
  return (1 + crit_damage) * crit_value + (1 - crit_value) * 1

def main():
  crit_damage_values = np.arange(0.5, 2.5, 0.05)
  crit_values = np.arange(0.05, 1, 0.05)
  
  crit_multi_diff = np.zeros((np.shape(crit_damage_values)[0], np.shape(crit_values)[0]))

  effective_crit_values = get_effective_crit_value(crit_values)

  for i in range(crit_damage_values.shape[0]):
    for j in range(crit_values.shape[0]): 
      crit_multi_diff[i][j] = get_crit_multi(crit_damage_values[i] + 0.57,effective_crit_values[j]) - get_crit_multi(crit_damage_values[i], crit_values[j] + 0.57 / 2)
  
  X, Y = np.meshgrid(crit_damage_values, crit_values, indexing='ij')

  fig = plt.figure(1)
  ax = fig.gca(projection='3d')

  surf = ax.plot_surface(X * 100, Y * 100, crit_multi_diff, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False, vmin=-0.4,vmax=0.4)

  fig.colorbar(surf, shrink=0.5, aspect=5)
  fig.title('Crit multi difference for crit rate / crit damage setup')

  ax.set_xlabel('Crit damage value, %')
  ax.set_ylabel('Crit rate value, %')
  ax.set_zlabel('Crit multi diff')
  ax.set_zlim(-1, 1)
  ax.view_init(20, -140)
  plt.show()


if __name__ == "__main__":
    main()
