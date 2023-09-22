import csv
import matplotlib.pyplot as plt

from util import create_unique_filename


def sort_output_csv(filepath: str, new_filename: str) -> str:
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        header_row = next(reader)

        sorted_list = sorted(list(reader), key=lambda row: row[0])

        new_filepath = create_unique_filename(f'sorted_results/{new_filename}', suffix='.csv')
        with open(new_filepath, 'x') as file:
            writer = csv.writer(file)
            writer.writerow(header_row)

            for row in sorted_list:
                writer.writerow(row)

    return new_filepath


def visualize_timeseries(filepath: str):
    # data
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)

    y_data_1 = [int(row[1]) for row in data]
    y_data_2 = [int(row[2]) for row in data]
    y_data_3 = [int(row[3]) for row in data]
    x_data = [date[0] for date in data]

    # plot
    fig, ax = plt.subplots()
    fig.set_size_inches(25, 4)

    ax.step(x_data, y_data_3, '#FFBB5C', label=header[3])
    ax.step(x_data, y_data_2, '#FF9B50', label=header[2])
    ax.step(x_data, y_data_1, '#C63D2F', label=header[1])

    ax.legend()

    # x ticks
    number_of_x_ticks = 12
    tick_interval = len(x_data) / number_of_x_ticks
    x_ticks = [x_data[int(i * tick_interval)] for i in range(number_of_x_ticks)]
    # y ticks
    biggest_y_value = int(max(y_data_1 + y_data_2 + y_data_3))
    # draw ticks
    ax.set(xlim=(0, number_of_x_ticks), xticks=x_ticks,
           ylim=(0, biggest_y_value), yticks=range(biggest_y_value + 1))

    plt.suptitle(filepath.split('/')[-1][:-4], fontweight='bold')
    plt.title('number of articles per day containing the target word')
    plt.show()


visualize_timeseries(filepath='results/SG_Tagblatt.csv')
