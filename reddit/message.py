import os

from anime.mal import mal_search_methods
from anime.mal.mal_anime import MalAnime
from anime.anilist import anilist_search_methods
from anime.anidb import anidb_search_methods
from anime.streams import stream_search_methods


def make_message(title):
    """Constructs message to be sent to reddit user"""
    anime_info = _set_up(title)
    comment = _construct_comment(anime_info)
    return comment


def _set_up(title):
    mal_url = mal_search_methods.get_mal_links(title)
    anilist_url = anilist_search_methods.get_anilist_links(title)
    anidb_url = anidb_search_methods.get_anidb_links(title)
    anime = MalAnime(mal_url)
    crunchyroll_url = (stream_search_methods.search_crunchyroll(anime.english_name)
                       if anime.english_name is not None
                       else stream_search_methods.search_crunchyroll(title))
    funimation_url = (stream_search_methods.search_funimation(anime.english_name)
                      if anime.english_name is not None
                      else stream_search_methods.search_funimation(title))
    animelab_url = (stream_search_methods.search_animelab(anime.english_name)
                    if anime.english_name is not None
                    else stream_search_methods.search_animelab(title))

    comment_info_dict = {'mal_url': mal_url,
                         'anilist_url': anilist_url,
                         'anidb_url': anidb_url,
                         'crunchy': crunchyroll_url,
                         'funi': funimation_url,
                         'animelab': animelab_url,
                         'anime': anime}

    return comment_info_dict


def _construct_comment(anime_info):
    comment = []
    anime = anime_info['anime']
    comment.append(f'# {anime.main_name} \n')

    comment.append('***** \n')

    comment.append(f'**Names:**\n')
    if anime.english_name is not None:
        comment.append(f'* English: {anime.english_name}')
    if anime.japanese_name is not None:
        comment.append(f'* Japanese: {anime.japanese_name}')
    if anime.synonyms is not None:
        comment.append(f'* Synonyms: {" , ".join(anime.synonyms)}')

    comment.append(f'\n**Show Information:**\n')
    if anime_info["anilist_url"] is not None:
        comment.append(f'* [Anilist]({anime_info["anilist_url"]})')
    if anime_info["mal_url"] is not None:
        comment.append(f'* [MyAnimeList]({anime_info["mal_url"]})')
    if anime_info["anidb_url"] is not None:
        comment.append(f'* [AniDB]({anime_info["anidb_url"]})')

    comment.append(f'\n**Streams:**\n')
    if anime_info["crunchy"] is not None:
        comment.append(f'* [Crunchyroll]({anime_info["crunchy"]})')
    if anime_info["funi"] is not None:
        comment.append(f'* [Funimation]({anime_info["funi"]})')
    if anime_info["animelab"] is not None:
        comment.append(f'* [Animelab (for Aus and NZ)]({anime_info["animelab"]})')

    comment.append('\n***** \n')

    comment.append(f'## Synopsis:\n')
    comment.append(f'{anime.synopsis}\n')

    comment.append('\n***** \n')

    comment.append(f'**Episodes:** {anime.episodes} |**Source:** {anime.source} | **Airdate:** {anime.airdate} | '
                   f'**Duration:** {anime.duration} |**Status:** {anime.status} | **Type:** {anime.anime_type} | '
                   f'**Rating:** {anime.rating}/10 | **Genres:** {", ".join(anime.genres)}')
    return '\n'.join(comment)


def main():
    print('Grimoire of Zero:\n {}'.format(make_message('Re Zero')))


if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()
