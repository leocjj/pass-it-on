"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""
from typing import Optional
from time import sleep
from multiprocessing import Manager, Queue

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import app, run, ui
from nicegui import events

import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

# in reality users passwords would obviously need to be hashed
passwords = {'user1': 'pass1', 'admin': 'admin'}

unrestricted_page_routes = {'/login'}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.
    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)

class Demo:
    def __init__(self):
        self.number = 1

def heavy_computation(q: Queue) -> str:
    """Run some heavy computation that updates the progress bar through the queue."""
    n = 50
    for i in range(n):
        # Perform some heavy computation
        sleep(0.05)

        # Update the progress bar through the queue
        q.put_nowait(i / n)
    return 'Done!'

app.add_middleware(AuthMiddleware)

@ui.page('/')
def main_page() -> None:
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')

    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.button("Go to content", on_click=lambda: ui.navigate.to('/subpage'))
        ui.button(on_click=logout, icon='logout').props('outline round')


@ui.page('/subpage')
def test_page() -> None:
    ui.label('This is a sub page.')
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.tabs() as tabs:
            ui.tab('Components')
            ui.tab('Widgets')
            ui.tab('Dataframe')

    with ui.left_drawer() as left_drawer:
        ui.label('Side menu')
        dark = ui.dark_mode()
        ui.label('Switch mode:')
        ui.button('Dark', on_click=dark.enable)
        ui.button('Light', on_click=dark.disable)

    with ui.tab_panels(tabs, value='Components').classes('w-full'):
        with ui.tab_panel('Widgets'):
            ui.label('Content of Widgets')
            
            async def start_computation():
                progressbar.visible = True
                result = await run.cpu_bound(heavy_computation, queue)
                ui.notify(result)
                progressbar.visible = False

            # Create a queue to communicate with the heavy computation process
            queue = Manager().Queue()
            # Update the progress bar on the main process
            ui.timer(0.1, callback=lambda: progressbar.set_value(queue.get() if not queue.empty() else progressbar.value))

            # Create the UI
            ui.button('compute', on_click=start_computation)
            progressbar = ui.linear_progress(value=0).props('instant-feedback')
            progressbar.visible = False

            ui.separator()
            ui.date(value='2025-02-25', on_change=lambda e: result.set_text(e.value))
            result = ui.label()

            ui.separator()
            ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')

            def mouse_handler(e: events.MouseEventArguments):
                color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
                ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
                ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

            ui.separator()
            src = 'https://picsum.photos/id/565/640/360'
            ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)

            ui.separator()
            with ui.carousel(animated=True, arrows=True, navigation=True).props('height=180px'):
                with ui.carousel_slide().classes('p-0'):
                    ui.image('https://picsum.photos/id/30/270/180').classes('w-[270px]')
                with ui.carousel_slide().classes('p-0'):
                    ui.image('https://picsum.photos/id/31/270/180').classes('w-[270px]')
                with ui.carousel_slide().classes('p-0'):
                    ui.image('https://picsum.photos/id/32/270/180').classes('w-[270px]')

        with ui.tab_panel('Dataframe'):
            ui.label('Content of Dataframe')
            df = pd.DataFrame(data={
                'col1': [x for x in range(4)],
                'col2': ['This', 'column', 'contains', 'strings.'],
                'col3': [x / 4 for x in range(4)],
                'col4': [True, False, True, False],
            })


            def update(*, df: pd.DataFrame, r: int, c: int, value):
                df.iat[r, c] = value
                ui.notify(f'Set ({r}, {c}) to {value}')


            with ui.grid(rows=len(df.index)+1).classes('grid-flow-col'):
                for c, col in enumerate(df.columns):
                    ui.label(col).classes('font-bold')
                    for r, row in enumerate(df.loc[:, col]):
                        if is_bool_dtype(df[col].dtype):
                            cls = ui.checkbox
                        elif is_numeric_dtype(df[col].dtype):
                            cls = ui.number
                        else:
                            cls = ui.input
                        cls(value=row, on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))

            ui.separator()
            from random import random

            echart = ui.echart({
                'xAxis': {'type': 'value'},
                'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
                'legend': {'textStyle': {'color': 'gray'}},
                'series': [
                    {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
                    {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
                ],
            })

            def update():
                echart.options['series'][0]['data'][0] = random()
                echart.update()

            ui.button('Update', on_click=update)

        with ui.tab_panel('Components'):
            ui.label('Content of Components')
            def show(event: events.ValueChangeEventArguments):
                name = type(event.sender).__name__
                ui.notify(f'{name}: {event.value}')

            with ui.row():
                ui.button('Button 1', on_click=lambda: ui.notify('Click'))
                ui.button('Button 2', on_click=lambda: ui.notify('Click'))

            with ui.row():
                ui.button(icon='add', on_click=lambda: ui.notify('Click'))
                ui.button(icon='add', on_click=lambda: ui.notify('Click')).props('outline')
                ui.button(icon='add', on_click=lambda: ui.notify('Click')).props('flat')

            with ui.row():
                ui.checkbox('Checkbox', on_change=show)
                ui.checkbox('Checkbox', on_change=show).props('checked')
                ui.checkbox('Checkbox', on_change=show)
                ui.separator()
                ui.switch('Switch', on_change=show)
                ui.switch('Switch', on_change=show).props('checked')
                ui.switch('Switch', on_change=show).props('checked')

            ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')

            with ui.row():
                ui.input('Text input', on_change=show)
                ui.select(['One', 'Two'], value='One', on_change=show)
            
            ui.separator()
            ui.label('Value Binding')
            demo = Demo()
            v = ui.checkbox('visible', value=True)
            with ui.column().bind_visibility_from(v, 'value'):
                ui.slider(min=1, max=3).bind_value(demo, 'number')
                ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
                ui.number().bind_value(demo, 'number')

            ui.separator()
            ui.chat_message(['Hello NiceGUI!', 'I am a robot.'],
                name='Robot',
                stamp='now',
                avatar='https://robohash.org/ui')

            ui.separator()
            with ui.button(icon='colorize') as button:
                ui.color_picker(on_pick=lambda e: button.classes(f'!bg-[{e.color}]'))

            ui.separator()
            def alert():
                ui.run_javascript('alert("Hello!")')
            ui.button('fire and forget', on_click=alert)

            ui.separator()
            ui.add_css('''
                .red {
                    color: red;
                }
            ''')
            ui.label('This is red with CSS.').classes('red')

            ui.add_head_html('''
                <style>
                    .my-red-label {
                        color: Crimson;
                        font-weight: bold;
                    }
                </style>
            ''')
            ui.label('This is red with with HTML').classes('my-red-label')

            ui.link('And many more...', 'https://nicegui.io/documentation', new_tab=True).classes('mt-8')

@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
    return None


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED', port=8090, reload=False)