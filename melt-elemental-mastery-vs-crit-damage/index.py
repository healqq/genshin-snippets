from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

BASE_DAMAGE = 1000
CRIT_RATE = 1.0

# https://genshin-impact.fandom.com/wiki/Elemental_Mastery#:~:text=Elemental%20Mastery%20is%20an%20attribute,Shattered%2C%20Swirl%2C%20and%20Crystallize.
def get_melt_effect(elemental_mastery):
  return 1 + 2.78 * elemental_mastery / (1400 + elemental_mastery)

def get_damage_value(elemental_mastery, crit_damage):
  return (BASE_DAMAGE * 
  # crit calculation including crit rate
  (1 + crit_damage) * CRIT_RATE + BASE_DAMAGE * (1 - CRIT_RATE)) * get_melt_effect(elemental_mastery) * 2

def crit_damage_to_em_ratio(crit_damage_value):
  return crit_damage_value / 0.07 * 20
def main():
  crit_damage_values = np.arange(0.5, 2.5, 0.05)
  elemental_mastery_values = np.arange(0, 200, crit_damage_to_em_ratio(0.05))
  results = np.zeros((np.shape(crit_damage_values)[0], np.shape(elemental_mastery_values)[0]))
  for i in range(crit_damage_values.shape[0]):
    for j in range(elemental_mastery_values.shape[0]): 
      results[i][j] = get_damage_value(elemental_mastery_values[j], crit_damage_values[i])
  
  X, Y = np.meshgrid(crit_damage_values, elemental_mastery_values, indexing='ij')
  fig = plt.figure()
  ax = fig.gca(projection='3d')

  print(np.shape(X))
  print(np.shape(Y))
  print(np.shape(results))
  surf = ax.plot_surface(X * 100, Y, results, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

  plt.colorbar(surf, shrink=0.5, aspect=5)
  plt.title('effect of EM and Crit for melt damage, {crit:d}% crit rate'.format(crit=int(CRIT_RATE * 100)))
  ax.set_xlabel('Crit damage value, %')
  ax.set_ylabel('Elemental mastery')
  ax.set_zlabel('Damage')
  plt.show()


if __name__ == "__main__":
    main()
