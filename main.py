import air
from os import getenv
from mixedbread import AsyncMixedbread
from mistletoe import markdown
from pathlib import Path
from typing import Any

app = air.Air()

mxbai = AsyncMixedbread(api_key=getenv('MIXEDBREAD_APIKEY'))


def layout(*children,  **kwargs):
    body_tags = air.layouts.filter_body_tags(children)
    head_tags = air.layouts.filter_head_tags(children)

    return air.Html(
        air.Head(
            air.Style(Path('bonkers.css').read_text()),
            air.Script(
                src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
                integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
                crossorigin="anonymous",
            ),
            *head_tags,
        ),
        air.Body(air.Main(*body_tags, class_="bonkers")),
    )


@app.page
def index(q: str | None = None):
    title = 'AirBread'
    return layout(
        air.Title(title),
        air.Script("""function updateQinURL() {
            let url = new URL(window.location);
            const value = document.getElementById('q').value
            url.searchParams.set('q', value);
            window.history.pushState({}, '', url);            
        };
        """),        
        air.H1(title),
        air.P('Mixedbread AI search of Air documentation and code.'),
        air.Form(
            air.Fieldset(
                air.Input(type="search", id="q", value=q, name="q", placeholder="Search", autofocus=True),
                air.Button(
                    "Search",
                    hx_get="/search",
                    hx_target="#results",
                    hx_include="#q",
                    onclick="updateQinURL()",
                ),                
                # air.Input(type="submit", value="Go!"),
                role="group",
            ), 
        ),
        air.Div(
            air.Article(air.Pre(air.Code("Response will go here")), id="results"),
        ),        
    )

@app.page
async def search(q: str):
    res = await mxbai.stores.search(
            query=q,
            store_identifiers=["Air-Documentation"],
            top_k=5,
        )
    return air.Div(
        *[air.Article(
            air.H3(air.A(chunk.metadata['link'].replace('https://', ''), href=chunk.metadata['link'])),
            air.Raw(markdown(f'{chunk.text or 'Non-text content'}')),
            air.Hr()
        ) for chunk in res.data],
        id='results',
        hx_swap_oob="true"
    )