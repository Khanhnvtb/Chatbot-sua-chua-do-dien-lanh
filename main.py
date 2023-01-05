import regex as re
from pyvi import ViTokenizer
import pandas as pd
import joblib
import math
import time


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
    # đưa về chữ viết thường
    document = document.lower()
    # chuẩn hóa unicode
    document = convert_unicode(document)
    # tách từ(từ đơn và từ ghép)
    document = ViTokenizer.tokenize(document)
    # loại bỏ ký tự đặc biệt
    document = re.sub(
        r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]', ' ', document)
    # xóa khoảng trắng thừa
    document = re.sub(r'\s+', ' ', document).strip()
    return document


DICT_SIGNAL_DH = {
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

DICT_SIGNAL_TL = {
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


# Tìm thuộc tính có độ hỗn loạn nhỏ nhất
def cal_Entropy(df: pd.DataFrame):
    # print(df)
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
    program = True
    while program:
        # Hỏi thiết bị người dùng cần tư vấn
        while True:
            print('\nHệ thống: Bạn cần tư vấn về vấn đề gì?')
            print('1. Điều hòa')
            print('2. Tủ lạnh')
            print('(Chọn 1 trong 2 lựa chọn)')
            input_user = input("\nNgười dùng: ").strip()

            if (input_user == '1'):
                folder = "Điều hòa"
                dict_signal = DICT_SIGNAL_DH
                break
            elif (input_user == '2'):
                folder = "Tủ lạnh"
                dict_signal = DICT_SIGNAL_TL
                break
            else:
                print('\nHệ thống: Vui lòng nhập chính xác 1 hoặc 2')

        # Load dữ liệu
        sheet_name = ['Câu hỏi', 'Case', 'Lỗi', 'Triệu chứng']
        data = pd.read_excel(f"{folder}/data.xlsx",
                             sheet_name=sheet_name)
        cases = data['Case']
        errors = data['Lỗi']
        questions = data['Câu hỏi']
        expression = data['Triệu chứng']

        # Load model
        model = joblib.load(f'{folder}/model.joblib')
        vectorizer = joblib.load(open(f"{folder}/tfidf.pkl", "rb"))

        # Hỏi vấn đề của người dùng
        print(f'\nHệ thống: {folder} của bạn gặp vấn đề gì?')
        input_user = input('\nNgười dùng: ').lower()
        input_user = text_preprocess(input_user)
        input_user = vectorizer.transform([input_user])

        # Dự đoán mã triệu chứng
        if (max(model.predict_proba(input_user)[0]) >= 0.5):
            problem_predict = model.predict(input_user)[0]
            property = dict_signal[problem_predict[:-2]]
            expression_code = problem_predict
            finish = False

            # Đưa ra câu hỏi dựa vào vấn đề gặp phải
            while (finish == False):
                cases = cases[cases[property].str.contains(expression_code)].drop(
                    [property], axis=1)
                property, entropy, list_expression_code = cal_Entropy(cases)

                # Liệt kê các biểu hiện có thể xảy ra với thuộc tính cần hỏi
                list_expression_code = sorted(
                    list_expression_code, key=lambda x: (len(x), x))
                list_option = []
                for index, expression_code in enumerate(list_expression_code):
                    codes = expression_code.split(', ')
                    option = ''
                    for i, code in enumerate(codes):
                        option += expression[expression['Mã']
                                             == code].iloc[0]['Dấu hiệu']
                        if (i < len(codes)-1):
                            option += ', '
                    option = option.lower().capitalize()
                    list_option.append(option)

                list_option.append('Trường hợp khác')

                # Đưa ra câu hỏi và lựa chọn
                while True:
                    question = questions[questions['Tiêu chí']
                                         == property].iloc[0]['Câu hỏi']
                    print(f"\nHệ thống: {question}")
                    for index, expression_code in enumerate(list_option):
                        print(f'{index+1}. {expression_code}')

                    input_user = input('\nNgười dùng: ')

                    try:
                        input_user = int(input_user)-1
                        if input_user < index:
                            expression_code = list_expression_code[input_user]

                            if (entropy - int(entropy) == 0):
                                error_code = cases[cases[property]
                                                   == expression_code].iloc[0]['Lỗi']
                                error = errors[errors['Mã'] == error_code]
                                print(
                                    f'\nHệ thống: Chẩn đoán lỗi: {error.iloc[0]["Lỗi"]}\n')
                                print(
                                    f'Hệ thống: Nguyên nhân:\n{error.iloc[0]["Nguyên nhân"]}\n')
                                print(
                                    f'Hệ thống: Cách khắc phục:\n{error.iloc[0]["Khắc phục"]}\n')
                                print(
                                    f'Hệ thống: Lời khuyên:\n{error.iloc[0]["Lời khuyên"]}\n')
                                finish = True
                            break
                        elif input_user == index:
                            print(
                                '\nHệ thống: Vấn đề bạn gặp phải chưa có trong hệ thống, bạn có thể gọi điện thoại đến số 0123456789 để được tư vấn trực tiếp từ nhân viên kỹ thuật\n')
                            finish = True
                            break
                        else:
                            print('\nHệ thống: Bạn vui lòng nhập đúng các lựa chọn')

                    except:
                        print('\nHệ thống: Bạn vui lòng nhập đúng các lựa chọn')
        else:
            print('\nHệ thống: Vấn đề bạn gặp phải chưa có trong hệ thống, bạn gọi điện thoại đến số 0123456789 để được tư vấn trực tiếp từ nhân viên kỹ thuật\n')

        time.sleep(2)

        # Hỏi người dùng có tiếp tục tư vấn
        while True:
            print('Hệ thống: Bạn muốn tiếp tục tư vấn không?')
            print('1. Có ')
            print('2. Không')
            print('(Chọn 1 trong 2 lựa chọn)')
            input_user = input("\nNgười dùng: ").strip()

            if (input_user == '1'):
                break
            elif (input_user == '2'):
                print("\nHệ thống: Chúc bạn một ngày vui vẻ")
                program = False
                break
            else:
                print('\nHệ thống: Vui lòng nhập chính xác 1 hoặc 2')


if __name__ == '__main__':
    main()
