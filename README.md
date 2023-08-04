# FastHud
![Captura de tela de 2023-07-23 13-32-21](https://github.com/fastoslinux/FastHud/assets/17401812/8dd7a41c-079a-4002-8531-d49544222a4e)


Easily configure MangoHud with pre-defined settings while having the option to adjust layouts between vertical and horizontal orientations. Additionally, the app automatically creates a backup of the previous MangoHud.conf file upon clicking the 'Apply' button."

Video Demo:

https://youtu.be/gf-XTDrDM7A

[Download Flatpak Bundle](https://github.com/fastoslinux/FastHud/releases/download/0.1/io.github.fastoslinux.fasthud.flatpak)


SETUP

Install Mangohud (Flatpak or whatever):

Need Flathub and GNOME 44 runtime installed

Flatpak:

``flatpak install org.freedesktop.Platform.VulkanLayer.MangoHud``

Steam Flatpak:

Set permissions with [Flatseal](https://flathub.org/pt-BR/apps/com.github.tchx84.Flatseal) or [terminal](https://docs.flatpak.org/en/latest/sandbox-permissions.html?highlight=permission):

Filesystem:

``xdg-config/MangoHud:ro``

Flatpak game:

Set permissions with [Flatseal](https://flathub.org/pt-BR/apps/com.github.tchx84.Flatseal) or [terminal](https://docs.flatpak.org/en/latest/sandbox-permissions.html?highlight=permission):

env:

``MANGOHUD=1``

Filesystem:

``xdg-config/MangoHud:ro``


