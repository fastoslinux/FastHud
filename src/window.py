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

         # Inicialização das variáveis de cores
        self.gpu_load_color = "FFFFFF,FFAA7F,CC0000"  # Azul por padrão
        self.cpu_load_color = "FFFFFF,FFAA7F,CC0000"  # Azul por padrão
        self.memory_load_color = ""  # Verde por padrão
        self.disk_load_color = ""    # Vermelho por padrão
        self.network_load_color = "" # Amarelo por padrão
        # Se você tiver outras variáveis de cor, defina-as aqui
        self.gpu_color = "2e9762"         # Azul por padrão
        self.cpu_color = "2e97cb"         # Azul por padrão

        # botão Apply
        left_space = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid.attach(left_space, 0, 1, 1, 1)
        left_space.set_hexpand(True)

        self.button = Gtk.Button(label="  Apply  ")
        self.grid.attach(self.button, 1, 8, 1, 1)
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
        style_provider.load_from_data(css.encode(), -1)
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

        #botões centrais
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
        self.slider.set_value(1.0)

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
        self.entry.connect("activate", self.on_entry_activated)
        self.grid.attach(self.entry, 1, 4, 1, 1)
        self.entry.set_margin_bottom(20)

        #botão de cores
        # Criar o seletor de cores (ComboBoxText)
        self.color_selector = Gtk.ComboBoxText()
        self.color_selector.append("default", "Default")
        self.color_selector.append("blue", "Blue")
        self.color_selector.append("red", "Red")
        self.color_selector.append("green", "Green")
        self.color_selector.set_active(0)  # Azul inicial
        self.grid.attach(self.color_selector, 1, 5, 1, 1)
        self.color_selector.set_margin_bottom(20)
        self.color_selector.connect("changed", self.on_color_selected)








    def aplicar_cores(self, cor_selecionada):
        if cor_selecionada == "default":
            # Reset to default values
            self.gpu_load_color = "FFFFFF,FFAA7F,CC0000"  # Default value
            self.cpu_load_color = "FFFFFF,FFAA7F,CC0000"  # Default value
            self.gpu_color = "2e9762"  # Default value
            self.cpu_color = "2e97cb"  # Default value
            # Reset other colors to their default empty values
            self.battery_color = ""
            self.vram_color = ""
            self.ram_color = ""
            self.io_color = ""
            self.engine_color = ""
            self.frametime_color = ""
            self.background_color = ""
            self.text_color = ""
            self.media_player_color = ""
            self.network_color = ""
            self.wine_color = ""

        elif cor_selecionada == "blue":
            # Blue theme - make sure these are different from defaults
            self.gpu_load_color = "1E90FF,4682B4,0000CD"  # Different blues
            self.cpu_load_color = "1E90FF,4682B4,0000CD"  # Different blues
            self.battery_color = "ADD8E6"       # LightBlue
            self.gpu_color = "87CEFA"           # LightSkyBlue
            self.cpu_color = "5F9EA0"           # CadetBlue
            self.vram_color = "87CEEB"          # SkyBlue
            self.ram_color = "B0E0E6"           # PowderBlue
            self.io_color = "D3D3D3"            # LightGray
            self.engine_color = "B0C4DE"        # LightSteelBlue
            self.frametime_color = "D3D3D3"     # LightGray
            self.background_color = "F0F8FF"    # AliceBlue
            self.text_color = "000000"          # Preto
            self.media_player_color = "4682B4"  # SteelBlue
            self.network_color = "5F9EA0"       # CadetBlue
            self.wine_color = "ADD8E6"          # LightBlue

        elif cor_selecionada == "red":
            self.gpu_load_color = "FF4500"      # OrangeRed
            self.cpu_load_color = "FF4500"      # OrangeRed
            self.gpu_color = "FF6347"           # Tomato
            self.cpu_color = "F08080"           # LightCoral
            self.vram_color = "FF7F7F"          # LightPink
            self.ram_color = "F4A460"           # SandyBrown
            self.io_color = "D2691E"            # Chocolate
            self.engine_color = "FF6347"        # Tomato
            self.frametime_color = "FFE4E1"     # MistyRose
            self.background_color = "FAFAD2"    # LightGoldenrodYellow
            self.text_color = "000000"          # Preto
            self.media_player_color = "CD5C5C"  # IndianRed
            self.network_color = "F08080"       # LightCoral
            self.wine_color = "FFC0CB"          # Pink

        elif cor_selecionada == "green":
            self.gpu_load_color = "32CD32"      # LimeGreen
            self.cpu_load_color = "32CD32"      # LimeGreen
            self.battery_color = "B0E57C"       # OliveDrab (mais contraste e menos saturado que o PaleGreen)
            self.gpu_color = "8FBC8F"           # DarkSeaGreen (para não ser tão saturado)
            self.cpu_color = "2E8B57"           # SeaGreen (mais escuro que o ForestGreen)
            self.vram_color = "A2D9A2"          # LightOliveGreen (um verde mais suave e contrastante)
            self.ram_color = "FFD700"           # Gold (para quebrar o verde e aumentar o contraste)
            self.io_color = "D3D3D3"            # LightGray
            self.engine_color = "556B2F"        # DarkOliveGreen (mais contraste e não tão saturado)
            self.frametime_color = "D3FFD3"     # LightGreen
            self.background_color = "F0FFF0"    # HoneyDew
            self.text_color = "000000"          # Preto
            self.media_player_color = "32CD32"  # LimeGreen
            self.network_color = "2E8B57"       # SeaGreen
            self.wine_color = "FF7F50"          # Coral (quebra a monotonia do verde)




    def on_color_selected(self, widget):
        cor_selecionada = self.color_selector.get_active_id()

        if cor_selecionada == "default":
            # Deixe o Mangohud decidir a cor por padrão
            self.aplicar_cores("default")  # Aqui, você pode deixar o Mangohud fazer a escolha padrão
        else:
            self.aplicar_cores(cor_selecionada)



    def on_entry_activated(self, entry):
        # Chama a função que simula o clique no botão Apply
        self.on_button_clicked(self.button)



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

        # Verificar se o valor do FPS é válido
        if not validar_fps(valor_fps):
            print("Digite no máximo 3 dígitos.")
            return

        # Verificar se uma posição foi selecionada
        posicao_selecionada = (
            self.top_left_checkbox.get_active()
            or self.top_right_checkbox.get_active()
            or self.bottom_left_checkbox.get_active()
            or self.bottom_right_checkbox.get_active()
            or self.topcenter_checkbox.get_active()
            or self.bottomcenter_checkbox.get_active()
        )

        # Verificar se um layout foi selecionado
        layout_selecionado = (
            self.layout_vertical_checkbox.get_active()
            or self.vertical_complete_checkbox.get_active()
            or self.layout_horizontal_checkbox.get_active()
        )

        # Se nenhuma posição ou layout for selecionado, destacar os checkboxes e exibir mensagem
        if not posicao_selecionada or not layout_selecionado:
            self.aplicar_estilo_destaque()  # Destacar os checkboxes
            print("Selecione uma opção de posição e layout!")
            return

        # Se tudo estiver correto, prosseguir com a lógica
        self.mostrar_opcoes(int(valor_fps), valor_scale)



    def aplicar_estilo_destaque(self):
        # Adicionar um estilo CSS temporário para destacar os checkboxes
        css = '''
        .destaque {
            border: 2px solid red;
            border-radius: 5px;
            padding: 5px;
        }
        '''

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode(), -1)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Verificar se os checkboxes de layout estão marcados
        layout_selecionado = (
            self.layout_vertical_checkbox.get_active()
            or self.vertical_complete_checkbox.get_active()
            or self.layout_horizontal_checkbox.get_active()
        )

        # Verificar se os checkboxes de posição estão marcados
        posicao_selecionada = (
            self.top_left_checkbox.get_active()
            or self.top_right_checkbox.get_active()
            or self.bottom_left_checkbox.get_active()
            or self.bottom_right_checkbox.get_active()
            or self.topcenter_checkbox.get_active()
            or self.bottomcenter_checkbox.get_active()
        )

        # Aplicar o destaque condicionalmente
        if layout_selecionado and not posicao_selecionada:
            # Destacar apenas os checkboxes de posição
            checkboxes_posicao = [
                self.top_left_checkbox,
                self.top_right_checkbox,
                self.bottom_left_checkbox,
                self.bottom_right_checkbox,
                self.topcenter_checkbox,
                self.bottomcenter_checkbox,
            ]
            for checkbox in checkboxes_posicao:
                checkbox.get_style_context().add_class("destaque")

        elif posicao_selecionada and not layout_selecionado:
            # Destacar apenas os checkboxes de layout
            checkboxes_layout = [
                self.layout_vertical_checkbox,
                self.vertical_complete_checkbox,
                self.layout_horizontal_checkbox,
            ]
            for checkbox in checkboxes_layout:
                checkbox.get_style_context().add_class("destaque")

        # Remover o estilo após 3 segundos
        def remover_destaque():
            if layout_selecionado and not posicao_selecionada:
                for checkbox in checkboxes_posicao:
                    checkbox.get_style_context().remove_class("destaque")
            elif posicao_selecionada and not layout_selecionado:
                for checkbox in checkboxes_layout:
                    checkbox.get_style_context().remove_class("destaque")

        # Usar GLib.timeout_add para remover o destaque após 3 segundos
        from gi.repository import GLib
        GLib.timeout_add_seconds(3, remover_destaque)


    def on_slider_value_changed(self, scale):
        value = scale.get_value()
        print("Valor selecionado:", value)

    def mostrar_opcoes(self, valor_fps, valor_scale):
        # Determinar a posição primeiro
        posicao = ""
        if self.top_left_checkbox.get_active():
            posicao = "top-left"
        elif self.top_right_checkbox.get_active():
            posicao = "top-right"
        elif self.bottom_left_checkbox.get_active():
            posicao = "bottom-left"
        elif self.bottom_right_checkbox.get_active():
            posicao = "bottom-right"
        elif self.topcenter_checkbox.get_active():
            posicao = "top-center"
        elif self.bottomcenter_checkbox.get_active():
            posicao = "bottom-center"
        else:
            print("Selecione uma opção de posição!")
            return

        caminho_config = os.path.expanduser("~/.config/MangoHud/MangoHud.conf")
        caminho_backup = os.path.expanduser("~/.config/MangoHud/backupMangoHud.conf")

        # Verificar se o diretório ~/.config/MangoHud/ existe e criar se não existir
        diretorio_mangohud = os.path.expanduser("~/.config/MangoHud/")
        os.makedirs(diretorio_mangohud, exist_ok=True)

        conteudo_horizontal = f"""
    legacy_layout=0
    table_columns=20
    background_alpha=0
    horizontal

    gpu_stats
    gpu_temp
    gpu_load_change
    gpu_load_value=50,90
    gpu_load_color={self.gpu_load_color}
    gpu_text=GPU
    gpu_color={self.gpu_color}
    gpu_core_clock

    cpu_stats
    cpu_temp
    cpu_load_change
    core_load_change
    cpu_load_value=50,90
    cpu_load_color={self.cpu_load_color}
    cpu_color={self.cpu_color}
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
    fps_metrics=avg,0.01,0.001

    engine_color=FFAA7F

    frame_timing=1
    frametime_color=00ff00
    background_alpha=0.4
    font_size=22
    gamemode
    device_battery=gamepad
    gamepad_battery_icon
    vulkan_driver
    position={posicao}
    round_corners=10

    toggle_hud=F1

    fps_limit={valor_fps}
    font_scale={valor_scale}
    """

        conteudo_vertical = f"""
    legacy_layout=false
    gpu_stats
    gpu_temp
    gpu_load_change
    gpu_load_value=50,90
    gpu_load_color={self.gpu_load_color}
    gpu_text=GPU
    cpu_stats
    cpu_temp
    cpu_load_change
    core_load_change
    cpu_load_value=50,90
    cpu_load_color={self.cpu_load_color}
    cpu_color={self.cpu_color}
    cpu_text=CPU
    io_color=a491d3
    vram
    vram_color=FEBD9D
    ram
    ram_color=FEBD9D

    fps
    fps_color_change
    fps_value=30,60,144
    fps_color=b22222,fdfd09,39f900

    engine_color=eb5b5b
    gpu_color={self.gpu_color}
    wine_color=eb5b5b
    frame_timing=1
    frametime_color=00ff00
    media_player_color=ffffff
    background_alpha=0.4
    font_size=32

    background_color=020202
    position={posicao}
    text_color=ffffff
    round_corners=10

    toggle_hud=F1

    fps_limit={valor_fps}
    font_scale={valor_scale}
    """

        conteudo_vertical_complete = f"""
    legacy_layout=false

    round_corners=10.0

    gpu_stats
    gpu_temp
    gpu_core_clock
    gpu_mem_clock
    gpu_power
    gpu_load_change
    gpu_load_value=50,90
    gpu_load_color={self.gpu_load_color}
    gpu_text=GPU
    cpu_stats
    cpu_temp
    core_load
    cpu_power
    cpu_mhz
    cpu_load_change
    core_load_change
    cpu_load_value=50,90
    cpu_load_color={self.cpu_load_color}
    cpu_color={self.cpu_color}
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
    fps_color_change
    fps_value=30,60,144
    fps_color=b22222,fdfd09,39f900
    fps_metrics=avg,0.01,0.001

    engine_version
    engine_color=eb5b5b
    gpu_name
    gpu_color={self.gpu_color}
    vulkan_driver
    arch
    wine
    wine_color=eb5b5b
    frame_timing=1
    frametime_color=00ff00
    show_fps_limit
    resolution
    gamemode
    gamepad_battery
    gamepad_battery_icon
    battery
    position={posicao}

    toggle_hud=F1

    fps_limit={valor_fps}
    font_scale={valor_scale}
    """

        opcao_horizontal = self.layout_horizontal_checkbox.get_active()
        opcao_vertical = self.layout_vertical_checkbox.get_active()
        opcao_vertical_complete = self.vertical_complete_checkbox.get_active()

        if opcao_horizontal and not (opcao_vertical or opcao_vertical_complete):
            conteudo_config = conteudo_horizontal
        elif opcao_vertical and not (opcao_horizontal or opcao_vertical_complete):
            conteudo_config = conteudo_vertical
        elif opcao_vertical_complete and not (opcao_horizontal or opcao_vertical):
            conteudo_config = conteudo_vertical_complete
        else:
            print("Selecione apenas uma opção de layout!")
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

        try:
            with open(caminho_config, "w") as config_file:
                config_file.write(conteudo_config)
            print("Arquivo de configuração atualizado!")
        except IOError as e:
            print(f"Erro ao atualizar o arquivo de configuração: {str(e)}")
