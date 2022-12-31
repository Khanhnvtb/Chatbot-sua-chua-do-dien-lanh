import regex as re
from pyvi import ViTokenizer
import yaml
import pandas as pd
import joblib
import math

sheet_name = ['Câu hỏi', 'Case', 'Lỗi', 'Triệu chứng']


uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"


def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic


# Đưa toàn bộ dữ liệu qua hàm này để chuẩn hóa lại

def convert_unicode(txt):
    dicchar = loaddicchar()
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)


def text_preprocess(document):
    # chuẩn hóa unicode
    document = convert_unicode(document)
    # tách từ(từ đơn và từ ghép)
    document = ViTokenizer.tokenize(document)
    # đưa về chữ viết thường
    document = document.lower()
    #loại bỏ ký tự đặc biệt
    document = re.sub(
        r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]', ' ', document)
    # xóa khoảng trắng thừa
    document = re.sub(r'\s+', ' ', document).strip()
    return document

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
    list_option = df[property_selected].value_counts().keys()
    return property_selected, entropy_min, list_option,

def main():
    print('Hệ thống: Bạn cần tư vấn về vấn đề gì?')
    print('1. Điều hòa')
    print('2. Tủ lạnh')
    while True:
        option = input("Người dùng: ").strip()
        
        if (option == '1'):
            folder = "Điều hòa"
            dict_signal = dict_signal_DH
            break
        elif (option == '2'):
            folder = "Tủ lạnh"
            dict_signal = dict_signal_TL
            break
        else:
            print('Hệ thống: Vui lòng nhập chính xác 1 hoặc 2')

    data = pd.read_excel(f"{folder}/data.xlsx",
                        sheet_name=sheet_name)

    model = joblib.load(f'{folder}/model.joblib')
    vectorizer = joblib.load(open(f"{folder}/tfidf.pkl", "rb"))

    cases = data['Case']
    errors = data['Lỗi']
    question = data['Câu hỏi']
    expression = data['Triệu chứng']

    print(f'Hệ thống: {folder} của bạn gặp vấn đề gì?')
    input_user = input('Người dùng: ')
    input_user = text_preprocess(input_user)
    input_user = vectorizer.transform([input_user])
    
    if(max(model.predict_proba(input_user)[0]) >= 0.3):
        problem_predict = model.predict(input_user)[0]
        print(problem_predict)
    else:
        print(model.predict(input_user)[0])
        print('Hệ thống: Lỗi của bạn hiện chưa có trong dữ liệu của chúng tôi')
        return
    
    property = dict_signal[problem_predict[:-2]]
    option = problem_predict
    finish = False

    while(finish == False):
        cases = cases[cases[property]== option].drop([property], axis=1)
        property, entropy, list_option_code = cal_Entropy(cases)
        print(f'{property}: ')
        list_option_code = sorted(list_option_code)
        list_option = []
        for index, option in enumerate(list_option_code):
            codes = option.split(', ')
            output = ''
            for i, code in enumerate(codes):
                output += expression[expression['Mã'] == code].iloc[0]['Dấu hiệu']
                if (i < len(codes)-1):
                    output += ', '
            list_option.append(output)

        list_option.append('Trường hợp khác')

        while True:          
            question_system = question[question['Tiêu chí'] == property].iloc[0]['Câu hỏi']
            print(
                f"Hệ thống: {question_system}")
            for index, option in enumerate(list_option):
                print(f'{index+1}. {option}')

            input_user = input('Người dùng: ')

            try:
                input_user = int(input_user)-1
                if input_user < index:
                    option = list_option_code[input_user]
                    if (entropy - int(entropy) == 0):
                        error_code = cases[cases[property] == option].iloc[0]['Lỗi']
                        error = errors[errors['Mã'] == error_code]
                        print(f'Hệ thống: Chẩn đoán lỗi: {error.iloc[0]["Lỗi"]}\n')
                        print(f'Hệ thống: Nguyên nhân:\n{error.iloc[0]["Nguyên nhân"]}\n')
                        print(f'Hệ thống: Cách khắc phục:\n{error.iloc[0]["Khắc phục"]}\n')
                        print(f'Hệ thống: Lời khuyên:\n{error.iloc[0]["Lời khuyên"]}\n')
                        finish = True
                    break
                elif input_user == index:
                    print('Hệ thống: Trường hợp này bạn vui lòng mang đến cửa hàng để kiểm tra kĩ hơn.')
                    finish = True
                    break
                else :
                    print('Hệ thống: Bạn vui lòng nhập đúng các lựa chọn')
                
            except:
                print('Hệ thống: Bạn vui lòng nhập đúng các lựa chọn')

main()


