from ursina import *

class Block(Button):

    def __init__(self, world, position=(0, 0, 0), type="grass"):

        self.world = world

        model='assets/block'
        match type:
            case "grass":
                texture=self.world.grass_texture
            case "stone":
                texture=self.world.stone_texture
            case "wood":
                texture=self.world.wood_texture
            case "brick":
                texture=self.world.brick_texture
            case "dirt":
                texture=self.world.dirt_texture
            case "log":
                texture=self.world.log_texture
            case "teleporter":
                texture=self.world.teleporter_texture
                model='assets/teleporter'
                # we add a little y shift so that teleporter renders correctly on top of another block
                position += Vec3(0, 0.001, 0)

        super().__init__(
            parent=scene,
            position=position,
            model=model,
            double_sided=True,
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, 1),
            scale=0.5
        )
        self.default_color = self.color

    def on_mouse_enter(self):
        self.world.highlight_block(self)

    def on_mouse_exit(self):
        self.color = self.default_color

    def input(self, key):
        if key == 'escape':
            application.quit()

        if self.hovered:
            if key == 'right mouse down':
                self.world.create_block(self.position)
                    
            if key == 'left mouse down':
                self.world.delete_block(self)
