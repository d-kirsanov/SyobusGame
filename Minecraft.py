from first_person_controller import FirstPersonController
from ursina import *
import math

app = Ursina()
player_enabled = True
p_key_held = False
original_world = []
world_size = 25 # x and y
world_depth = 5 # z

reach_distance = 5

player_starting_position = (12, 4, 12)

x_m = 20
z_m = 15
h_m = 5
r_m = 10

#camera.orthographic = True
grass_texture = load_texture('assets/grass_block2.png')
stone_texture = load_texture('assets/stone_block2.png')
wood_texture = load_texture('assets/wood_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
log_texture = load_texture('assets/log texture.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture2.png')
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)
block_pick = 1

window.fps_counter.enabled = True
window.exit_button.visible = True

def show_popup(text):
    global popup_text
    popup_text = Text(text=text, origin=(0, 0), scale=2,color=color.black)
    popup_text.x = -popup_text.width / 2
    popup_text.y = -popup_text.height / 2
    
def hide_popup():
    global popup_text
    destroy(popup_text)

def reset_game():
    show_popup("мир переделан!!!")
    
    for block in scene.entities:
        if isinstance(block, Block):
            block.disable()  # Disable current blocks

    for x, y, z, texture in original_world:
        block = Block(position=(x, y, z), texture=texture)  # Recreate blocks

    player.position = player_starting_position  # Reset player's position
    invoke(hide_popup, delay=4)  # Hide popup after 3 seconds

def toggle_player_visibility():
    global player_enabled
    player_enabled = not player_enabled
    player.enabled = player_enabled

def update():
    global block_pick
    global p_key_held
    
    if player.y < -10:  # Check if player fell off the edge
        reset_game()

    if held_keys['r']:  # Press 'r' key to reset the game
        reset_game()

    if held_keys['p'] and not p_key_held:
        toggle_player_visibility()
        p_key_held = True
    elif not held_keys['p'] and p_key_held:
        p_key_held = False


    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']: 
        block_pick = 1
        hand.texture = grass_texture
        hand.model='assets/block'
    if held_keys['2']: 
        block_pick = 2
        hand.texture = stone_texture
        hand.model='assets/block'
    if held_keys['3']: 
        block_pick = 3
        hand.texture = brick_texture
        hand.model='assets/block'
    if held_keys['4']: 
        block_pick = 4
        hand.texture = dirt_texture
        hand.model='assets/block'
    if held_keys['5']: 
        block_pick = 5
        hand.texture = wood_texture
        hand.model='assets/block'
    if held_keys['6']: 
        block_pick = 6
        hand.texture = log_texture
        hand.model='assets/block'



class Block(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, 1),
            scale=0.5
        )
        self.default_color = self.color

    def on_mouse_enter(self):
        #print("=============hovered!")
        #print(self.position)
        #print(player.position)
        #print(math.dist(self.position, player.position))
        if math.dist(self.position, player.position) < reach_distance:
            self.color = color.color(19, 0.03, 0.7)

    def on_mouse_exit(self):
        self.color = self.default_color

    def input(self, key):
        if key == 'escape':
            application.quit()

        if self.hovered:
            if key == 'right mouse down':
                if math.dist(self.position, player.position) < reach_distance:
                    punch_sound.play()
                    if block_pick == 1: Block(position=self.position + mouse.normal, texture=grass_texture)
                    if block_pick == 2: Block(position=self.position + mouse.normal, texture=stone_texture)
                    if block_pick == 3: Block(position=self.position + mouse.normal, texture=brick_texture)
                    if block_pick == 4: Block(position=self.position + mouse.normal, texture=dirt_texture)
                    if block_pick == 5: Block(position=self.position + mouse.normal, texture=wood_texture)
                    if block_pick == 6: Block(position=self.position + mouse.normal, texture=log_texture)

            if key == 'left mouse down':
                if math.dist(self.position, player.position) < reach_distance:
                    punch_sound.play()
                    destroy(self)

    
class NonInteractiveButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_color = self.color
        self.collision = False

class TableUI(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        cell_size = 0.08  # Size of each cell
        spacing = 0.02  # Spacing between cells

        self.cells = []
        for i in range(9):

            if i <= 5:   
                cell = NonInteractiveButton(               
                parent=self,
                model='quad',
                color=color.rgba(1, 1, 1, 0.9),
                texture=["assets/grass3d.png","assets/Stone3d.png","assets/Brick3d.png","assets/Dirt3d.png","assets/plank3d.png","assets/log3d.png"][i],
                border=0.02,
                scale=(cell_size, cell_size),  # Cells are square now
                origin=(-0.5, 0),
                position=(-0.43 + i * (cell_size + spacing), -0.42)) # Adjust positions
                text_entity = Text(text=str(i + 1), position=(-0.43 + i * (cell_size + spacing), -0.382))
            else:
                cell = NonInteractiveButton(    
                parent=self,
                model='quad',
                border=0.02,
                scale=(cell_size, cell_size),  # Cells are square now
                origin=(-0.5, 0),
                position=(-0.43 + i * (cell_size + spacing), -0.42))  # Adjust positions
                text_entity = Text(text=str(i + 1), position=(-0.43 + i * (cell_size + spacing), -0.382))

            self.cells.append(cell)
            


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

for z in range(world_size):
    for x in range(world_size):
        dist_m = math.dist(Vec2(x, z), Vec2(x_m, z_m))
        if dist_m <= r_m:
            h = (math.cos(dist_m * math.pi / r_m) + 1)*h_m/2
        else:
            h = 0
        for y in range(world_depth + round(h)):
            if y == world_depth + round(h) - 1:
                block = Block(position=(x, y, z), texture=grass_texture)
                original_world.append((x, y, z, grass_texture))
            elif y == 0:
                block = Block(position=(x, y, z), texture=stone_texture)
                original_world.append((x, y, z, stone_texture))
            else:
                block = Block(position=(x, y, z), texture=dirt_texture)
                original_world.append((x, y, z, dirt_texture))
player = FirstPersonController(position=player_starting_position)
table = TableUI()
sky = Sky()
hand = Hand()
window.fullscreen = True
app.run()
