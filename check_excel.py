import openpyxl

wb = openpyxl.load_workbook('links-new.xlsx')
sheet = wb.active

for i in range(1, 6):
    print([cell.value for cell in sheet[i]])