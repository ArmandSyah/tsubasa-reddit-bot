import pprint
from crunchyroll.apis.meta import MetaApi

pp = pprint.PrettyPrinter(indent=4)
api = MetaApi()
cowboy_bebop = list(api.search_anime_series('Jojo'))[0]
pp.pprint(cowboy_bebop)
