import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('datatest2-30R-30T-5 0I.csv')


plt.plot(df['Probability Of 3.5-Instruct'], df['Success Rate'], marker='o')
plt.xlabel('Probability of Using 3.5-Instruct')
plt.ylabel('Success Rate')
plt.title('Success rate vs probability of using 3.5-Instruct for printing 1-100 given 20 tokens')
plt.show()