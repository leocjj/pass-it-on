from nicegui import ui

ui.icon("thumb_up")
ui.markdown("This is **Markdown**.")
ui.html("This is <strong>HTML</strong>.")
ui.separator()

with ui.row():
    ui.label("This is a CSS label").style("color: #800; font-weight: bold")
    ui.label("This is a Tailwind label").classes("font-serif text-xl text-blue-500")
    ui.label("This is a Quasar label").classes("q-ml-xl text-lowercase text-h6 text-primary")
ui.separator()

ui.link("NiceGUI on GitHub", "https://github.com/zauberzeug/nicegui")

ui.link("NiceGUI examples", "https://github.com/zauberzeug/nicegui/tree/main/examples")

ui.run(binding_refresh_interval=1, port=8085, title="NiceGUI Demo")
