import matplotlib.pyplot as plt
import csv
from datetime import date
  
Names = []
Values = []
  
def main(data=None):
    plt.figure(figsize=(200,10))
    if not data:
        with open(f'{date.today()}.csv','r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                if len(row) > 0:
                    Names.append(row[0])
                    Values.append(float(row[1]))
        
        plt.scatter(Names, Values, color = 'g', s=10)
        plt.xticks(rotation = 25)
        plt.xlabel('Names')
        plt.ylabel('Values')
        plt.title('MLB Swamy Scores Today', fontsize = 20)
    else:
        x, y = zip(*data)
        plt.plot(x, y)

    plt.show()

if __name__ == '__main__':
    main()