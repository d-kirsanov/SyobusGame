from first_person_controller import FirstPersonController
from ursina import *
import math

from block import Block

class World:

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

    def __init__(self):
        self.grass_texture = load_texture('assets/grass_block2.png')
        self.stone_texture = load_texture('assets/stone_block2.png')
        self.wood_texture = load_texture('assets/wood_block.png')
        self.brick_texture = load_texture('assets/brick_block.png')
        self.dirt_texture = load_texture('assets/dirt_block.png')
        self.log_texture = load_texture('assets/log texture.png')
        self.teleporter_texture = load_texture('assets/teleporter texture.png')
        self.sky_texture = load_texture('assets/skybox.png')
        self.arm_texture = load_texture('assets/arm_texture2.png')
        self.punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)

        self.player = FirstPersonController(position=self.player_starting_position)

        self.hand = Hand(self)

        self.build_original()

    block_pick = 1

    def show_popup(self, text):
        self.popup_text = Text(text=text, origin=(0, 0), scale=2,color=color.black)
        self.popup_text.x = -self.popup_text.width / 2
        self.popup_text.y = -self.popup_text.height / 2
        
    def hide_popup(self):
        destroy(self.popup_text)

    def reset_game(self):
        self.show_popup("мир переделан!!!")
        
        for block in scene.entities:
            if isinstance(block, Block):
                block.disable()  # Disable current blocks

        for x, y, z, type in self.original_world:
            block = Block(self, position=(x, y, z), type=type)  # Recreate blocks

        self.player.position = self.player_starting_position  # Reset player's position
        invoke(self.hide_popup, delay=4)  # Hide popup after 3 seconds

    def toggle_player_visibility(self):
        self.player_enabled = not self.player_enabled
        self.player.enabled = self.player_enabled


    def hand_update(self, pick, texture, model='assets/block', position=Vec2(0.4, -0.6), rotation=Vec3(150, -10, 0)):
        self.block_pick = pick
        self.hand.texture = texture
        self.hand.model=model
        self.hand.position = position
        self.hand.rotation = rotation

    def create_block(self, position):
        if math.dist(position, self.player.position) < self.reach_distance:
            self.punch_sound.play()
            if self.block_pick == 1: Block(self, position=position + mouse.normal, type="grass")
            if self.block_pick == 2: Block(self, position=position + mouse.normal, type="stone")
            if self.block_pick == 3: Block(self, position=position + mouse.normal, type="brick")
            if self.block_pick == 4: Block(self, position=position + mouse.normal, type="dirt")
            if self.block_pick == 5: Block(self, position=position + mouse.normal, type="wood")
            if self.block_pick == 6: Block(self, position=position + mouse.normal, type="log")
            if self.block_pick == 7: Block(self, position=position + mouse.normal, type="teleporter")

    def delete_block(self, block):
        if math.dist(block.position, self.player.position) < self.reach_distance:
            self.punch_sound.play()
            destroy(block)

    def highlight_block(self, block):
        if math.dist(block.position, self.player.position) < self.reach_distance:
            block.color = color.color(19, 0.03, 0.7)

    def build_original(self):
        for z in range(self.world_size):
            for x in range(self.world_size):
                dist_mountain = math.dist(Vec2(x, z), Vec2(self.x_m, self.z_m))
                if dist_mountain <= self.r_m:
                    h = (math.cos(dist_mountain * math.pi / self.r_m) + 1)*self.h_m/2
                else:
                    h = 0
                for y in range(self.world_depth + round(h)):
                    if y == self.world_depth + round(h) - 1:
                        block = Block(self, position=(x, y, z), type="grass")
                        self.original_world.append((x, y, z, "grass"))
                    elif y == 0:
                        block = Block(self, position=(x, y, z), type="stone")
                        self.original_world.append((x, y, z, "stone"))
                    else:
                        block = Block(self, position=(x, y, z), type="dirt")
                        self.original_world.append((x, y, z, "dirt"))


    def update(self):
        if self.player.y < -10:  # Check if player fell off the edgehufyrvguyrfgveewwwwwwryewuwgvuuuuuuuueyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
            self.player.position=self.player_starting_position

        if held_keys['p'] and not self.p_key_held:
            self.toggle_player_visibility()
            self.p_key_held = True
        elif not held_keys['p'] and self.p_key_held:
            self.p_key_held = False

        if held_keys['left mouse'] or held_keys['right mouse']:
            self.hand.active()
        else:
            self.hand.passive()

        if held_keys['1']: 
            self.hand_update(1, self.grass_texture)
        if held_keys['2']: 
            self.hand_update(2, self.stone_texture)
        if held_keys['3']: 
            self.hand_update(3, self.brick_texture)
        if held_keys['4']: 
            self.hand_update(4, self.dirt_texture)
        if held_keys['5']: 
            self.hand_update(5, self.wood_texture)
        if held_keys['6']: 
            self.hand_update(6, self.log_texture)
        if held_keys['7']:
            self.hand_update(7, self.teleporter_texture, model='assets/teleporter', position=Vec2(0.4, -0.3), rotation=Vec3(290, -10, 0))

    
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

            if i <= 6:   
                cell = NonInteractiveButton(               
                parent=self,
                model='quad',
                color=color.rgba(1, 1, 1, 0.9),
                texture=["assets/grass3d.png","assets/Stone3d.png","assets/Brick3d.png","assets/Dirt3d.png","assets/plank3d.png","assets/log3d.png","assets/teleporter3D.png"][i],
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
    def __init__(self, world):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=world.sky_texture,
            scale=150,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self, world):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=world.arm_texture,
            double_sided=True,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

app = Ursina()
window.fps_counter.enabled = True
window.exit_button.visible = True
window.fullscreen = True
world = World()
def update():
    world.update()
table = TableUI()
sky = Sky(world)
app.run()
