import yaml
import pandas as pd

case = "\Case.xlsx"
question = '\question.yml'

sheet_name_DH = ['Hoạt động', 'Tình trạng', 'Nhiệt độ', 'Đèn báo lỗi, bảng hiển thị',
                 'Quạt dàn lạnh', 'Quạt dàn nóng', 'Cục nóng', 'Ống đồng', 'Mùi', 'Tín hiệu remote']
sheet_name_TL = ['Khả năng làm lạnh', 'Đèn', 'Block', 'Ống đồng', 'Nhiệt độ',
                 'Hoạt động', 'Tình trạng', 'Dàn nóng', 'Khả năng bảo quản', 'Mùi']

data2 = pd.read_excel("Điều hoà\Độ tương đồng.xlsx",
                      sheet_name=sheet_name_DH, index_col=0)


dict_signal_DH = {
    'HD': 'Hoạt động',
    'TT': 'Tình trạng',
    'ND': 'Nhiệt độ',
    'DB': 'Đèn báo lỗi, bảng hiển thị',
    'QL': 'Quạt dàn lạnh',
    'QN': 'Quạt dàn nóng',
    'CN': 'Cục nóng',
    'OD': 'Ống đồng',
    'M': 'Mùi',
    'TH': 'Tín hiệu remote'
}

dict_signal_TL = {
    'LL': 'Khả năng làm lạnh',
    'D': 'Đèn',
    'B': 'Block',
    'OD': 'Ống đồng',
    'ND': 'Nhiệt độ',
    'HD': 'Hoạt động',
    'TT': 'Tình trạng',
    'DN': 'Dàn nóng',
    'BQ': 'Khả năng bảo quản',
    'M': 'Mùi'
}

dict_signal = {}

print('Hệ thống: Bạn cần tư vấn về vấn đề gì?')
print('1. Điều hoà')
print('2. Tủ lạnh')
if (input("Người dùng: ") == '1'):
    case = "Điều hoà" + case
    question = "Điều hoà" + question
    dict_signal = dict_signal_DH
else:
    case = "Tủ lạnh" + case
    question = "Tủ lạnh" + question
    data2 = pd.read_excel("Tủ lạnh\Độ tương đồng.xlsx",
                          sheet_name=sheet_name_TL, index_col=0)
    dict_signal = dict_signal_TL

data = pd.read_excel(case, sheet_name=[
                     'Case', 'Lỗi', 'Tiêu chí'], index_col=0)

with open(question, 'r', encoding="utf8") as f:
    doc = yaml.load(f, Loader=yaml.FullLoader)
doc = dict(doc)
signals = []


for key in doc.keys():
    print('\nHệ thống:', doc[key]['question'])
    for option in doc[key]['options']:
        print(option)

    ops = input('\nNgười dùng: ').split(',')
    signal = ''
    for i, op in enumerate(ops):
        code = doc[key]['code']
        signal += f'{code}%02d' % int(op)
        if i != len(ops) - 1:
            signal += ', '
    signals.append((code, signal))


cases = data['Case']
errors = data['Lỗi']
weights = data['Tiêu chí']
max_probability = 0
id = 0


for index, case in cases.iterrows():
    sum1 = sum2 = 0
    for signal_code in signals:
        code = signal_code[1]
        signal = dict_signal[signal_code[0]]
        weight = weights.loc[signal, 'Trọng số']
        similarity = data2[signal].loc[code, case[signal]]
        sum1 += weight*similarity
        sum2 += weight

    probability = sum1/sum2
    if (max_probability < probability):
        max_probability = probability
        id = index


if max_probability > 0.9:
    conclusion = 'Chắc chắn bị lỗi '
elif max_probability > 0.7:
    conclusion = 'Có tỉ lệ cao bị lỗi '
elif max_probability > 0.5:
    conclusion = 'Có khả năng bị lỗi '
elif max_probability > 0:
    conclusion = 'Hệ thống chưa thể xác định được lỗi'

print(f"\nHệ thống: {conclusion}", end='')

if max_probability > 0.5:
    error = errors['Lỗi'][cases.loc[id, 'Lỗi']]
    print(f"'{error}'")
    print(
        f"\nHệ thống: Nguyên nhân bị lỗi: \n {errors['Nguyên nhân'][cases.loc[id, 'Lỗi']]}")
    print(
        f"\nHệ thống: Cách khắc phục: \n {errors['Khắc phục'][cases.loc[id, 'Lỗi']]}")
