import logging

log = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
