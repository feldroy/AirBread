from pathlib import Path
import typer
from os import getenv
from mixedbread import Mixedbread
from rich import print

mxbai = Mixedbread(api_key=getenv('MIXEDBREAD_APIKEY'))

STORE_IDENTIFIER = "Air-Documentation"


def delete_current():
    results = mxbai.stores.files.list(
        store_identifier=STORE_IDENTIFIER,
        limit=100,
    )
    for record in results.data:
        print(f'[red bold]Deleting {record.filename}[/red bold]')
        res = mxbai.stores.files.delete(
            store_identifier=STORE_IDENTIFIER,
            file_id=record.id,
        )        

def ingest_latest(path: Path):
    doc_paths = path.glob('**/*.md')
    count = 0
    for fpath in doc_paths:
        strpath = str(fpath)
        print(f"Ingesting {strpath}")
        baselink = strpath.replace("../air/docs/", "")
        baselink = baselink.replace('index.md', '')
        baselink = baselink.replace('.md', '')
        link = f'https://feldroy.github.io/air/{baselink}'
        print(f'{link=}')
        vector_store_file = mxbai.stores.files.upload(
            store_identifier=STORE_IDENTIFIER,
            file=fpath,
            metadata={
               'link': link
            }
        )

        # print(f'{vector_store_file=}')
        count += 1
        # if count > 5: break


def main(path: Path):
    delete_current()
    ingest_latest(path)
    print('Done')


    # doc_paths = Path('../air/src/air').glob('**/*.md')




if __name__ == '__main__':
    typer.run(main)