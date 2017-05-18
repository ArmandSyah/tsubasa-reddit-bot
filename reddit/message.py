from anime.mal import malsearchmethods
from anime.mal.malanime import MalAnime
from anime.anilist import anilistsearchmethods
from anime.anidb import anidbsearchmethods
from anime.streams import streamsearchmethods


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
    crunchyroll_url = streamsearchmethods.search_crunchyroll(title)
    funimation_url = streamsearchmethods.search_funimation(title)
    animelab_url = streamsearchmethods.search_animelab(title)

    comment_info_dict = {'mal_url': mal_url,
                         'anilist_url': anilist_url,
                         'anidb_url': anidb_url,
                         'crunchyroll_url': crunchyroll_url,
                         'funimation_url': funimation_url,
                         'animelab_url': animelab_url,
                         'anime': anime}

    return comment_info_dict


def _construct_comment(anime_info):
    comment = []
    anime = anime_info['anime']
    comment.append(f'# {anime.main_name} \n')
    comment.append('***** \n')

    comment.append(f'**Show Information:**\n')
    if anime_info["anilist_url"] is not None:
        comment.append(f'* [Anilist]({anime_info["anilist_url"]}) \n')
    if anime_info["mal_url"] is not None:
        comment.append(f'* [MyAnimeList]({anime_info["mal_url"]}) \n')
    if anime_info["anidb_url"] is not None:
        comment.append(f'* [AniDB]({anime_info["anidb_url"]}) \n')

    comment.append(f'**Streams:**\n')
    if anime_info["crunchyroll_url"] is not None:
        comment.append(f'* [Crunchyroll]({anime_info["crunchyroll_url"]}) \n')
    if anime_info["funimation_url"] is not None:
        comment.append(f'* [Funimation]({anime_info["funimation_url"]}) \n')
    if anime_info["animelab_url"] is not None:
        comment.append(f'* [AnimeLab]({anime_info["animelab_url"]}) \n')
    return ''.join(comment)


def main():
    print(make_message('Hinako Note'))

if __name__ == '__main__':
    main()