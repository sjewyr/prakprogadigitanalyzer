from enum import Enum, unique
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
)

ABSOLUTE = {"zero": 0}

UNITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

DECIUNITS = {
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}

DECIMAL = {
    "twenty": 20,
    "thirty": 30,
    "fourty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

HUNDREDS = {
    "one hundred": 100,
    "two hundred": 200,
    "three hundred": 300,
    "four hundred": 400,
    "five hundred": 500,
    "six hundred": 600,
    "seven hundred": 700,
    "eight hundred": 800,
    "nine hundred": 900,
}

ALL_SYMBOLS = {}
ALL_SYMBOLS.update(UNITS)
ALL_SYMBOLS.update(DECIMAL)
ALL_SYMBOLS.update(HUNDREDS)
ALL_SYMBOLS.update(DECIUNITS)
ALL_SYMBOLS.update(ABSOLUTE)


ALLOWED_LITERALS = list(ALL_SYMBOLS.keys())


class InvalidReturn:
    def __init__(self, pos=None, val=None, typ: "ERRORS" = None, addinfo=None) -> None:
        self.pos: int = pos
        self.val: str = val
        self.type: ERRORS = typ.value(pos, val, addinfo)

    def __str__(self):
        return str(self.type)


class Analyzer:
    def __init__(self, code: str):
        self.code: str = code.lower()
        self._code = list(filter(lambda x: x != "", self.code.split(" ")))
        self._nodes = self.get_nodes()

    def get_nodes(self):
        result = []
        i = 0
        flag = 0
        while i < len(self._code):
            if i + 1 < len(self._code):
                if " ".join([self._code[i], self._code[i + 1]]) in ALLOWED_LITERALS:
                    result.append(" ".join([self._code[i], self._code[i + 1]]))
                    i += 2
                    continue
            result.append(self._code[i])
            i += 1
        return result

    def analyze(self):
        err = self.analyze_syllables()
        if err:
            return err

        err = self.analyze_semantic(0, self._nodes.copy(), ALLOWED_LITERALS.copy())
        if err:
            return err

        return self.calc()

    def calc(self):
        res = 0
        for node in self._nodes:
            res += ALL_SYMBOLS[node]
        return res

    def analyze_semantic(self, idx, to_process: list, allowed_symbols, prev=None):
        if not to_process:
            return

        cur = to_process.pop(0)
        if cur not in allowed_symbols:
            return InvalidReturn(
                idx, cur, ERRORS.Semantic, f"{cur} не может следовать после {prev}"
            )
        if cur in HUNDREDS:
            idx += 1
            allowed_symbols = {}
            allowed_symbols.update(UNITS)
            allowed_symbols.update(DECIMAL)
            allowed_symbols.update(DECIUNITS)
        if cur in DECIMAL:
            allowed_symbols = {}
            allowed_symbols.update(UNITS)
        if cur in UNITS:
            allowed_symbols = {}
        if cur in DECIUNITS:
            allowed_symbols = {}
        if cur in ABSOLUTE:
            allowed_symbols = {}

        return self.analyze_semantic(idx + 1, to_process, allowed_symbols, prev=cur)

    def analyze_syllables(self):
        idx = 0
        for symbol in self._nodes:
            if not symbol in ALLOWED_LITERALS:
                return InvalidReturn(idx, symbol, ERRORS.Syntax)
            idx += len(symbol.split(" "))


class SemanticError:
    def __init__(self, idx, cur, additional=None) -> None:
        self.cur = cur
        self.idx = idx
        self.additional = additional

    def __str__(self):
        if self.additional:
            return f"Семантическая ошибка: в символе {self.cur} по индексу {self.idx}, {self.additional}"
        return f"Семантическая ошибка: в символе {self.cur} по индексу {self.idx}"


class SyntaxErr:
    def __init__(self, idx, cur, *args, **kwargs) -> None:
        self.cur = cur
        self.idx = idx

    def __str__(self):
        return f"Синтаксическая ошибка: в символе {self.cur} по индексу {self.idx}"


class ERRORS(Enum):
    Syntax = SyntaxErr
    Semantic = SemanticError


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.inp1 = QLineEdit()
        self.out = QLabel()
        self.button = QPushButton()
        self.button.setText("Посчитать")
        self.button.clicked.connect(self.calculate)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Введите код: "))
        self.layout().addWidget(self.inp1)
        self.layout().addWidget(QLabel("Результат: "))
        self.layout().addWidget(self.out)
        self.layout().addWidget(self.button)

    def calculate(self):
        code = self.inp1.text()
        analyzer = Analyzer(code)
        result = analyzer.analyze()
        self.out.setText(str(result))


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
