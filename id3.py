import pandas as pd
import math
sheet_name_DH = ['Hoạt động', 'Tình trạng', 'Nhiệt độ', 'Đèn báo lỗi, bảng hiển thị',
                 'Quạt dàn lạnh', 'Quạt dàn nóng', 'Cục nóng', 'Ống đồng', 'Mùi', 'Tín hiệu remote']
data = pd.read_excel('Điều hòa/Case.xlsx', sheet_name=[
                     'Case', 'Lỗi', 'Tiêu chí'], index_col=0)
cases = data['Case']
sheet_name_DH.remove('Tình trạng')
# print(cases[cases['Tình trạng'] == 'TT02'])
# print(cases[cases['Hoạt động'] == 'HDO1'].value_counts())


def cal_Entropy(df: pd.DataFrame):
    print(df)
    total_cases = df.shape[0]
    property_selected = ''
    entropy_min = -1

    for property in df.columns[:-1]:
        entropy = 0
        for code, quantity in df[property].value_counts().items():
            sum = 0
            for count_by_error in df[df[property] == code]['Lỗi'].value_counts():
                s = count_by_error / quantity
                if s != 0:
                    s *= math.log(s, 2) * -1
                sum += s
            entropy += sum * quantity / total_cases
                
        if (entropy_min == -1) or (entropy_min > entropy):
            entropy_min = entropy
            property_selected = property
        print(property, entropy)
    list_option = df[property_selected].value_counts().keys()
    return property_selected, entropy_min, list_option,

property = 'Tình trạng'
option = 'TT03'
while(True):
    cases = cases[cases[property] == option].drop([property],axis=1)
    property, entropy, list_option = cal_Entropy(cases)
    print(f'{property}: ')
    list_option = sorted(list_option)
    for index, option in enumerate(list_option):
        print(f'{index+1}. {option}')
    print(int(entropy))
    option = int(input())-1

    if(entropy - int(entropy) == 0) :
        print(cases[cases[property] == list_option[option]]['Lỗi'].unique())
        break
