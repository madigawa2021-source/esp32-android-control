import flet as ft
import requests
import traceback

# The default IP address for ESP32 in AP mode
ESP32_IP = "http://192.168.4.1"

def main(page: ft.Page):
    page.title = "ESP32 Controller"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Status and Log displays
    status_text = ft.Text("Connect to 'ESP32_Control' Wi-Fi", size=18, color=ft.colors.AMBER)
    error_log = ft.Text("", size=12, color=ft.colors.RED_300, italic=True)

    def send_command(endpoint):
        try:
            # We use a 2-second timeout so the app doesn't freeze
            response = requests.get(f"{ESP32_IP}/{endpoint}", timeout=2)
            if response.status_code == 200:
                status_text.value = response.text
                status_text.color = ft.colors.GREEN
                error_log.value = ""
            else:
                status_text.value = f"Error: {response.status_code}"
                status_text.color = ft.colors.RED
        except Exception as e:
            status_text.value = "ESP32 Not Found"
            status_text.color = ft.colors.RED
            error_log.value = f"Details: {str(e)}"
        
        page.update()

    # Layout Components
    controls = ft.Column(
        [
            ft.Icon(name=ft.icons.SETTINGS_REMOTE, size=100, color=ft.colors.BLUE_VIOLET),
            ft.Text("ESP32 Control", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, color="transparent"),
            status_text,
            error_log,
            ft.Divider(height=40, color="transparent"),
            ft.ElevatedButton(
                "ON", icon=ft.icons.LIGHTBULB,
                bgcolor=ft.colors.GREEN_700, color="white",
                width=200, height=60,
                on_click=lambda _: send_command("on")
            ),
            ft.ElevatedButton(
                "OFF", icon=ft.icons.LIGHTBULB_OUTLINE,
                bgcolor=ft.colors.RED_700, color="white",
                width=200, height=60,
                on_click=lambda _: send_command("off")
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    try:
        page.add(controls)
    except Exception:
        # If anything fails during startup, show the crash on screen!
        page.add(ft.Text(f"CRASH: {traceback.format_exc()}", color="red", size=10))

# Critical for Android: Do NOT use target=main directly in some environments,
# but for flet build apk, this standard way is usually correct.
if __name__ == "__main__":
    ft.app(target=main)
