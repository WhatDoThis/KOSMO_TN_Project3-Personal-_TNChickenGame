import pygame, random

pygame.init()
pygame.mixer.init()

endgame = False

pygame.display.set_caption("TN Chicken Game By Woo")
gamepad_width = 1000
gamepad_height = 700
gamepad = pygame.display.set_mode((gamepad_width, gamepad_height))

game_sound = pygame.mixer.Sound("bgm\\chickenBGM.mp3")
game_sound.play(-1)

game_font = pygame.font.Font("font\\Maplestory Light.ttf", 20)
background = pygame.image.load("img2\\BackgroundCG.png")

time = pygame.time.Clock()


mania = pygame.image.load("img2\\ChickenMania.png")
mania_size = mania.get_rect().size
mania_width = mania_size[0]
mania_height = mania_size[1]
mania_x_pos = (gamepad_width/2) - (mania_width/2)
mania_y_pos = gamepad_height - mania_height
mania_speed = 0.4
mania_to_x = 0

eat = pygame.image.load("img2\\ChickenMania2.png")

weapon = pygame.image.load("img2\\fork.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 10


chicken_images = [
    pygame.image.load("img2\\chicken1.png"),
    pygame.image.load("img2\\chicken2.png"),
    pygame.image.load("img2\\chicken3.png"),
    pygame.image.load("img2\\chicken4.png")]

chicken_speed_y = [-20, -19, -18, -17]

chickens = []

# 최초 발생하는 큰 공 추가
chickens.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50, # 공의 y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3, # 공의 x축 이동 방향, -3이면 왼쪽으로 3이면 오른쪽으로
    "to_y" : -6, # 공의 y축 이동 방향
    "init_speed_y": chicken_speed_y[0]}) # y 최초 속도

weapon_to_remove = -1
chicken_to_remove = -1

total_time = 20
start_time = pygame.time.get_ticks() # 시작 시간 정의

game_result = "Game Over"

def text(text, color, x, y):
        text_content = game_font.render(text, True, color)
        text_rect = text_content.get_rect()
        text_rect.midtop = (x, y)
        gamepad.blit(text_content, text_rect)
    

gamepad.blit(background,(0,0))
gamepad.blit(mania,(mania_x_pos,mania_y_pos))
text("[3초 후 게임 시작]", (0,0,0), gamepad_width/2, gamepad_height/2-100)

pygame.display.update()
pygame.time.delay(3000)    

eat_count = 0
isEat = False    
running = True

