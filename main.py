from fasthtml.common import *

tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
css = Style('.x {border:black solid 1px}  .down {position:absolute; bottom:10px; right:10px} ')

app = FastHTML(hdrs=(tlink, dlink, picolink, css))


@app.route('/')
def get():
    page = Body(
        Div(
            H1(
                "Il en reste encore 6 :o",
                id="main_title",
                cls="text-4xl font-bold text-gray-100 m-4",
            ),
            Form(
                Div(
                    Input(
                        inputmode="text",
                        name="input_data",
                        placeholder="Enter your code",
                        cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    Button(
                        "Check",
                        inputmode="submit",
                        cls="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    cls="flex justify-center items-center space-x-4",
                ),
                action="/premiere-page.html",
                method="GET",
                cls="space-y-4",
            ),
            Form(
                Div(
                    Input(
                        inputmode="text",
                        name="full_name",
                        placeholder="Name",
                        cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    Input(
                        inputmode="text",
                        name="noma",
                        placeholder="NOMA...",
                        cls="bg-gray-800 border border-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    Button(
                        "Envoyer",
                        inputmode="submit",
                        cls="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    cls="flex justify-center items-center space-x-4",
                ),
                action="/deuxieme-page.html",
                method="GET",
                cls="space-y-4",
            ),
            cls="text-center space-y-8",
        ),
        cls="h-screen bg-gray-900 text-white flex items-center justify-center",
    )

    return page


@app.route('/list')
def get():
    page = Body(
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
                    Tr(
                        Td("1", cls="border border-gray-700 px-4 py-2"),
                        Td("Mathématiques", cls="border border-gray-700 px-4 py-2"),
                        Td("Dr. Dupont", cls="border border-gray-700 px-4 py-2"),
                        Td("Calcul avancé", cls="border border-gray-700 px-4 py-2"),
                        Td("Alice", cls="border border-gray-700 px-4 py-2"),
                        Td("2024-11-01", cls="border border-gray-700 px-4 py-2"),
                        cls="bg-gray-700",
                    ),
                    Tr(
                        Td("2", cls="border border-gray-700 px-4 py-2"),
                        Td("Physique", cls="border border-gray-700 px-4 py-2"),
                        Td("Mme. Bernard", cls="border border-gray-700 px-4 py-2"),
                        Td("Mécanique", cls="border border-gray-700 px-4 py-2"),
                        Td("Non découvert", cls="border border-gray-700 px-4 py-2"),
                        Td("Non découvert", cls="border border-gray-700 px-4 py-2"),
                        cls="bg-red-600",
                    ),
                    Tr(
                        Td("3", cls="border border-gray-700 px-4 py-2"),
                        Td("Chimie", cls="border border-gray-700 px-4 py-2"),
                        Td("Dr. Moreau", cls="border border-gray-700 px-4 py-2"),
                        Td("Synthèse organique", cls="border border-gray-700 px-4 py-2"),
                        Td("Bob", cls="border border-gray-700 px-4 py-2"),
                        Td("2024-11-10", cls="border border-gray-700 px-4 py-2"),
                        cls="bg-gray-700",
                    ),
                ),
                cls="table-auto w-full border-collapse border border-gray-700 text-left",
            ),
            cls="w-3/4",
        ),
        cls="h-screen bg-gray-900 text-white flex flex-col items-center justify-center",
    )

    return page


serve()
