""""
練習してみよう💋
"""
import pygame
import os

from sprites import *
from map import *
from setting import *



# pygameを初期化
pygame.init()
# ウインドウを初期化
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# タイトル設定
pygame.display.set_caption(TITLE)



# 継承してないから、()つかなくてもいいよ
class Game:
    def __init__(self):
        """
        初期化の時に呼び出される
        ここではゲームをどんなルールで動かすのかやどんな画像を使うのかという設定をする
        """
        pygame.init()
        # 音声の読み込みと再生を行うmixerモジュールを初期化
        pygame.mixer.init()
        # 時間の管理
        self.clock = pygame.time.Clock()
        # ウインドウサイズの設定
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        # これがないとdraw_textのところでロードにめちゃくちゃ時間かかって、ラグが出る
        self.font_name = TEXT_FONT

    def new(self):
        """
        ゲームオブジェクトを作成
        """
        # 空のスプライトグループを作成。これによりGroupに追加されたupdate関数を一括で実施できる
        self.all_sprites = pygame.sprite.Group()
        # ブロック専用のグループを作成。グループ分けをしておくことで衝突判定などの仕組みを作りやすくなる
        self.block_sprites = pygame.sprite.Group()
        # エネミー専用のグループを作成。グループ分けをしておくことで衝突判定などの仕組みを作りやすくなる
        self.enemy_sprites = pygame.sprite.Group()
        # ゴール専用のグループを作成。と思ったけど、ゴール一個しかないからグループ化する必要なし
        #self.goal_sprites = pygame.sprite.Group()
        # プレイヤーを初期化。初期化する際、このクラスを引数として渡す
        self.player = Player(self, PLAYER_SPRITESHEET_DIR, 0, 294, 68, 93)
        # プレイヤーをスプライトグループに追加
        self.all_sprites.add(self.player)
        self.load_map()
        self.load_sound_data()
        # 再生するBGMのファイルをロード
        #pygame.mixer.music.load(os.path.join(SOUND_DIR, "main_theme.ogg"))
        # 用意ができたので、ゲームループを実行！
        self.run()

    def load_map(self):
        self.map = Map(os.path.join(BASE_DIR, "map.txt"))
        #print("マップ", self.map.data)
        #print("行", self.map.row_num)
        #print("列", self.map.col_num)
        
        #col-1にするとなぜかできる。なんで？⇨改行をきちんと除去してなかったからだ！ココ　line = line.rstrip()  # 改行除去
        for row in range(self.map.row_num):
            for col in range(self.map.col_num):
                #print("行:", row, "","列:", col, "値:", self.map.data[row][col])
                #print("col:",col)
                if self.map.data[row][col] == "B":
                    block = Block(BLOCK_SPRITESHEET_DIR, 0, 864, 70, 70)
                    block.set_position(col*OBJECT_SIZE, row*OBJECT_SIZE)
                    self.all_sprites.add(block)
                    self.block_sprites.add(block)
                elif self.map.data[row][col] == "E":
                    enemy = Enemy(BLOCK_SPRITESHEET_DIR, 72, 216, 70, 70)
                    enemy.set_position(col*OBJECT_SIZE, row*OBJECT_SIZE)
                    self.all_sprites.add(enemy)
                    self.enemy_sprites.add(enemy)
                elif self.map.data[row][col] == "G":
                    self.goal = Block(BLOCK_SPRITESHEET_DIR, 288, 360, 70, 70)
                    self.goal.set_position(col*OBJECT_SIZE, row*OBJECT_SIZE)
                    # オフセットを使ってゴールの位置もずらしたいので、all_spritesには追加しないといかん
                    self.all_sprites.add(self.goal)
                    #self.goal_sprites.add(self.goal)

    def load_sound_data(self):
        # 各サウンドを初期化。BGMじゃないよ。
        self.jump_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "small_jump.ogg"))
        self.bump_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "bump.ogg"))

    def run(self):
        """
        ゲームループの実行
        ゲームは
        ・イベント入力情報の取得
        ・入力情報をもとに内容を更新
        ・更新した情報で描画
        を繰り返すよ
        """
        # その前にBGMを再生。loops=-1にすると無限リピート
        #pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            # FPSでゲームループを実行
            self.clock.tick(FPS)
            # こうするとゲーム全体の更新が止まるので、クリア後に敵に接触したりプレイヤーがジャンプするなどを防止できる！これで良くない？
            self.event()
            self.update()
            self.draw()
        # BGMを止める
        #pygame.mixer.music.stop()


    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False


    def calc_offset(self, target):
        # プレイヤーのマップ上のx座標をスクリーン上のx座標に変換（オフセット）
        offset_x = -target.rect.x + WIDTH//2
        offset_y = -target.rect.y + HEIGHT//2
        #print("offset_x:", offset_x)
        #print("offset_y:", offset_y)
        return offset_x, offset_y


    def update(self):
        self.all_sprites.update()


    def draw_grid(self):
        """グリッドの描画"""
        # 縦方向にグリッドのラインを作成
        for x in range(0, WIDTH, OBJECT_SIZE):
            # 第１がどこに描画？第２が何色で？どこから（第３引数）、どこまで（第４引数）線を引く？
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))

        # 横方向にグリッドのラインを作成
        for y in range(0, HEIGHT, OBJECT_SIZE):
            # 第１がどこに描画？第２が何色で？どこから（第３引数）、どこまで（第４引数）線を引く？
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))


    def apply(self, object, offset):
        # ゲームオブジェクトを引数に指定した距離だけ移動させる
        return object.rect.move(offset)

    def draw(self):
        # ウインドウの背景を塗りつぶす
        self.screen.fill(BG_COLOR)
        # オフセットを計算
        offset = self.calc_offset(self.player)
        # グリッドを描画
        #self.draw_grid()
        # ウインドウ上（screen上）にスプライト（ゲームオブジェクト）を表示（描画）。引数で指定した場所に表示する（描画する）。
        #self.all_sprites.draw(self.screen)
        # 上のdrawを改造
        for sprite in self.all_sprites:
            #self.screen.blit(sprite.image, sprite.rect)が通常の形だけど、これをカメラ移動用に変更
            self.screen.blit(sprite.image, self.apply(sprite, offset))

        # 画面のチラつきを抑えるためダブルバッファリングを実施
        pygame.display.flip()

    def game_over(self):
        """ゲームオーバー時に画面を表示"""
        # これがないと罰ボタン押した時、ゲームオーバーじゃない時もゲームオーバーの画面が出てしまう
        if not self.running:
            return
        pygame.mixer.music.load(os.path.join(SOUND_DIR, "game_over.ogg"))
        # loops=-1にしてはいかんよ
        pygame.mixer.music.play()
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48, TEXT_COLOR, WIDTH / 2, HEIGHT / 2 - 25)
        self.draw_text("Press Enter to restart", 22, TEXT_COLOR, WIDTH / 2, HEIGHT / 2 + 25)
        pygame.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        """
            テキストの表示
            手順は
            １：Font オブジェクトを作成
            ２：Fontオブジェクトを使ってテキストを描画したSurfaceを作成
            ３：Surfaceを画面に描画
            https://aidiary.hatenablog.com/entry/20080504/1275694644
        """
        # Noneにするとデフォルトのフォント（freesansbold.ttf）になる。
        # sysFont使うとラグい
        # 第１引数にはNoneを直接指定してもいい。self.font_nameにしてるのは、フォントをカスタマイズしやすいようにするため
        # https://shizenkarasuzon.hatenablog.com/entry/2018/12/29/203344
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def wait_for_key(self):
        """ボタンを押すまで待機"""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                # イベントのうち、特定のキーが押された時
                if event.type == pygame.KEYDOWN:
                    # 押されたキーがスペースの時
                    if event.key == K_SPACE:
                        waiting = False


game = Game()
while game.running:
    game.new()
    game.game_over()

pygame.quit()