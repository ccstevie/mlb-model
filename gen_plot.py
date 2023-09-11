import matplotlib.pyplot as plt
import csv
from datetime import date
  
Names = []
Values = []
  
def main(data=None):
    if not data:
        with open(f'{date.today()}.csv','r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            count = 10
            for row in lines:
                if count == 0:
                    break
                if len(row) > 0:
                    Names.append(row[0])
                    Values.append(float(row[1]))
                    count -= 1
        
        plt.scatter(Names, Values, color = 'g', s=10)
        plt.xticks(rotation = 25)
        plt.xlabel('Names')
        plt.ylabel('Values')
        plt.title(f'{date.today()} Swamy Scores', fontsize = 20)
    else:
        x, y = zip(*data)
        plt.plot(x, y)

    plt.show()

if __name__ == '__main__':
    main()