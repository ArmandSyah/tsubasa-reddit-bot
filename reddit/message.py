import os

from anime.mal import malsearchmethods
from anime.mal.malanime import MalAnime
from anime.anilist import anilistsearchmethods
from anime.anidb import anidbsearchmethods


def make_message(title):
    """Constructs message to be sent to reddit user"""
    anime_info = _set_up(title)
    comment = _construct_comment(anime_info)
    print(comment)


def _set_up(title):
    mal_url = malsearchmethods.get_mal_links(title)
    anilist_url = anilistsearchmethods.get_anilist_links(title)
    anidb_url = anidbsearchmethods.get_anidb_links(title)
    anime = MalAnime(mal_url)

    comment_info_dict = {'mal_url': mal_url,
                         'anilist_url': anilist_url,
                         'anidb_url': anidb_url,
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

    comment.append(f'**Show Information:**\n')
    if anime_info["anilist_url"] is not None:
        comment.append(f'* [Anilist]({anime_info["anilist_url"]})')
    if anime_info["mal_url"] is not None:
        comment.append(f'* [MyAnimeList]({anime_info["mal_url"]})')
    if anime_info["anidb_url"] is not None:
        comment.append(f'* [AniDB]({anime_info["anidb_url"]})')

    comment.append('\n***** \n')

    comment.append(f'## Synopsis:\n')
    comment.append(f'{anime.synopsis}\n')

    comment.append('\n***** \n')

    comment.append(f'Source: {anime.source} | ')
    return '\n'.join(comment)


def main():
    make_message('Attack on Titan')

if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()