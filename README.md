# Pokemon-Terminal

[![Build Status](https://travis-ci.org/m-hikichi/Pokemon-Terminal.svg?branch=master)](https://travis-ci.org/m-hikichi/Pokemon-Terminal)

ターミナル背景・デスクトップ壁紙をポケモン画像に変更するCLIツールです。
このリポジトリでは、日本語名指定（例: `ピカチュウ`）にも対応しています。

## 特徴

- 719匹（第1世代〜第6世代）の背景画像を収録
- ポケモンを `ID` / `英語名` / `日本語名` で指定可能
- 地方・タイプ・明るさでフィルタ可能
- ターミナル背景と壁紙の両方に対応
- スライドショー表示に対応

## インストール後の表示イメージ

<p align="center">
  <img src="https://i.imgur.com/n34fXyp.png" width="700" alt="Pikachu preview" />
  <img src="https://i.imgur.com/bLajJfw.png" width="430" alt="Bulbasaur preview" />
  <img src="https://i.imgur.com/ZzQhJuE.png" width="430" alt="Squirtle preview" />
  <img src="https://i.imgur.com/54fvKOQ.png" width="430" alt="Charizard preview" />
  <img src="https://i.imgur.com/xaHPMUd.png" width="430" alt="Eevee preview" />
  <img src="https://i.imgur.com/W41EHr2.png" width="430" alt="Clefairy preview" />
</p>

## 対応環境

### ターミナル

- iTerm2
- ConEmu
- Terminology
- Windows Terminal
- Tilix
- Kitty

### 壁紙

- Windows
- macOS
- GNOME
- Openbox（feh）
- i3wm（feh）
- sway

## インストール

### uvでインストール

`pokemon` コマンドを普段使いする場合は、`uv tool install` で専用の隔離環境にインストールできます。

`uv` が未インストールの場合は、先にインストールします。

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

このリポジトリをGitHubから直接インストール:

```bash
uv tool install "git+https://github.com/m-hikichi/Pokemon-Terminal.git"
```

インストール済みのツールを更新する場合:

```bash
uv tool upgrade pokemon-terminal
```

### pipでインストール

```bash
pip install "git+https://github.com/m-hikichi/Pokemon-Terminal.git"
```

## アンインストール

uvでインストールした場合:

```bash
uv tool uninstall pokemon-terminal
```

pipでインストールした場合:

```bash
pip uninstall pokemon-terminal
```

## 使い方

```bash
pokemon [オプション] [id_or_name]
```

### 基本例

```bash
pokemon                 # ランダム
pokemon 25              # ID指定
pokemon pikachu         # 英語名指定
pokemon ピカチュウ        # 日本語名指定
pokemon -n bulb         # 英語名の部分一致
pokemon -n フシギダネ      # 日本語名の厳密一致
pokemon -r kanto -dr    # フィルタ結果を表示のみ（変更しない）
pokemon -w              # 壁紙を変更
pokemon -c              # ターミナル背景をクリア
```

## 日本語名データ

日本語名の対応表は以下にあります。

- `pokemonterminal/Data/pokemon_ja.txt`

仕様:
- 1行目がNo.001、2行目がNo.002... の対応
- 空行は無視
- 重複名があると起動時にエラー

## カスタム画像を追加

以下フォルダに `jpg` を置くと候補に入ります。

- `pokemonterminal/Images/Extra`

一覧確認:

```bash
pokemon -e -dr
```

## Dockerでテスト

このリポジトリには Docker テスト環境を用意しています（`python:3.10` ベース）。

```bash
docker compose run --rm test
```

## upstream更新を取り込む（fork運用）

本家（`upstream`）の更新を、あなたのfork（`origin`）へ反映する手順です。

```bash
git switch master
git fetch upstream
git rebase upstream/master
git push origin master
```

必要なら作業ブランチにも反映:

```bash
git switch <your-branch>
git rebase master
```

## 補足

- 画像はプロジェクトの著作権・ライセンス条件に従って利用してください。
- 一部ターミナルでは透明度設定を手動調整すると見やすくなります。

## クレジット

- Original project: [LazoCoder/Pokemon-Terminal](https://github.com/LazoCoder/Pokemon-Terminal)
- 画像作成・圧縮・各プラットフォーム対応のコントリビューターの皆さん
