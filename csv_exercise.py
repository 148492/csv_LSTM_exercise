import csv
import xlrd


def csv_from_excel():
    wb = xlrd.open_workbook('温度.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    with open('温度.csv', 'w', newline='') as your_csv_file:
    # your_csv_file = open('温度.csv', 'w', newline='')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


csv_from_excel()
# runs the csv_from_excel function:
