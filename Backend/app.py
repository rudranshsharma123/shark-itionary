
import os
import sys

import click
from jina import Flow, Document, DocumentArray
import logging

from dataset import input_index_data

MAX_DOCS = int(os.environ.get("JINA_MAX_DOCS", 10000))
cur_dir = os.path.dirname(os.path.abspath(__file__))


def config():
    os.environ.setdefault('JINA_WORKSPACE', os.path.join(cur_dir, 'workspace'))
    os.environ.setdefault(
        'JINA_WORKSPACE_MOUNT',
        f'{os.environ.get("JINA_WORKSPACE")}:/workspace/workspace')
    os.environ.setdefault('JINA_LOG_LEVEL', 'INFO')
    os.environ.setdefault('JINA_PORT', str(45678))


def index_restful():
    flow = Flow().load_config('flows/flow-index.yml', override_with={'protocol': 'http'})
    with flow:
        flow.block()





def index(num_docs, request_size):
    flow = Flow().load_config('flows/flow-index.yml')
    with flow:
        flow.post(on='/index',
                  inputs=input_index_data(num_docs, request_size),
                  request_size=request_size,
                  show_progress=True)




def query_restful():
    flow = Flow(cors=True).load_config('flows/flow-query.yml')
    flow.rest_api = True
    flow.protocol = 'http'
    with flow:
        flow.block()


@click.command()
@click.option('--task', '-t', type=click.Choice(['index', 'query_restful']), default='index')

def main(task):
    num_docs= MAX_DOCS
    request_size = 16
    config()
    workspace = os.environ['JINA_WORKSPACE']
    logger = logging.getLogger('cross-modal-search')
    if 'index' in task:
        if os.path.exists(workspace):
            logger.error(
                f'\n +------------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                           | \
                    \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
                    \n |                                   🤖🤖🤖                                           | \
                    \n +------------------------------------------------------------------------------------+'
            )
            sys.exit(1)
    if 'query' in task:
        if not os.path.exists(workspace):
            logger.error(f'The directory {workspace} does not exist. Please index first via `python app.py -t index`')
            sys.exit(1)

    if task == 'index':
        index(num_docs, request_size)
    
    elif task == 'query_restful':
        query_restful()


if __name__ == '__main__':
    main()
