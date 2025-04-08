# FastHud
![image](https://github.com/user-attachments/assets/0fc35144-873c-425d-9e90-998f005b0900)



Easily configure MangoHud with pre-defined settings while having the option to adjust layouts between vertical and horizontal orientations. Additionally, the app automatically creates a backup of the previous MangoHud.conf file upon clicking the 'Apply' button."


[Download Flatpak Bundle](https://github.com/fastoslinux/FastHud/releases/download/0.1/io.github.fastoslinux.fasthud.flatpak)


SETUP

Install Mangohud (Flatpak or whatever):

Need Flathub and GNOME 47 runtime installed

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


