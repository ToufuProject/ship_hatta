import os

# ウインドウの横幅
WIDTH = 1024
# ウインドウの高さ
HEIGHT = 768
# FPS(Frames Per Second)
FPS = 60#← youtube版はなくてもいいかもね
# タイトル
TITLE = "TOUFU"
# 重力
GRAVITY = 1
# ジャンプ力
JUMP_POWER = -15
# 背景色
BG_COLOR = (20, 20, 20)
# テキストカラー
TEXT_COLOR = (255, 255, 255)
# フォント
TEXT_FONT = None
# グリッドのラインカラー
GRID_COLOR = (200, 200, 200)
# ディレクトリを設定
BASE_DIR = os.path.dirname(__file__)
# 画像のディレクトリを設定
IMG_DIR = os.path.join(BASE_DIR, "imgs")
# サウンドのディレクトリを設定
SOUND_DIR = os.path.join(BASE_DIR, "sound")
# ゲームオーバーBGM
GAMEOVER_BGM = "game_over.ogg"
# ゲームクリアBGM
GAMECLEAR_BGM = "stage_clear.wav"
# スプライトシートのディレクトリを指定
PLAYER_SPRITESHEET_DIR = os.path.join(IMG_DIR, "alienBeige.png")
# ブロック用のスプライトシートのディレクトリを指定
BLOCK_SPRITESHEET_DIR = os.path.join(IMG_DIR, "tiles_spritesheet.png")
# オブジェクトサイズ
OBJECT_SIZE = 32
# プレイヤー横幅
PLAYER_WIDTH = 32
# プレイヤー縦幅
PLAYER_HEIGHT = int(PLAYER_WIDTH * 1.5)
# プレイヤースピード
SPEED = 2