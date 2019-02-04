import sys
import math
from PyQt5 import QtWidgets
import design
from core import sochetanie,fact


class Lb3App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    back_or_next_operation = False
    current = 0
    max_input = 0
    pi = []
    mi = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Установка видимості елементів
        self.t2_back.setEnabled(False)
        self.t2_next.setEnabled(False)
        self.t2_label_pi.setEnabled(False)
        self.t2_pi.setEnabled(False)
        self.t2_label_mi.setEnabled(False)
        self.t2_mi.setEnabled(False)
        # Робота першій вкладки
        self.t1_calc.clicked.connect(self.calc_bernulli)
        # Робота другий вкладки
        self.t2_ok.clicked.connect(self.set_polin_input)
        self.t2_back.clicked.connect(self.slot_back_key)
        self.t2_next.clicked.connect(self.slot_next_key)
        self.t2_pi.valueChanged.connect(self.slot_save_pi_mi)
        self.t2_mi.valueChanged.connect(self.slot_save_pi_mi)
        self.t2_calc.clicked.connect(self.calc_polinom)
        # Робота третьої вкладки
        self.t3_calc.clicked.connect(self.calc_muavr)

    def calc_bernulli(self):
        def formula_bernulli(m, n, p, q):
            return sochetanie(m,n)*(p**m)*(q**(n-m))

        p = self.t1_p.value()
        n = self.t1_n.value()
        m = self.t1_m.value()
        m1 = self.t1_m1.value()
        m2 = self.t1_m2.value()
        q = 1 - p
        res1 = formula_bernulli(m, n, p, q)
        res2 = 0
        for i in range(0,m):
            res2 += formula_bernulli(i, n, p, q)
        res3 = 0
        for i in range(m, n + 1):
            res3 += formula_bernulli(i, n, p, q)
        res4 = 0
        for i in range(m1, m2 + 1):
            res4 += formula_bernulli(i, n, p, q)
        result = "Pn(k = m) = {0}\n" \
                 "Pn(k <= m) = {1}\n" \
                 "Pn(k >= m) = {2}\n" \
                 "Pn(m1 <= k <= m2) = {3}\n".format(res1, res2, res3, res4)
        self.t1_out.setText(result)

    def calc_muavr(self):
        p = self.t3_p.value()
        n = self.t3_n.value()
        m = self.t3_m.value()
        q = 1 - p
        x0 = (m - n*p)/math.sqrt(n*p*q)
        fi = math.e**(-x0**2/2)/math.sqrt(2*math.pi)
        pn = fi/math.sqrt(n*p*q)
        result = "P{0}({1}) = {2}".format(n, m, pn)
        self.t3_out.setText(result)

    def set_polin_input(self):
        self.pi.clear()
        self.mi.clear()
        self.pi.append(0.00)
        self.mi.append(0)
        self.current = 0
        self.max_input = self.t2_k.value()
        self.t2_pi.setValue(0.00)
        self.t2_mi.setValue(0)
        self.t2_label_pi.setText("p[0]")
        self.t2_label_mi.setText("m[0]")
        if self.max_input > 1:
            self.t2_next.setEnabled(True)
        if self.max_input > 0:
            self.t2_label_pi.setEnabled(True)
            self.t2_pi.setEnabled(True)
            self.t2_label_mi.setEnabled(True)
            self.t2_mi.setEnabled(True)
        elif self.max_input == 0:
            self.t2_label_pi.setEnabled(False)
            self.t2_pi.setEnabled(False)
            self.t2_label_mi.setEnabled(False)
            self.t2_mi.setEnabled(False)

    def slot_back_key(self):
        self.current -= 1
        self.t2_label_pi.setText("p[{0}]".format(self.current))
        self.t2_label_mi.setText("m[{0}]".format(self.current))
        self.back_or_next_operation = True
        self.t2_pi.setValue(self.pi[self.current])
        self.t2_mi.setValue(self.mi[self.current])
        self.back_or_next_operation = False
        if self.current == 0:
            self.t2_back.setEnabled(False)
        self.t2_next.setEnabled(True)

    def slot_next_key(self):
        self.current += 1
        if self.current > len(self.pi) - 1:
            self.pi.append(0.00)
            self.mi.append(0)
        self.t2_label_pi.setText("p[{0}]".format(self.current))
        self.t2_label_mi.setText("m[{0}]".format(self.current))
        self.back_or_next_operation = True
        self.t2_pi.setValue(self.pi[self.current])
        self.t2_mi.setValue(self.mi[self.current])
        self.back_or_next_operation = False
        if self.current == self.max_input - 1:
            self.t2_next.setEnabled(False)
        self.t2_back.setEnabled(True)

    def slot_save_pi_mi(self):
        if not self.back_or_next_operation:
            self.pi[self.current] = self.t2_pi.value()
            self.mi[self.current] = self.t2_mi.value()

    def calc_polinom(self):
        if len(self.pi) != self.t2_k.value() or len(self.mi) != self.t2_k.value():
            self.t2_out.setText("Длина вектора p[i] или m[i] не совпадает с k")
        elif math.fsum(self.mi) != self.t2_n.value():
            self.t2_out.setText("Сумма m[i] не равна n")
        else:
            fmk = 1
            for m in self.mi:
                fmk *= math.factorial(m)
            mpk = 1
            for i in range(0, self.t2_k.value()):
                mpk *= self.pi[i]**self.mi[i]
            pn = math.factorial(self.t2_n.value())*mpk/fmk
            result = "Pn = {0}".format(pn)
            self.t2_out.setText(result)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Lb3App()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
