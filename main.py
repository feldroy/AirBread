import air
from os import getenv
from mixedbread import AsyncMixedbread
from mistletoe import markdown

app = air.Air()

mxbai = AsyncMixedbread(api_key=getenv('MIXEDBREAD_APIKEY'))


@app.page
def index():
    title = 'AirBread'
    return air.layouts.mvpcss(
        air.Title(title),
        air.H1(title),
        air.P('Mixedbread AI search of Air documentation and code.'),
        air.Form(
            air.Fieldset(
                air.Input(type="search", name="q", placeholder="Search"),
                air.Input(type="submit", value="Go!"),
                role="group",
            ),
            hx_get="/search",
            hx_target='#result',
            hx_swap="none",             
        ),

        air.Div(
            air.Article(air.Pre(air.Code("Response will go here")), id="result"),
        ),        
    )

@app.page
async def search(q: str):
    res = await mxbai.stores.search(
            query=q,
            store_identifiers=["Air-Documentation"],
            top_k=5,
        )

    for chunk in res.data:
        print(
            # f"Score: {chunk.score:.4f}, File: {chunk.filename}, Chunk: {chunk.text or 'Non-text content'}..."
            f"Score: {chunk.score:.4f}, File: {chunk.filename}"    
        )
        print(            f'Metadata: {chunk.metadata}'        )
    return air.Div(
        *[air.Article(

            air.H3(air.A(f"{chunk.score:.4f}: {chunk.filename}", href=chunk.metadata['link'])),
            air.Raw(markdown(f'{chunk.text or 'Non-text content'}')),
            air.Hr()
        ) for chunk in res.data],
        id='result',
        hx_swap_oob="true"
    )