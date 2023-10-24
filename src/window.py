import os
import shutil
import gi
from gi.repository import Gtk, Gdk

def validar_fps(valor):
    return len(valor) <= 3 and (valor.isdigit() or valor == "")

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 500)
        self.set_title("FastHud")

        self.grid = Gtk.Grid()
        self.set_child(self.grid)

        # botão Apply
        left_space = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid.attach(left_space, 0, 1, 1, 1)
        left_space.set_hexpand(True)

        self.button = Gtk.Button(label="  Apply  ")
        self.grid.attach(self.button, 1, 5, 1, 1)
        self.button.set_margin_bottom(20)
        self.button.connect("clicked", self.on_button_clicked)

        style_provider = Gtk.CssProvider()
        css = '''
        .custom-button {
            background-color: #234fdb;
        }
        .custom-button:active {
            background-color: #3A3A3A;
        }
        '''
        style_provider.load_from_data(css, -1)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.button.get_style_context().add_class('custom-button')

        right_space = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid.attach(right_space, 2, 1, 1, 1)
        right_space.set_hexpand(True)

        expanding_space = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.grid.attach(expanding_space, 0, 0, 3, 3)
        expanding_space.set_vexpand(True)

        self.grid.set_row_homogeneous(False)

        self.topleft_checkbox = Gtk.CheckButton(label="Top Left")
        self.grid.attach(self.topleft_checkbox, 0, 0, 1, 1)
        self.topleft_checkbox.set_halign(Gtk.Align.START)
        self.topleft_checkbox.set_valign(Gtk.Align.START)
        self.topleft_checkbox.connect("toggled", self.on_corner_checkbox_toggled)

        self.topright_checkbox = Gtk.CheckButton(label="Top Right")
        self.grid.attach(self.topright_checkbox, 2, 0, 1, 1)
        self.topright_checkbox.set_halign(Gtk.Align.END)
        self.topright_checkbox.set_valign(Gtk.Align.START)
        self.topright_checkbox.connect("toggled", self.on_corner_checkbox_toggled)

        self.bottomleft_checkbox = Gtk.CheckButton(label="Bottom Left")
        self.grid.attach(self.bottomleft_checkbox, 0, 2, 1, 1)
        self.bottomleft_checkbox.set_halign(Gtk.Align.START)
        self.bottomleft_checkbox.set_valign(Gtk.Align.END)
        self.bottomleft_checkbox.connect("toggled", self.on_corner_checkbox_toggled)

        self.bottomright_checkbox = Gtk.CheckButton(label="Bottom Right")
        self.grid.attach(self.bottomright_checkbox, 2, 2, 1, 1)
        self.bottomright_checkbox.set_halign(Gtk.Align.END)
        self.bottomright_checkbox.set_valign(Gtk.Align.END)
        self.bottomright_checkbox.connect("toggled", self.on_corner_checkbox_toggled)

        #botões  centrais
        self.topcenter_checkbox = Gtk.CheckButton(label="Top Center")
        self.grid.attach(self.topcenter_checkbox, 1, 0, 1, 1)
        self.topcenter_checkbox.set_halign(Gtk.Align.CENTER)
        self.topcenter_checkbox.set_valign(Gtk.Align.START)
        self.topcenter_checkbox.connect("toggled", self.on_corner_checkbox_toggled)

        self.bottomcenter_checkbox = Gtk.CheckButton(label="Bottom Center")
        self.grid.attach(self.bottomcenter_checkbox, 1, 2, 1, 1)
        self.bottomcenter_checkbox.set_halign(Gtk.Align.CENTER)
        self.bottomcenter_checkbox.set_valign(Gtk.Align.END)
        self.bottomcenter_checkbox.connect("toggled", self.on_corner_checkbox_toggled)

        checkbox_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.grid.attach(checkbox_box, 1, 0, 1, 3)
        checkbox_box.set_spacing(10)

        top_checkbox = Gtk.CheckButton(label="Layout Vertical")
        top_checkbox.connect("toggled", self.on_checkbox_toggled)
        checkbox_box.append(top_checkbox)
        checkbox_box.set_margin_top(80)

        middle_checkbox = Gtk.CheckButton(label="Layout Vertical Complete")
        middle_checkbox.connect("toggled", self.on_checkbox_toggled)
        checkbox_box.append(middle_checkbox)

        bottom_checkbox = Gtk.CheckButton(label="Layout Horizontal")
        bottom_checkbox.connect("toggled", self.on_checkbox_toggled)
        checkbox_box.append(bottom_checkbox)
        checkbox_box.set_margin_bottom(80)

        self.slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.5, 1.5, 0.1)
        self.slider.set_draw_value(True)
        self.slider.set_digits(2)
        self.slider.set_size_request(150, -1)
        self.slider.set_margin_start(1)

        self.slider.add_mark(0.5, Gtk.PositionType.BOTTOM, "Small")
        self.slider.add_mark(1.0, Gtk.PositionType.BOTTOM)
        self.slider.add_mark(1.5, Gtk.PositionType.BOTTOM, "Big")

        self.grid.attach(self.slider, 1, 3, 1, 1)

        self.grid.set_column_homogeneous(True)
        self.grid.set_column_spacing(10)
        self.slider.set_halign(Gtk.Align.CENTER)

        self.layout_vertical_checkbox = top_checkbox
        self.vertical_complete_checkbox = middle_checkbox
        self.layout_horizontal_checkbox = bottom_checkbox

        self.top_left_checkbox = self.topleft_checkbox
        self.top_right_checkbox = self.topright_checkbox
        self.bottom_left_checkbox = self.bottomleft_checkbox
        self.bottom_right_checkbox = self.bottomright_checkbox

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("FPS Limit (0 = unlimited)")
        self.entry.set_max_length(3)
        self.entry.set_input_purpose(Gtk.InputPurpose.DIGITS)
        self.entry.set_input_hints(
            Gtk.InputHints.SPELLCHECK | Gtk.InputHints.NO_EMOJI
        )
        self.entry.connect("changed", self.on_entry_changed)
        self.grid.attach(self.entry, 1, 4, 1, 1)
        self.entry.set_margin_bottom(20)

    def on_checkbox_toggled(self, button):
        for child in button.get_parent():
            if child != button:
                child.set_active(False)

    def on_corner_checkbox_toggled(self, button):
        checkboxes = [
            self.topleft_checkbox,
            self.topcenter_checkbox,
            self.topright_checkbox,
            self.bottomleft_checkbox,
            self.bottomcenter_checkbox,
            self.bottomright_checkbox,
        ]
        for checkbox in checkboxes:
            if checkbox != button:
                checkbox.set_active(False)

    def on_entry_changed(self, entry):
        text = entry.get_text()
        if text and not text.isdigit():
            entry.set_text("")

    def on_button_clicked(self, button):
        valor_fps = self.entry.get_text()

        if not valor_fps:
            valor_fps = "0"

        valor_scale = self.slider.get_value()

        if validar_fps(valor_fps):
            self.mostrar_opcoes(int(valor_fps), valor_scale)
        else:
            print("Digite no máximo 3 dígitos.")

    def on_slider_value_changed(self, scale):
        value = scale.get_value()
        print("Valor selecionado:", value)

    def mostrar_opcoes(self, valor_fps, valor_scale):
        caminho_config = os.path.expanduser("~/.config/MangoHud/MangoHud.conf")
        caminho_backup = os.path.expanduser("~/.config/MangoHud/backupMangoHud.conf")

        os.makedirs(os.path.dirname(caminho_config), exist_ok=True)

        conteudo_horizontal = """
horizontal
legacy_layout=0
table_columns=20
background_alpha=0

gpu_stats
gpu_temp
gpu_load_change
gpu_load_value=50,90
gpu_load_color=FFFFFF,FFAA7F,CC0000
gpu_text=GPU
gpu_color=FEBD9D
gpu_core_clock

cpu_stats
cpu_temp
cpu_load_change
core_load_change
cpu_load_value=50,90
cpu_load_color=FFFFFF,FFAA7F,CC0000
cpu_color=FEBD9D
cpu_text=CPU
cpu_mhz

vram
vram_color=FFAA7F

ram
ram_color=62A0EA

fps
fps_color_change
fps_value=30,60,144
fps_color=b22222,fdfd09,39f900

engine_color=FFAA7F


frame_timing=1
frametime_color=00ff00
background_alpha=0.4
font_size=22
gamemode
device_battery=gamepad
gamepad_battery_icon
vulkan_driver
position=top-left
round_corners=10

toggle_hud=F1

fps_limit={}
font_scale={}
"""

        conteudo_vertical = """
legacy_layout=false
gpu_stats
gpu_temp
gpu_load_change
gpu_load_value=50,90
gpu_load_color=FFFFFF,FFAA7F,CC0000
gpu_text=GPU
cpu_stats
cpu_temp
cpu_load_change
core_load_change
cpu_load_value=50,90
cpu_load_color=FFFFFF,FFAA7F,CC0000
cpu_color=2e97cb
cpu_text=CPU
io_color=a491d3
vram
vram_color=FEBD9D
ram
ram_color=FEBD9D
fps
engine_color=eb5b5b
gpu_color=2e9762
wine_color=eb5b5b
frame_timing=1
frametime_color=00ff00
media_player_color=ffffff
background_alpha=0.4
font_size=32

background_color=020202
position=top
text_color=ffffff
round_corners=10

toggle_hud=F1

fps_limit={}
font_scale={}
"""

        conteudo_vertical_complete = """
legacy_layout=false
gpu_stats
gpu_temp
gpu_core_clock
gpu_mem_clock
gpu_power
gpu_load_change
gpu_load_value=50,90
gpu_load_color=FFFFFF,FFAA7F,CC0000
gpu_text=GPU
cpu_stats
cpu_temp
core_load
cpu_power
cpu_mhz
cpu_load_change
core_load_change
cpu_load_value=50,90
cpu_load_color=FFFFFF,FFAA7F,CC0000
cpu_color=2e97cb
cpu_text=CPU
io_stats
io_read
io_write
io_color=a491d3
swap
vram
vram_color=ad64c1
ram
ram_color=c26693
fps
engine_version
engine_color=eb5b5b
gpu_name
gpu_color=2e9762
vulkan_driver
arch
wine
wine_color=eb5b5b
frame_timing=1
frametime_color=00ff00
frame_count
show_fps_limit
resolution
gamemode
gamepad_battery
gamepad_battery_icon
battery
position=top

toggle_hud=F1

fps_limit={}
font_scale={}
"""

        opcao_horizontal = self.layout_horizontal_checkbox.get_active()
        opcao_vertical = self.layout_vertical_checkbox.get_active()
        opcao_vertical_complete = self.vertical_complete_checkbox.get_active()

        posicao = ""
        if self.top_left_checkbox.get_active():
            posicao = "top-left"
            self.top_right_checkbox.set_active(False)
            self.bottom_left_checkbox.set_active(False)
            self.bottom_right_checkbox.set_active(False)
        elif self.top_right_checkbox.get_active():
            posicao = "top-right"
            self.top_left_checkbox.set_active(False)
            self.bottom_left_checkbox.set_active(False)
            self.bottom_right_checkbox.set_active(False)
        elif self.bottom_left_checkbox.get_active():
            posicao = "bottom-left"
            self.top_left_checkbox.set_active(False)
            self.top_right_checkbox.set_active(False)
            self.bottom_right_checkbox.set_active(False)
        elif self.bottom_right_checkbox.get_active():
            posicao = "bottom-right"
            self.top_left_checkbox.set_active(False)
            self.top_right_checkbox.set_active(False)
            self.bottom_left_checkbox.set_active(False)
        elif self.topcenter_checkbox.get_active():
            posicao = "top-center"
            self.top_left_checkbox.set_active(False)
            self.top_right_checkbox.set_active(False)
            self.bottom_left_checkbox.set_active(False)
            self.bottom_right_checkbox.set_active(False)
        elif self.bottomcenter_checkbox.get_active():
            posicao = "bottom-center"
            self.top_left_checkbox.set_active(False)
            self.top_right_checkbox.set_active(False)
            self.bottom_left_checkbox.set_active(False)
            self.bottom_right_checkbox.set_active(False)
        else:
            print("Selecione uma opção de posição!")
            return


        if opcao_horizontal and not (opcao_vertical or opcao_vertical_complete):
            conteudo_config = conteudo_horizontal.replace("position=top", f"position={posicao}")
        elif opcao_vertical and not (opcao_horizontal or opcao_vertical_complete):
            conteudo_config = conteudo_vertical.replace("position=top", f"position={posicao}")
        elif opcao_vertical_complete and not (opcao_horizontal or opcao_vertical):
            conteudo_config = conteudo_vertical_complete.replace("position=top", f"position={posicao}")
        else:
            print("Selecione apenas uma opção!")
            return

        if not os.path.isfile(caminho_config):
            try:
                with open(caminho_config, "w") as config_file:
                    config_file.write(conteudo_config)
                print("Arquivo de configuração criado!")
            except IOError as e:
                print(f"Erro ao criar o arquivo de configuração: {str(e)}")
                return

        try:
            shutil.copy2(caminho_config, caminho_backup)
            print("Cópia de backup criada com sucesso!")
        except IOError as e:
            print(f"Erro ao criar cópia de backup: {str(e)}")
            return

        conteudo_config = conteudo_config.replace("fps_limit={}", f"fps_limit={valor_fps}")
        conteudo_config = conteudo_config.replace("font_scale={}", f"font_scale={valor_scale}")

        try:
            with open(caminho_config, "w") as config_file:
                config_file.write(conteudo_config)
            print("Arquivo de configuração atualizado!")
        except IOError as e:
            print(f"Erro ao atualizar o arquivo de configuração: {str(e)}")

