import os
import ast
import pytesseract
from PIL import Image, ImageOps


pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

CorrectDict = {'"': "7", '#': '4', '%': '3', '+': '4', '.': '1', ':': '2', '?': '7', 'A': '4', 'B': '6', 'C': '2', 'E': '6', 'G': '5', 'H': '0', 'I': '1', 'L': '1', 'O': '0', 'Q': '0', 'R': '2', 'S': '5', 'T': '7', 'Z': '2', 'a': '3', 'd': '7', 'n': '0', 'r': '5', 's': '3', 't': '5', '£': '1', '¥': '0', '§': '5', '€': '1'}

RightCount = 0
WrongCount = 0
LeraningArray = []

for FileName in os.listdir("../PythonResults/ImageSample"):
    if FileName.endswith('.jpg') or FileName.endswith('.png'):
        ImageTarget = ImageOps.expand(Image.open(os.path.abspath(os.path.join("../PythonResults/ImageSample", FileName))).convert('L'), 8, "white")
        TextTarget = pytesseract.image_to_string(ImageTarget).replace(" ", "")
        print("未校正結果 for " + FileName + " is " + TextTarget)
        for Key in CorrectDict.keys():
            TextTarget = TextTarget.replace(Key, CorrectDict[Key])
        print("校正結果 for " + FileName + " is " + TextTarget)
        if TextTarget == FileName[0: 4]:
            RightCount += 1
        else:
            WrongCount += 1
            if len(TextTarget) != 4:
                print("OCR結果 " + TextTarget + " 與答案 " + FileName[0: 4] + " 長度不同，無法學習。")
                continue
            WordLearning = []
            for IndexChar in range(4):
                if TextTarget[IndexChar] != FileName[IndexChar]:
                    WordLearning.append([TextTarget[IndexChar], FileName[IndexChar]])
            print("OCR結果" + TextTarget + "與答案" + FileName[0: 4] + "之學習結果:", WordLearning)
            LeraningArray = LeraningArray + (WordLearning)

print("成功率為", RightCount / (RightCount + WrongCount))
print("學習陣列為", LeraningArray)
LearningResult = {}
for LearningPair in LeraningArray:
    [WrongChar, CorrectChar] = LearningPair
    LearningResult[str([WrongChar, CorrectChar])] = LearningResult.get(str([WrongChar, CorrectChar]), 0) + 1
print("學習字典為", LearningResult)

LearningCount = {"['8', '0']": 2, "['G', '0']": 2, "['B', '0']": 1, "['R', '2']": 1, "['S', '6']": 1, "['T', '1']": 2, "['4', '3']": 1, "['4', '0']": 1, "['Q', '0']": 2, "['S', '5']": 7, "['H', '0']": 1, "['%', '3']": 3, "['O', '0']": 3, "['T', '7']": 13, "['£', '1']": 1, "['€', '1']": 1, "['L', '1']": 5, "['%', '4']": 1, "['9', '5']": 2, "['§', '5']": 1, "['%', '1']": 2, "['C', '2']": 1, "['2', '0']": 1, "['4', '7']": 1, "['4', '1']": 3, "['A', '2']": 1, "['A', '4']": 2, "['S', '3']": 2, "['n', '0']": 1, "['s', '3']": 1, "['I', '1']": 3,
                 '[\'"\', \'7\']': 1, "['+', '4']": 2, "['#', '4']": 3, "['8', '6']": 2, "['€', '4']": 1, "['E', '4']": 2, "['¥', '0']": 1, "['G', '4']": 1, "['A', '5']": 1, "['R', '4']": 1, "[':', '2']": 1, "['8', '3']": 3, "['G', '5']": 3, "['C', '1']": 1, "['E', '6']": 3, "['t', '5']": 1, "['a', '3']": 1, "['r', '5']": 1, "['d', '7']": 1, "['2', '3']": 3, "['6', '5']": 1, "['1', '4']": 1, "['.', '1']": 1, "['s', '6']": 1, "['B', '6']": 2, "['4', '5']": 1, "['d', '0']": 1, "['?', '7']": 1, "['£', '6']": 1, "['5', '6']": 1, "['Z', '2']": 3, "['C', '6']": 1}
Result = [[ast.literal_eval(Key), LearningCount[Key]] for Key in LearningCount.keys()]
Result = sorted(Result, key=lambda Key: Key[0][0])
print(Result)
