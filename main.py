# -*- coding: utf-8 -*-
"""
اپلیکیشن اندرویدی دسترسی سریع به مرورگرها و شبکه‌های تلویزیونی
ساخته‌شده با Kivy
برای ساخت APK از Buildozer استفاده کنید.
"""

import webbrowser

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, RoundedRectangle

NAVY = (0.055, 0.09, 0.17, 1)
PANEL = (0.09, 0.14, 0.24, 1)
YELLOW = (0.96, 0.77, 0.22, 1)
WHITE = (0.96, 0.97, 1, 1)
MUTED = (0.68, 0.73, 0.82, 1)

# لینک‌های مرورگرها؛ در اندروید معمولاً لینک در مرورگر پیش‌فرض باز می‌شود.
BROWSERS = [
    ("Google", "https://www.google.com"),
    ("Microsoft Edge", "https://www.microsoft.com/edge"),
    ("Firefox", "https://www.mozilla.org/firefox/"),
]

# پورتال رسمی پخش زنده صداوسیما.
# شناسه idv برای شبکه ۱ در منبع عمومی تأیید شده است؛
# شناسه‌های ۲ تا ۲۱ را در صورت تغییر ساختار سایت می‌توان در همین فهرست اصلاح کرد.
IRIB_LIVE = "https://sepehr.irib.ir/?idc=32&idt=tv&idv={}"
CHANNEL_URLS = {n: IRIB_LIVE.format(n) for n in range(1, 22)}
CHANNEL_URLS[3] = "https://tv3.ir/#!"


def rounded_background(widget, color, radius=16):
    with widget.canvas.before:
        Color(*color)
        shape = RoundedRectangle(pos=widget.pos, size=widget.size,
                                 radius=[dp(radius)] * 4)
    def update(*_):
        shape.pos = widget.pos
        shape.size = widget.size
    widget.bind(pos=update, size=update)


def make_button(text, callback, height=54, font_size=16, primary=False):
    btn = Button(
        text=text,
        size_hint_y=None,
        height=dp(height),
        font_size=font_size,
        bold=True,
        color=NAVY if primary else WHITE,
        background_normal="",
        background_down="",
        background_color=YELLOW if primary else PANEL,
        halign="center",
        valign="middle",
    )
    btn.bind(on_release=lambda *_: callback())
    return btn


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(12))
        root.canvas.before.clear()
        with root.canvas.before:
            Color(*NAVY)
            self.bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
        root.bind(pos=lambda *_: setattr(self.bg, "pos", root.pos),
                  size=lambda *_: setattr(self.bg, "size", root.size))
        self.add_widget(root)

        root.add_widget(Label(
            text="[b]مرکز دسترسی سریع[/b]",
            markup=True, color=YELLOW, font_size="25sp",
            size_hint_y=None, height=dp(52)
        ))
        root.add_widget(Label(
            text="مرورگرها و شبکه‌های تلویزیونی ایران",
            color=MUTED, font_size="14sp",
            size_hint_y=None, height=dp(28)
        ))

        # در موبایل دکمه‌ها زیر هم و در اندازه مناسب لمس قرار می‌گیرند.
        for title, url in BROWSERS:
            root.add_widget(make_button(
                title + "  ↗",
                lambda link=url: webbrowser.open(link),
                height=52, font_size=15
            ))

        root.add_widget(make_button(
            "شبکه‌های تلویزیونی ایران  |  ۱ تا ۲۱",
            lambda: setattr(self.manager, "current", "channels"),
            height=62, font_size=16, primary=True
        ))
        root.add_widget(Label(
            text="برای بازگشت از صفحه شبکه‌ها، دکمه بازگشت را بزنید",
            color=MUTED, font_size="11sp"
        ))


class ChannelsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        with root.canvas.before:
            Color(*NAVY)
            self.bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
        root.bind(pos=lambda *_: setattr(self.bg, "pos", root.pos),
                  size=lambda *_: setattr(self.bg, "size", root.size))
        self.add_widget(root)

        top = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        back = make_button("← بازگشت", lambda: setattr(self.manager, "current", "home"),
                           height=44, font_size=13, primary=True)
        back.size_hint_x = 0.34
        top.add_widget(back)
        top.add_widget(Label(
            text="[b]شبکه‌های تلویزیونی[/b]", markup=True,
            color=YELLOW, font_size="19sp"
        ))
        root.add_widget(top)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(4))
        grid = GridLayout(cols=2, spacing=dp(10), padding=(0, dp(4)),
                          size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for number in range(1, 22):
            # شماره‌ها فارسی نمایش داده می‌شوند.
            fa_number = str(number).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
            button = make_button(
                f"شبکه {fa_number}",
                lambda n=number: webbrowser.open(CHANNEL_URLS[n]),
                height=58, font_size=15,
                primary=(number == 3)
            )
            grid.add_widget(button)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        root.add_widget(Label(
            text="با انتخاب هر شماره، صفحه پخش زنده شبکه باز می‌شود.",
            color=MUTED, font_size="11sp",
            size_hint_y=None, height=dp(25)
        ))


class TVLauncherApp(App):
    def build(self):
        self.title = "مرکز دسترسی سریع"
        Window.clearcolor = NAVY
        manager = ScreenManager(transition=SlideTransition())
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(ChannelsScreen(name="channels"))
        return manager

    def on_start(self):
        # دکمه بازگشت اندروید
        Window.bind(on_keyboard=self.on_keyboard)

    def on_keyboard(self, window, key, *args):
        if key == 27:
            if self.root.current == "channels":
                self.root.current = "home"
                return True
        return False


if __name__ == "__main__":
    TVLauncherApp().run()
