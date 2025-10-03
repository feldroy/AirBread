# from os import getenv
# from mixedbread import Mixedbread

# mxbai = Mixedbread(api_key=getenv('MIXEDBREAD_APIKEY'))

# res = mxbai.stores.search(
#     query="Create a minimal Air App",
#     store_identifiers=["Air Documentation"],
#     top_k=5,
# )

# for chunk in res.data:
#     print(
#         # f"Score: {chunk.score:.4f}, File: {chunk.filename}, Chunk: {chunk.text or 'Non-text content'}..."
#         f"Score: {chunk.score:.4f}, File: {chunk.filename}"
#     )

from os import getenv
from mixedbread import AsyncMixedbread
import typer
import asyncio

mxbai = AsyncMixedbread(api_key=getenv('MIXEDBREAD_APIKEY'))
# app = typer.Typer()


async def _search(query: str):
    res = await mxbai.stores.search(
            query=query,
            store_identifiers=["Air Documentation"],
            top_k=5,
        )

    for chunk in res.data:
        print(
            # f"Score: {chunk.score:.4f}, File: {chunk.filename}, Chunk: {chunk.text or 'Non-text content'}..."
            f"Score: {chunk.score:.4f}, File: {chunk.filename}"            
        )    


# @app.command()
def search(query: str):
    asyncio.run(_search(query))




if __name__ == "__main__":
    typer.run(search)