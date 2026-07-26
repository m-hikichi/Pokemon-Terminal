import sys
import argparse
import textwrap
import pokemonterminal.filters as filters
from pokemonterminal.database import Database


# 既定値はここに集約し、argparse の const/default とヘルプ文言の両方で使う。
# こうしておくと値を変えたときにヘルプが自動で追従する。
LIGHT_DEFAULT = 0.7
DARK_DEFAULT = 0.42
SLIDESHOW_DEFAULT = 10.0

# ヘルプの説明欄（インデント24）に収まる折り返し幅。
_HELP_WIDTH = 48


def _choices_block(values):
    """選択肢の一覧を、ヘルプの説明欄の幅に折り返した文字列にする。

    一覧をベタ書きせず Database から生成することで、地方やタイプが
    追加されたときにヘルプの更新漏れが起きないようにしている。
    """
    return '\n'.join(textwrap.wrap(' '.join(values), _HELP_WIDTH))


class _HelpFormatter(argparse.RawTextHelpFormatter):
    """`-n NAME, --name NAME` ではなく `-n, --name NAME` と表示する。

    メタ変数が短縮形と長い形の両方に繰り返されると左の列が無駄に長くなる。
    Python 3.13 以降の argparse は標準でこの形式なので、それに揃える。
    """

    def __init__(self, prog, **kwargs):
        # 既定の 24 だと -l だけが折り返され、隣の -d と不揃いになる。
        kwargs.setdefault('max_help_position', 25)
        super().__init__(prog, **kwargs)

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string


parser = argparse.ArgumentParser(
    prog='pokemon',
    add_help=False,
    usage='pokemon [オプション] [ID または 名前]',
    # 日本語は単語区切りの空白がなく既定のフォーマッタでは折り返されないため、
    # help 文字列の改行をそのまま出す RawText を使い、改行位置は手で決める。
    formatter_class=_HelpFormatter,
    description='ターミナルの背景 / デスクトップの壁紙を、ポケモンの画像に変更します。\n'
                'オプションを何も指定しない場合は、全ポケモンからランダムに1匹選ばれます。',
    epilog='使用例:\n'
           '  pokemon                      ランダムに1匹\n'
           '  pokemon 25                   ID で指定\n'
           '  pokemon pikachu              英語名で指定\n'
           '  pokemon ピカチュウ             日本語名で指定\n'
           '  pokemon -n saur              英語名の部分一致で絞り込んでランダム\n'
           '  pokemon -r kanto -t fire     カントー地方のほのおタイプからランダム\n'
           '  pokemon -l                   明るい画像だけからランダム\n'
           '  pokemon -w -r johto          ジョウト地方のポケモンを壁紙に設定\n'
           '  pokemon -ss 5 -t water       みずタイプを5分ごとに切り替え\n'
           '  pokemon -c                   背景を元に戻す / スライドショーを停止\n'
           '\n'
           '対応しているターミナル・壁紙環境は README を参照してください。')

_basic_group = parser.add_argument_group('基本')
# 排他グループを parser ではなく引数グループから作ることで、
# ID と -c が同じ見出しの下に並び、択一の関係が読み取れるようにする。
_either = _basic_group.add_mutually_exclusive_group()
_either.add_argument(
    'id',
    metavar='ID_OR_NAME',
    help='表示したいポケモンを1匹だけ指定します（完全一致）\n'
         '例: 25 / pikachu / ピカチュウ\n'
         '省略した場合は、下の絞り込み条件に合うポケモンから\n'
         'ランダムに1匹選ばれます',
    nargs='?',
    default=0, const=0)
_either.add_argument(
    '-c',
    '--clear',
    help='設定した背景を元に戻して終了します\n'
         'スライドショーが動いていれば、それも停止します\n'
         'ID・名前とは同時に指定できません',
    action='store_true')
_basic_group.add_argument(
    '-h',
    '--help',
    action='help',
    default=argparse.SUPPRESS,
    help='このヘルプを表示して終了します')

_filters_group = parser.add_argument_group(
    '絞り込み（条件に合うポケモンからランダムに1匹選ばれます）')
_filters_group.add_argument(
    '-n',
    '--name',
    metavar='NAME',
    help='名前で絞り込みます\n'
         '英語名は部分一致で絞り込めます\n'
         '（-n saur → Bulbasaur, Ivysaur, Venusaur）\n'
         '日本語名は完全一致のみ（-n フシギダネ）',
    action=filters.NameFilter,
    type=str.lower)
_filters_group.add_argument(
    '-r',
    '--region',
    metavar='REGION',
    help='地方で絞り込みます（複数指定できます）\n'
         + _choices_block(Database.REGIONS),
    action=filters.RegionFilter,
    choices=Database.REGIONS,
    nargs='*',
    type=str.lower)
_filters_group.add_argument(
    '-t',
    '--type',
    metavar='TYPE',
    help='タイプで絞り込みます（複数指定できます）\n'
         '第2タイプも判定の対象になります\n'
         + _choices_block(Database.POKEMON_TYPES),
    action=filters.TypeFilter,
    choices=Database.POKEMON_TYPES,
    nargs='*',
    type=str.lower)
_filters_group.add_argument(
    '-l',
    '--light',
    help='明るい画像だけに絞り込みます\n'
         f'指定値より明るいものが残ります（値の省略時は {LIGHT_DEFAULT:g}）\n'
         'このオプション自体を書かなければ絞り込みません',
    default=LIGHT_DEFAULT,
    const=LIGHT_DEFAULT,
    metavar='0.0-1.0',
    nargs='?',
    type=float,
    action=filters.LightFilter)
_filters_group.add_argument(
    '-d',
    '--dark',
    help='暗い画像だけに絞り込みます\n'
         f'指定値より暗いものが残ります（値の省略時は {DARK_DEFAULT:g}）\n'
         '-l と併用すると「その間の明るさ」に絞り込めます',
    default=DARK_DEFAULT,
    const=DARK_DEFAULT,
    metavar='0.0-1.0',
    nargs='?',
    type=float,
    action=filters.DarkFilter)
_filters_group.add_argument(
    '-ne',
    '--no-extras',
    help='特別画像（メガシンカ・フォルム違いなど）を除き、\n'
         '通常のポケモンだけを対象にします',
    nargs=0,
    action=filters.NonExtrasFilter)
_filters_group.add_argument(
    '-e',
    '--extras',
    help='逆に、その特別画像だけを対象にします',
    nargs=0,
    action=filters.ExtrasFilter)

_misc_group = parser.add_argument_group('動作の指定')
_misc_group.add_argument(
    '-w',
    '--wallpaper',
    help='ターミナルの背景ではなく、デスクトップの壁紙を変更します',
    action='store_true')
_misc_group.add_argument(
    '-ss',
    '--slideshow',
    help='1匹に固定せず、絞り込んだポケモンを一定間隔で切り替え\n'
         f'続けます（分単位 / 値の省略時は {SLIDESHOW_DEFAULT:g} 分）\n'
         'バックグラウンドで動作します\n'
         '止めるとき: pokemon -c （壁紙のときは pokemon -c -w）',
    const=SLIDESHOW_DEFAULT, nargs='?', type=float, metavar='MINUTES')
_misc_group.add_argument(
    '-v',
    '--verbose',
    help='条件に一致したポケモンの一覧を表示します',
    action='store_true')
_misc_group.add_argument(
    '-dr',
    '--dry-run',
    help='背景も壁紙も変更せず、結果の確認だけを行います\n'
         '（-v の内容もあわせて表示されます）',
    action='store_true')


is_slideshow = '-ss' in sys.argv or '--slideshow' in sys.argv
