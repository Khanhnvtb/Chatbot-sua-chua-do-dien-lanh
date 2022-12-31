import pandas as pd
question = pd.read_excel("Điều hòa/data.xlsx",
                     sheet_name=['Case', 'Câu hỏi'])['Câu hỏi']
question.loc[question['Tiêu chí'] == 'Quạt dàn lạnh']
# print(question['Case'])