import xlwt

list = input().split()

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('enc_1')

worksheet.write(0, 0, 'τ_ext')
worksheet.write(0, 1, 'L_ext')
worksheet.write(0, 2, 'τ_enc')
worksheet.write(0, 3, 'L_enc')
i0 = 1
i1 = 1
i2 = 1
i3 = 1

for i in range(len(list) // 2):
    if list[i * 2] == 'τ_ext':
        worksheet.write(i0, 0, list[i * 2 + 1])
        i0 += 1
    elif list[i * 2] == 'L_ext':
        worksheet.write(i1, 1, list[i * 2 + 1])
        i1 += 1
    elif list[i * 2] == 'τ_enc':
        worksheet.write(i2, 2, list[i * 2 + 1])
        i2 += 1
    else:
        worksheet.write(i3, 3, list[i * 2 + 1])
        i3 += 1

workbook.save('time_record.xls')
