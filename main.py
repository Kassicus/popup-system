import PySimpleGUI as sg

header_text = "Your System Uptime Has Exceeded 24 Hours"
body_text = """This is just a warning that your system uptime has exceeded 24 hours.\n
If your system uptime exceeds 7 days you will be required to reboot.\n
We recommend saving and closing all programs and running any available\n
windows updates followed by a reboot at your earliest convienience."""

confirm_text = "Acknowledge"

color_nexus_blue = "#0099D8"
color_nexus_light_gray = "#EDEDEE"

header_object = sg.Text(
    header_text,
    font=("Roboto", 24),
    text_color="#FFFFFF",
    background_color=color_nexus_blue,
    expand_x=True,
    justification="center",
    pad = (0, 0),
    size = (1000, 1),
    border_width=30
)
 
body_object = sg.Text(
    body_text,
    font = ("Roboto", 16),
    text_color="Black",
    background_color=color_nexus_light_gray,
    expand_x = True,
    justification="center"
) 

ack_button = sg.Button(
    confirm_text,
    font=("Roboto", 18),
    auto_size_button=True,
    button_color="Red",
    size=(40,1),
    pad = ((0, 0),(0, 30))
)

layout = [
    [header_object],
    [sg.VPush(background_color=color_nexus_light_gray)],
    [sg.Push(background_color=color_nexus_light_gray), body_object, sg.Push(background_color=color_nexus_light_gray)],
    [sg.VPush(background_color=color_nexus_light_gray)],
    [sg.Push(background_color=color_nexus_light_gray), ack_button, sg.Push(background_color=color_nexus_light_gray)]
]

window = sg.Window(
    'Notice from IT',
    layout,
    background_color = color_nexus_light_gray,
    disable_close = True,
    disable_minimize=True,
    keep_on_top = True,
    size = (800, 500),
    grab_anywhere = True,
    no_titlebar= True,
    margins = (0, 0),
    finalize = True,
)

window.ding()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Acknowledge':
        break

window.close()