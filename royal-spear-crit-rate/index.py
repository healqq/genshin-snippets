import numpy as np
import random
import matplotlib.pyplot as plt

EXPERIMENT_SIZE = 100000
WEAPON_STACK_VALUE = 0.08
random.seed()
def get_experiment_result_for_crit_value(current_crit):
  result = np.zeros(EXPERIMENT_SIZE)

  crit_stacks = 0
  for index in range(result.shape[0]):
    roll = random.random()
    current_result = roll < current_crit + crit_stacks * WEAPON_STACK_VALUE 
    if current_result:
      crit_stacks = 0
    else:
      # cap is at 5 stacks
      crit_stacks = min(crit_stacks + 1, 5)

    result[index] = int(current_result)
  return result


def main():
  crit_values = np.arange(0, 0.8, 0.05)
  results = np.zeros((np.shape(crit_values)[0], EXPERIMENT_SIZE))
  for index in range(crit_values.shape[0]):
    results[index] = get_experiment_result_for_crit_value(crit_values[index])
  
  mean_results = np.mean(results, axis=1)
  plt.plot(
    # added crit
    crit_values * 100, (mean_results - crit_values) * 100, 'r',
    # effective crit
    crit_values * 100, mean_results * 100, 'b',
    # base crit
    crit_values * 100, crit_values * 100, 'b--'
  )
  
  plt.title('crit rate with Royal Spear (refinement 1)')
  plt.xlabel('base crit rate, %')
  plt.ylabel('effective crit rate, %')
  plt.legend(['added crit', 'effective crit', 'base crit'])
  plt.show()


if __name__ == "__main__":
    main()
