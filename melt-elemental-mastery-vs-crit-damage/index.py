from mpl_toolkits.mplot3d import Axes3D
import os
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

BASE_DAMAGE = 1000

# https://genshin-impact.fandom.com/wiki/Elemental_Mastery#:~:text=Elemental%20Mastery%20is%20an%20attribute,Shattered%2C%20Swirl%2C%20and%20Crystallize.
def get_melt_effect(elemental_mastery):
  return 1 + 2.78 * elemental_mastery / (1400 + elemental_mastery)

def get_damage_value(elemental_mastery, crit_damage, crit_rate):
  return (BASE_DAMAGE * 
  # crit calculation including crit rate
  (1 + crit_damage) * crit_rate + BASE_DAMAGE * (1 - crit_rate)) * get_melt_effect(elemental_mastery) * 2

def crit_damage_to_em_ratio(crit_damage_value):
  return crit_damage_value / 0.07 * 20

def generate_plot_for_crit_rate(crit_rate):
  crit_damage_values = np.arange(0.5, 2.5, 0.05)
  elemental_mastery_values = np.arange(0, crit_damage_to_em_ratio(2.5), crit_damage_to_em_ratio(0.05))
  results = np.zeros((np.shape(crit_damage_values)[0], np.shape(elemental_mastery_values)[0]))
  for i in range(crit_damage_values.shape[0]):
    for j in range(elemental_mastery_values.shape[0]): 
      results[i][j] = get_damage_value(elemental_mastery_values[j], crit_damage_values[i], crit_rate)
  
  X, Y = np.meshgrid(crit_damage_values, elemental_mastery_values, indexing='ij')
  
  fig = plt.figure(num=crit_rate)
  ax = fig.gca(projection='3d')

  surf = ax.plot_surface(X * 100, Y, results, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

  fig.colorbar(surf, shrink=0.5, aspect=5)
  # fig.title('effect of EM and Crit for melt damage, {crit:d}% crit rate'.format(crit=int(CRIT_RATE * 100)))
  ax.set_title('effect of EM and Crit for melt damage, {crit:d}% crit rate'.format(crit=int(crit_rate * 100)))
  ax.set_xlabel('Crit damage value, %')
  ax.set_ylabel('Elemental mastery')
  ax.set_zlabel('Damage')
  return ax,fig

def main():
  for crit_rate in [0.2, 0.4, 0.6, 0.8, 1.0]:
    ax, fig = generate_plot_for_crit_rate(crit_rate)
    ax.view_init(20, -140)
    fig.savefig('{path}/plot_{crit:d}%.png'.format(
      path=os.path.dirname(os.path.realpath(__file__)), 
      crit=int(crit_rate * 100)
      ))
    plt.close(fig)

  # to display with fixed crit rate  
  # crit_rate = 0.4
  # ax, fig = generate_plot_for_crit_rate(crit_rate)
  # ax.view_init(20, -140)
  # plt.show()


if __name__ == "__main__":
    main()
