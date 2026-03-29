import flet as ft
import requests

# The default IP address for ESP32 in AP mode is usually 192.168.4.1
ESP32_IP = "http://192.168.4.1"

def main(page: ft.Page):
    page.title = "ESP32 Controller"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600

    status_text = ft.Text("Connect to 'ESP32_Control' Wi-Fi", size=18, color=ft.colors.AMBER)

    def send_command(endpoint):
        try:
            response = requests.get(f"{ESP32_IP}/{endpoint}", timeout=2)
            if response.status_code == 200:
                status_text.value = response.text
                status_text.color = ft.colors.GREEN
            else:
                status_text.value = f"Error: {response.status_code}"
                status_text.color = ft.colors.RED
        except requests.exceptions.RequestException as e:
            status_text.value = "ESP32 Not Found (Check Wi-Fi)"
            status_text.color = ft.colors.RED
        
        page.update()

    def turn_on(e):
        send_command("on")

    def turn_off(e):
        send_command("off")

    # UI Components
    page.add(
        ft.Column(
            [
                ft.Icon(name=ft.icons.SETTINGS_REMOTE, size=100, color=ft.colors.BLUE_VIOLET),
                ft.Text("ESP32 Remote Control", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color="transparent"),
                status_text,
                ft.Divider(height=40, color="transparent"),
                ft.ElevatedButton(
                    text="TURN LED ON",
                    icon=ft.icons.LIGHTBULB,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN_700,
                    width=250,
                    height=60,
                    on_click=turn_on
                ),
                ft.ElevatedButton(
                    text="TURN LED OFF",
                    icon=ft.icons.LIGHTBULB_OUTLINE,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.RED_700,
                    width=250,
                    height=60,
                    on_click=turn_off
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
