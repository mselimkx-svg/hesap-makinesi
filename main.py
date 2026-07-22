from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse

# Arka plan nötr gri
Window.clearcolor = (0.5, 0.5, 0.5, 1)

class YuvarlakButon(Button):
    def __init__(self, circle_color=(0, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.circle_color = circle_color
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.circle_color)
            size = min(self.width, self.height)
            x = self.x + (self.width - size) / 2
            y = self.y + (self.height - size) / 2
            Ellipse(pos=(x, y), size=(size, size))

class HesapMakinesi(App):
    def build(self):
        self.title = "Yin-Yang Desenli Hesap Makinesi"
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = False

        main_layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Beyaz zeminli ekran kutusu
        self.solution = Label(
            text="0",
            font_size=48,
            halign="right",
            valign="center",
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
            bold=True
        )
        self.solution.bind(size=self.solution.setter('text_size'))
        main_layout.add_widget(self.solution)

        # 5 Satır x 4 Sütun
        buttons = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            [".", "0", "DEL", "="]
        ]

        # Yin-Yang renk deseni matrisi (1: Siyah Buton, 0: Beyaz/Gri Buton)
        # Siyah ve beyaz alanlar Yin-Yang sembolündeki gibi birbirini sarmallar
        yin_yang_pattern = [
            [1, 1, 1, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        grid_layout = GridLayout(cols=4, spacing=15)

        for r_idx, row in enumerate(buttons):
            for c_idx, label in enumerate(row):
                is_black = yin_yang_pattern[r_idx][c_idx] == 1
                
                if is_black:
                    btn_color = (0.05, 0.05, 0.05, 1)  # Yin (Siyah Daire)
                    text_color = (1, 1, 1, 1)          # Beyaz Yazı
                else:
                    btn_color = (0.95, 0.95, 0.95, 1)  # Yang (Beyaz Daire)
                    text_color = (0, 0, 0, 1)          # Siyah Yazı

                button = YuvarlakButon(
                    text=label,
                    font_size=24,
                    bold=True,
                    color=text_color,
                    circle_color=btn_color
                )
                button.bind(on_press=self.on_button_press)
                grid_layout.add_widget(button)

        main_layout.add_widget(grid_layout)
        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = "0"
            self.last_was_operator = False
        elif button_text == "DEL":
            if len(current) > 1 and current != "Hata":
                self.solution.text = current[:-1]
            else:
                self.solution.text = "0"
            self.last_was_operator = self.solution.text[-1] in self.operators if self.solution.text else False
        elif button_text == "=":
            try:
                result = str(eval(self.solution.text))
                self.solution.text = result
                self.last_was_operator = False
            except Exception:
                self.solution.text = "Hata"
                self.last_was_operator = False
        else:
            if current == "0" or current == "Hata":
                if button_text == ".":
                    self.solution.text = "0."
                elif button_text in self.operators:
                    return
                else:
                    self.solution.text = button_text
            else:
                if button_text == "." and current[-1] == ".":
                    return
                if button_text in self.operators and self.last_was_operator:
                    return
                self.solution.text += button_text

            self.last_was_operator = button_text in self.operators

if __name__ == "__main__":
    HesapMakinesi().run()
