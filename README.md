# Pokemon-Terminal（日本語対応 fork）

[![CI](https://github.com/m-hikichi/Pokemon-Terminal/actions/workflows/ci.yml/badge.svg)](https://github.com/m-hikichi/Pokemon-Terminal/actions/workflows/ci.yml)

ターミナルの背景・デスクトップの壁紙を、ポケモンの画像に変えるCLIツールです。
[LazoVelko/Pokemon-Terminal](https://github.com/LazoVelko/Pokemon-Terminal) の fork で、**日本語まわりを強化**しています。

- 🇯🇵 **日本語名でそのまま指定できる** — `pokemon ピカチュウ`（本家は英語名 / ID のみ）
- 📖 **ヘルプも日本語** — `pokemon -h` が実行例つきの日本語ガイドになっている
- ⚡ **1コマンドで導入** — `uv tool install` の手順を用意

```bash
pokemon ピカチュウ           # 日本語名で指定
pokemon 25                   # ID で指定
pokemon -r kanto -t fire     # カントー地方のほのおタイプからランダム
pokemon -c                   # 元に戻す
```

<p align="center">
  <img src="https://i.imgur.com/n34fXyp.png" width="700" alt="Pikachu preview" />
  <img src="https://i.imgur.com/bLajJfw.png" width="430" alt="Bulbasaur preview" />
  <img src="https://i.imgur.com/ZzQhJuE.png" width="430" alt="Squirtle preview" />
  <img src="https://i.imgur.com/54fvKOQ.png" width="430" alt="Charizard preview" />
  <img src="https://i.imgur.com/xaHPMUd.png" width="430" alt="Eevee preview" />
  <img src="https://i.imgur.com/W41EHr2.png" width="430" alt="Clefairy preview" />
</p>

## インストール

サポート・動作検証の対象は、このREADMEの `uv tool install --python 3.12` による導入です。
CIはuv 0.13.8・Python 3.12のWindows・macOS・Linuxで通常の導入環境を再現します。
pip・npm・手動配置など、ここに記載したuv以外の導入方法はサポート・検証・動作保証の対象外です。
ホストOSやターミナルの全パッケージの安全性を保証するものではありません。

### uv

`pokemon` コマンドを普段使いするなら、`uv tool install` で専用の隔離環境に入れるのが手軽です。

`uv --version` が0.13.8でない場合は、次の手順でインストール・更新します。

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.13.8/install.ps1 | iex"
```

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/0.13.8/install.sh | sh
```

このリポジトリをGitHubから直接インストール:

```bash
uv tool install --python 3.12 "git+https://github.com/m-hikichi/Pokemon-Terminal.git"
```

更新する場合:

```bash
uv tool upgrade pokemon-terminal
```

以前の手順で導入した環境を揃え直す場合:

```bash
uv tool install --force --python 3.12 "git+https://github.com/m-hikichi/Pokemon-Terminal.git"
```

### アンインストール

```bash
uv tool uninstall pokemon-terminal
```

## 使い方

```bash
pokemon [オプション] [ID または 名前]
```

よく使う例:

```bash
pokemon                   # ランダムに1匹
pokemon 25                # ID で指定
pokemon pikachu           # 英語名で指定
pokemon ピカチュウ          # 日本語名で指定
pokemon -n saur           # 英語名の部分一致で絞り込んでランダム
pokemon -r kanto -t fire  # カントー地方のほのおタイプからランダム
pokemon -w                # ターミナルではなく壁紙を変更
pokemon -ss 5             # 5分ごとに切り替えるスライドショー
pokemon -c                # 元に戻す（スライドショーも停止）
```

**オプションの全一覧・絞り込み条件・実行例は `pokemon -h` を参照してください。**
日本語で、実行例つきで表示されます。

> `ichooseyou` は `pokemon` の別名として同時にインストールされます。どちらでも同じように使えます。

## 本家との違い

### 日本語名で指定できる

ポケモンを日本語名で呼び出せます。指定方法によって挙動が変わります。

| 書き方 | 挙動 |
|---|---|
| `pokemon ピカチュウ` | 完全一致で1匹を指定 |
| `pokemon -n フシギダネ` | 完全一致で絞り込み（日本語は部分一致に非対応） |
| `pokemon -n saur` | 英語名は部分一致で絞り込み（Bulbasaur / Ivysaur / Venusaur） |

対応表は [`pokemonterminal/Data/pokemon_ja.txt`](pokemonterminal/Data/pokemon_ja.txt) にあります。

### ヘルプが日本語

`pokemon -h` を日本語化し、実行例・絞り込み条件・スライドショーの停止方法を載せています。
本家は英語で、実行例はありません。

### uv での導入手順

本家 README には無い `uv tool install` の手順を用意しています。
Python 環境を汚さずに `pokemon` コマンドを導入・更新できます。

## 対応環境

### ターミナル

| ターミナル | 備考 |
|---|---|
| iTerm2 | |
| ConEmu | Cmder などの派生も可 |
| Terminology | |
| Tilix | |
| Windows Terminal | |
| Kitty | **0.27.0 以降** |

### 壁紙（デスクトップ）

| 環境 | 備考 |
|---|---|
| Windows | |
| macOS | |
| GNOME | |
| sway | |
| swww | `swww` コマンドとデーモンの起動が必要 |
| Openbox / i3wm | `feh` と `xprop` が必要 |

対応環境は起動時に自動判定されます。うまく動かない場合は `pokemon -dr` で
ポケモンの選択だけを確認し、背景の変更処理と切り分けてください。

## 日本語名データ

日本語名の対応表は [`pokemonterminal/Data/pokemon_ja.txt`](pokemonterminal/Data/pokemon_ja.txt) です。

- 1行目が No.001、2行目が No.002 ... の並び順で対応
- 空行は無視される
- 同じ名前が重複していると起動時にエラーになる

## カスタム画像を追加

以下のフォルダに `jpg` を置くと、候補に加わります。

- `pokemonterminal/Images/Extra`

追加した画像を含む一覧の確認:

```bash
pokemon -e -dr
```

## 開発・テスト

通常利用と同じuv tool環境へアプリをインストールした後、テスト用ツールを追加して検証します。
追加前の実行時依存を制約として使い、追加後も依存バージョンが変化していないことを検査します。
テストはソースツリーの外で実行し、インストール済みのアプリを読み込みます。

```bash
uv run --no-project --python 3.12 scripts/check_environment.py --test
```

Dockerは `alpine:3.23` とAlpine公式のPython 3.12パッケージを使う開発用の補助環境です。通常利用のサポート対象は上記のuvによる導入です。
Dockerでもuv toolでアプリをインストールし、同じ依存バージョンでテストします。
導入にはuvを使い、追加のpipはインストールしません。検査用だけでなく、このDocker環境自体を同じ構成で使います。

```bash
docker compose build --pull --no-cache test
docker compose run --rm test
```

## 依存パッケージのセキュリティ検査

[セキュリティ検査ワークフロー](.github/workflows/security-scan.yml) は、毎日日本時間09:00（UTC 00:00）、関連ファイルのPR変更時、手動操作で実行します。
定期実行と手動実行はデフォルトブランチへの反映後に利用できます。開始時刻は混雑により遅れることがあります。

- 通常利用環境: Windows・macOS・Linuxで `uv tool install --python 3.12` を実行し、その環境にインストールされた直接・間接依存をpip-auditで検査します。PRではGit URLの代わりに同じパッケージ内容のローカルコピーを導入します。
- 実行時依存: `setup.py` でバージョンを固定し、通常の導入・テスト・監査で共有します。ビルド依存は `pyproject.toml` に定義します。
- Docker: 開発用イメージ全体のPython・OSパッケージをTrivyで別途検査します。この結果はuv利用者のホストOSを検査した結果ではありません。
- 既知の脆弱性は重大度・修正版の有無を問わず失敗とし、取得・検査エラーでも失敗します。検査を通す目的でパッケージや指摘を除外しません。
- 検査レポートと解決された依存バージョンを失敗時もArtifactsへアップロードし、30日間保存します（キャンセル時を除く）。

ローカルで通常利用環境の依存を検査する場合:

```bash
uv run --no-project --python 3.12 scripts/check_environment.py --audit
```

検証時点の結果と残る指摘は[セキュリティ対応の検証記録](docs/security-remediation.md)を参照してください。
導入済みの古いバージョンが自動で更新されるわけではないため、`uv tool upgrade pokemon-terminal` で更新してください。

## upstream の更新を取り込む（fork 運用）

本家（`upstream`）の更新を fork（`origin`）へ反映する手順です。

```bash
git switch master
git fetch upstream
git rebase upstream/master
git push origin master
```

必要なら作業ブランチにも反映します。

```bash
git switch <your-branch>
git rebase master
```

## 補足

- 収録画像は第1世代〜第6世代（カントー〜カロス）のポケモンです。
- 画像はプロジェクトの著作権・ライセンス条件に従って利用してください。
- 一部のターミナルでは、透明度を手動で調整すると見やすくなります。

## クレジット

- 本家: [LazoVelko/Pokemon-Terminal](https://github.com/LazoVelko/Pokemon-Terminal)
- 画像作成・圧縮・各プラットフォーム対応のコントリビューターの皆さん
