"""
vista.py:
    Módulo encargado de generar la interfaz gráfica de la app. 
"""
__author__ = "Diego Calderón, Nahuel Vargas"
__maintainer__ = "Diego Calderón, Nahuel Vargas"
__email__ = "diegoacalderon994@gmail.com, nahuvargas24@gmail.com"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"

from modelo import Crud
from kivy.metrics import dp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class Home(MDBoxLayout):
    Builder.load_file("home.kv")


class Agregar(MDBoxLayout):
    Builder.load_file("agregar.kv")


class Eliminar(MDBoxLayout):
    Builder.load_file("eliminar.kv")


class Modificar(MDBoxLayout):
    Builder.load_file("modificar.kv")


class Consultar(MDBoxLayout):
    Builder.load_file("consultar.kv")


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class MisPantallas(MDScreenManager):
    def __init__(self, app, **kwargs):
        super(MisPantallas, self).__init__(**kwargs)
        self.obj_app = app
        self.obj_home = Home()
        self.obj_agregar = Agregar()
        self.obj_eliminar = Eliminar()
        self.obj_modificar = Modificar()
        self.obj_consultar = Consultar()
        self.ids.home.add_widget(self.obj_home)
        self.ids.add.add_widget(self.obj_agregar)
        self.ids.elim.add_widget(self.obj_eliminar)
        self.ids.mod.add_widget(self.obj_modificar)
        self.ids.consulta.add_widget(self.obj_consultar)
        self.obj_c = Crud()
        self.crear_menu()
        self.widgets_consulta()

    def cambiar_tema(self, value):
        if value == "claro":
            self.menu.dismiss()
            self.obj_app.theme_cls.primary_palette = "LightBlue"
            self.obj_app.theme_cls.theme_style = "Light"
            self.obj_home.ids.buttonadd.md_bg_color = "#C7C7C7"
            self.obj_home.ids.buttondel.md_bg_color = "#C7C7C7"
            self.obj_home.ids.buttonedit.md_bg_color = "#C7C7C7"
            self.obj_home.ids.buttonsearch.md_bg_color = "#C7C7C7"
            self.crear_menu()
        else:
            self.menu.dismiss()
            self.obj_app.theme_cls.primary_palette = "Orange"
            self.obj_app.theme_cls.theme_style = "Dark"
            self.obj_home.ids.buttonadd.md_bg_color = "#404040"
            self.obj_home.ids.buttondel.md_bg_color = "#404040"
            self.obj_home.ids.buttonedit.md_bg_color = "#404040"
            self.obj_home.ids.buttonsearch.md_bg_color = "#404040"
            self.crear_menu()

    def crear_menu(self):
        self.menu_items = [
            {
                "icon": "weather-sunny",
                "text": "Tema Claro",
                "theme_text_color": "Custom",
                "text_color": self.obj_app.theme_cls.opposite_bg_darkest,
                "viewclass": "IconListItem",
                "on_release": lambda x="claro": self.cambiar_tema(x),
            },
            {
                "icon": "moon-waning-crescent",
                "text": "Tema Oscuro",
                "theme_text_color": "Custom",
                "text_color": self.obj_app.theme_cls.opposite_bg_darkest,
                "viewclass": "IconListItem",
                "on_release": lambda x="oscuro": self.cambiar_tema(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.obj_home.ids.button,
            items=self.menu_items,
            max_height=dp(100),
            width_mult=dp(3),
        )

    def call_agreg(self):
        nombre = self.obj_agregar.ids.input_nombre_add
        cantidad = self.obj_agregar.ids.input_cantidad_add
        precio = self.obj_agregar.ids.input_precio_add
        descripcion = self.obj_agregar.ids.input_descrip_add
        try:
            mje = self.obj_c.agreg(nombre, cantidad, precio, descripcion)
        except ValueError as mje:
            print(mje)
            self.show_msg_popup(
                ["Error en la operación", "Campos cargados incorrectamente"]
            )
        else:
            self.show_msg_popup(mje)

    def call_elim(self):
        nombre = self.obj_eliminar.ids.input_nombre_elim

        mje = self.obj_c.elim(nombre)
        self.show_msg_popup(mje)

    def call_modif(self):
        nombre = self.obj_modificar.ids.input_nombre_mod
        cantidad = self.obj_modificar.ids.input_cantidad_mod
        precio = self.obj_modificar.ids.input_precio_mod
        descripcion = self.obj_modificar.ids.input_descrip_mod
        try:
            mje = self.obj_c.modif(nombre, cantidad, precio, descripcion)
        except ValueError as mje:
            print(mje)
            self.show_msg_popup(
                ["Error en la operación", "Campos cargados incorrectamente"]
            )
        else:
            self.show_msg_popup(mje)

    def show_msg_popup(self, mje):
        self.dialog = MDDialog(
            title=mje[0],
            type="custom",
            content_cls=MDLabel(
                text=mje[1],
                theme_text_color="Custom",
                text_color=self.obj_app.theme_cls.opposite_bg_darkest,
            ),
            buttons=[
                MDFlatButton(
                    text="Aceptar",
                    theme_text_color="Custom",
                    text_color=self.obj_app.theme_cls.primary_color,
                    on_release=self.close_msg_popup,
                ),
            ],
        )

        self.dialog.open()

    def close_msg_popup(self, obj):
        self.dialog.dismiss()
