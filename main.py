import asyncio

from fasthtml.common import *

from db_utils import get_eggs, get_num_of_not_yet_discovered_eggs, get_code_status, EGG_STATUS, EggCode, found_egg

tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
css = Style("""
    .x {border:black solid 1px}  
    .down {position:absolute;bottom:10px; right:10px} 
    .htmx-indicator{
        opacity:0;
        transition: opacity 500ms ease-in;
    }
    .htmx-request .htmx-indicator{
        opacity:1;
    }
    .htmx-request.htmx-indicator{
        opacity:1;
    }
    """)

app = FastHTML(hdrs=(tlink, dlink, css))


@app.route('/')
def get():
    first_form = Form(
        Input(
            inputmode="text",
            name="code",
            placeholder="Enter your code",
            cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ",
            style="margin:4px"
        ),
        Button(
            "Check",
            Img(id="spinner", cls="htmx-indicator", src="https://htmx.org/img/bars.svg", alt="Loading",
                style="height: 16px;"),
            type="submit",
            cls="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            style="margin:4px; display: flex; align-items: center; gap: 8px;"
        ),
        hx_post="/check",
        id="main_from",
        cls="flex justify-center items-center space-x-4, space-y-4",
    )

    page = Body(
        Div(
            H1(
                f"Il en reste ",
                A(f"{get_num_of_not_yet_discovered_eggs()}",
                  cls="text-blue-500 hover:text-blue-700 font-semibold",
                  href="/list"),
                " ...",
                id="main_title",
                cls="text-4xl font-bold text-gray-100 m-4",
            ),
            first_form,
            cls="text-center space-y-8",
        ),
        cls="h-screen bg-gray-900 text-white flex items-center justify-center",
    )

    return page


@app.route('/check')
async def post(egg_code: EggCode):
    stutus = get_code_status(egg_code.code)
    if stutus == EGG_STATUS.NOT_FOUND:
        await asyncio.sleep(5)
        titre = H1(
            f"Désolé, cet Easter Egg n'existe pas ...",
            id="main_title",
            hx_swap_oob=true,
            cls="text-4xl font-bold text-gray-100 m-4",
        )
        return titre, Div("")
    if stutus == EGG_STATUS.ALREADY_FOUND:
        titre = H1(
            f"Désolé, cet Easter Egg a déjà été trouvé.",
            id="main_title",
            hx_swap_oob=true,
            cls="text-4xl font-bold text-gray-100 m-4",
        )
        return titre, Div("")

    # if we are here, then code is correct
    if egg_code.noma is not None and egg_code.noma != "" and egg_code.name is not None and egg_code.name != "":
        found_egg(egg_code)
        titre = H1(
            f"Bravo !  Ton easter egg a bien été enregistré",
            id="main_title",
            hx_swap_oob=true,
            cls="text-4xl font-bold text-gray-100 m-4",
        )
        return titre, Div("")

    titre = H1(
        f"Bravo ! Veillez encoder ces infos pour finaliser votre trouvaille",
        id="main_title",
        hx_swap_oob=true,
        cls="text-4xl font-bold text-gray-100 m-4",
    )
    full_form = Form(
        Input(
            inputmode="text",
            name="code",
            placeholder="egg_code",
            value=egg_code.code,
            cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ",
            style="margin:4px"
        ),
        Input(
            inputmode="text",
            name="name",
            value=egg_code.name,
            placeholder="John Doe",
            cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ",
            style="margin:4px"
        ),
        Input(
            inputmode="text",
            name="noma",
            value=egg_code.noma,
            placeholder="he42645",
            cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ",
            style="margin:4px"
        ),
        Button(
            "Send",
            type="submit",
            hx_indicator="#spinner",
            cls="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 ",
            style="margin:4px; width:auto"
        ),
        hx_post="/check",
        id="main_from",
        cls="flex justify-center items-center space-x-4, space-y-4",
    )

    return full_form, titre


def make_line(egg):
    color = "bg-blue-600" if egg['decouvert_par'] == "" else "bg-gray-700"
    line = Tr(
        Td(egg['id'], cls="border border-gray-700 px-4 py-2"),
        Td(egg['cours'], cls="border border-gray-700 px-4 py-2"),
        Td(egg['prof'], cls="border border-gray-700 px-4 py-2"),
        Td(egg['indice'], cls="border border-gray-700 px-4 py-2"),
        Td(egg['decouvert_par'], cls="border border-gray-700 px-4 py-2"),
        Td(egg['decouvert_le'], cls="border border-gray-700 px-4 py-2"),
        cls=color,
    ),
    return line


@app.route('/list')
def get():
    page = Div(
        A("home", href="/", cls="absolute top-4 right-4 text-blue-500 hover:text-blue-700 font-semibold"),
        H1("Suivi des Découvertes", cls="text-4xl font-bold text-gray-100 mb-8"),
        Div(
            Table(
                Thead(
                    Tr(
                        Th("ID", cls="border border-gray-700 px-4 py-2"),
                        Th("Cours", cls="border border-gray-700 px-4 py-2"),
                        Th("Prof", cls="border border-gray-700 px-4 py-2"),
                        Th("Indice", cls="border border-gray-700 px-4 py-2"),
                        Th("Découvert Par", cls="border border-gray-700 px-4 py-2"),
                        Th("Découvert Le", cls="border border-gray-700 px-4 py-2"),
                        cls="bg-gray-800",
                    )
                ),
                Tbody(
                    *[make_line(egg) for egg in get_eggs()]
                ),
                cls="table-auto w-full border-collapse border border-gray-700 text-left",
            ),
            cls="w-3/4",
        ),
        cls="h-screen bg-gray-900 text-white flex flex-col items-center justify-center",
    )

    return page


serve()