while running:
    FPS = time.tick(60)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mania_to_x -= mania_speed
            elif event.key == pygame.K_RIGHT:
                mania_to_x += mania_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = mania_x_pos + (mania_width / 2) - (weapon_width / 2)
                weapon_y_pos = mania_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                mania_to_x = 0
                
    mania_x_pos += mania_to_x * FPS
    
    if mania_x_pos < 0:
        mania_x_pos = 0
    elif mania_x_pos > gamepad_width - mania_width:
        mania_x_pos = gamepad_width - mania_width
    
    # 무기 위치 조정 -> 무기 위치를 위로 올림  ex)100, 200 -> 180, 160, 140, ...
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
    
    # 치킨들 정의하기
    for chicken_idx, val in enumerate(chickens):
        chicken_pos_x = val["pos_x"]
        chicken_pos_y = val["pos_y"]
        chicken_img_idx = val["img_idx"]

        chicken_size = chicken_images[chicken_img_idx].get_rect().size
        chicken_width = chicken_size[0]
        chicken_height = chicken_size[1]

        # 가로벽에 닿았을 때 치킨 이동 위치 변경(튕겨 나오는 효과)
        if chicken_pos_x < 0 or chicken_pos_x > gamepad_width - chicken_width:
            val["to_x"] = val["to_x"] * -1

        # 세로 위치 -> 스테이지에 튕겨서 올라가는 처리
        if chicken_pos_y >= gamepad_height - chicken_height:
            val["to_y"] = val["init_speed_y"]
        else: # 그 외의 모든 경우에는 속도를 증가(시작값이 원래 음수) -> 포물선 효과
            val["to_y"] += 0.5

        val["pos_x"] += val["to_x"]
        val["pos_y"] += val["to_y"]
        
    # 캐릭터 정보 업데이트
    mania_rect = mania.get_rect()
    mania_rect.left = mania_x_pos
    mania_rect.top = mania_y_pos

    for chicken_idx, val in enumerate(chickens):
        chicken_pos_x = val["pos_x"]
        chicken_pos_y = val["pos_y"]
        chicken_img_idx = val["img_idx"]

        # 치킨 정보 업데이트
        chicken_rect = chicken_images[chicken_img_idx].get_rect()
        chicken_rect.left = chicken_pos_x
        chicken_rect.top = chicken_pos_y

        # 치킨과 캐릭터 충돌 체크
        if mania_rect.colliderect(chicken_rect):
            running = False
            break
        # 치킨과 무기들의 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(chicken_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                chicken_to_remove = chicken_idx # 해당 치킨 없애기 위한 값 설정

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if chicken_img_idx < 3:
                    # 나눠진 공 정보
                    small_chicken_rect = chicken_images[chicken_img_idx + 1].get_rect()
                    small_chicken_width = small_chicken_rect.size[0]
                    small_chicken_height = small_chicken_rect.size[1]

                    # 왼쪽으로 튕겨 나가는 작은 공
                    chickens.append({
                        "pos_x": chicken_pos_x + (chicken_width/2) - (small_chicken_width/2),  # 공의 x 좌표
                        "pos_y": chicken_pos_y + (chicken_height/2) - (small_chicken_height/2),  # 공의 y 좌표
                        "img_idx": chicken_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": -3,  # 공의 x축 이동 방향, -3이면 왼쪽으로 3이면 오른쪽으로
                        "to_y": -6,  # 공의 y축 이동 방향
                        "init_speed_y": chicken_speed_y[chicken_img_idx + 1]})  # y 최초 속도

                    # 오른쪽으로 튕겨 나가는 작은 공
                    chickens.append({
                        "pos_x": chicken_pos_x + (chicken_width/2) - (small_chicken_width/2),  # 공의 x 좌표
                        "pos_y": chicken_pos_y + (chicken_height/2) - (small_chicken_height/2),  # 공의 y 좌표
                        "img_idx": chicken_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 3,  # 공의 x축 이동 방향, -3이면 왼쪽으로 3이면 오른쪽으로
                        "to_y": -6,  # 공의 y축 이동 방향
                        "init_speed_y": chicken_speed_y[chicken_img_idx + 1]})  # y 최초 속도
                break
        else: # 계속 게임을 진행
            continue # 안쪽 for 문 조건이 맞지 않으면 continue. 바깥 for문 계속 수행
        break # 안쪽 for 문에서 break를 만나면 여기로 진입 가능. 2중 for 문을 한번에 탈출

    # 충돌된 공 또는 무기 없애기
    if chicken_to_remove > -1:
        del chickens[chicken_to_remove]
        chicken_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
        pygame.mixer.Sound("bgm\\chickenEAT.mp3").play()
        isEat = True

    # 모든 공을 없앤 경우 게임 종료(성공)
    if len(chickens) == 0:
        game_result = "Mission Complete"
        running = False
    
    
    gamepad.blit(background,(0,0))
    gamepad.blit(mania,(mania_x_pos,mania_y_pos))
    
    if isEat:
        gamepad.blit(eat,(mania_x_pos-20,mania_y_pos-60))
        eat_count += 1
        if eat_count > 15:
            eat_count = 0
            isEat = False
    
    for weapon_x_pos, weapon_y_pos in weapons:
        gamepad.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(chickens):
        chicken_pos_x = val["pos_x"]
        chicken_pos_y = val["pos_y"]
        chicken_img_idx = val["img_idx"]
        gamepad.blit(chicken_images[chicken_img_idx], (chicken_pos_x, chicken_pos_y))
    
    # 경과 시간 계산
    end_time = (pygame.time.get_ticks() - start_time) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - end_time)), True, (255, 0, 0))
    gamepad.blit(timer, (10, 10))
    
    
    # 시간 초과했다면
    if total_time - end_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()


text(game_result, (0,0,0), gamepad_width/2, gamepad_height/2-250)
text("[3초 대기 후 자동 꺼짐]", (0,0,0), gamepad_width/2, gamepad_height/2-100)

pygame.display.update()
game_sound.stop()
pygame.time.delay(500)
pygame.mixer.Sound("bgm\\chickenEND.mp3").play()
pygame.time.delay(2500)

pygame.quit()