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
    small_form = Form(
        Input(
            inputmode="text",
            name="code",
            placeholder="Enter your code",
            cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ",
            style="margin:4px"
        ),
        Button(
            "Check",
            Img(id="spinner", cls="htmx-indicator",
                src="https://raw.githubusercontent.com/SamHerbert/SVG-Loaders/5deed925369e57e9c58ba576ce303466984db501/svg-loaders/three-dots.svg",
                alt="Loading",
                style="height: 16px;"),
            type="submit",
            hx_indicator="#spinner",
            cls="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            style="margin:4px; display: flex; align-items: center; gap: 8px;"
        ),
        hx_post="/check",
        hx_target="body",
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
                cls="text-4xl font-bold text-gray-100 m-4",
            ),
            small_form,
            cls="text-center space-y-8",
        ),
        cls="h-screen bg-gray-900 text-white flex items-center justify-center",
        style="flex-direction: column",
        id="body"
    )

    return Title("TI Easter Eggs"), page


@app.route('/check')
async def post(egg_code: EggCode):
    status, finder = get_code_status(egg_code.code)
    if status == EGG_STATUS.NOT_FOUND:
        await asyncio.sleep(5)
        titre = H1(
            A("Désolé, cet Easter Egg n'existe pas...", href="/"),
            cls="text-4xl font-bold text-gray-100 m-4",
        )
        return titre
    if status == EGG_STATUS.ALREADY_FOUND:
        titre = H1(
            A(f"Bravo, tu as trouvé un Easter Egg ! ", NotStr('<br><br>'),
              "Malheureusement, il a déjà été trouvé par ", Span(finder, cls="text-blue-700"),
              NotStr('.<br>'),
              "Continue, ton heure de gloire viendra !",
              href="/"),
            cls="text-4xl font-bold text-gray-100 m-4",
        )
        return titre

    # if we are here, then code is correct
    if egg_code.noma is not None and egg_code.noma != "" and egg_code.name is not None and egg_code.name != "":
        egg_code.name = egg_code.name.title()
        db_egg = found_egg(egg_code)
        titre = H1(
            f"Bravo {egg_code.name} !  Tu as validé l'Easter Egg numéro ",
            A(f'{db_egg.get("id")}', href="/list", cls="text-blue-500 hover:text-blue-700 font-semibold", ),
            cls="text-4xl font-bold text-gray-100 m-4",
        )
        return titre

    # if we are here, then the code is correct, but we don't have all the information yet

    titre = H1(
        f"Bravo ! Veillez encoder ces infos pour finaliser votre trouvaille",
        id="main_title",
        cls="text-4xl font-bold text-gray-100 m-4",
    )
    full_form = Form(
        Div(
            Label(
                "Code Egg", _for="code", cls="mb-2 text-sm font-medium text-gray-300"
            ),
            Input(
                inputmode="text",
                name="code",
                placeholder="egg_code",
                value=egg_code.code,
                cls="bg-gray-700 border border-gray-600 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full",
            ),
            cls="flex flex-col",
        ),
        Div(
            Label(
                "Nom Complet", _for="name", cls="mb-2 text-sm font-medium text-gray-300"
            ),
            Input(
                inputmode="text",
                name="name",
                value=egg_code.name,
                placeholder="John Doe",
                cls="bg-gray-700 border border-gray-600 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full",
            ),
            cls="flex flex-col",
        ),
        Div(
            Label(
                "Numéro Étudiant",
                _for="noma",
                cls="mb-2 text-sm font-medium text-gray-300",
            ),
            Input(
                inputmode="text",
                name="noma",
                value=egg_code.noma,
                placeholder="he42645",
                cls="bg-gray-700 border border-gray-600 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full",
            ),
            id="main_from",
            cls="flex flex-col",
        ),
        Button(
            "Envoyer",
            inputmode="submit",
            hx_indicator="#spinner",
            cls="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
        ),
        hx_post="/check",
        hx_target="body",
        hx_swap="outerHTML",
        cls="max-w-md w-full mx-auto p-6 space-y-4 bg-gray-800 rounded-lg shadow-md m-5",
    )

    return titre, full_form


def make_line(egg):
    color = "bg-gray-700" if egg['decouvert_par'] else "bg-blue-600"
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
            cls="w-3/4 overflow-x-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200",
        ),
        cls="h-screen bg-gray-900 text-white flex flex-col items-center justify-center",
    )

    return Title("TI Easter Eggs"), page


serve()
