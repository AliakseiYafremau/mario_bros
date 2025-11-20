from abc import ABC, abstractmethod


class Scene(ABC):
    def set_manager(self, manager):
        self.manager = manager

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError


class SceneManager:
    def __init__(self, scenes: dict[str, Scene]):
        if not scenes:
            raise ValueError("Manager must have atleast one scene")
        self.scenes: dict[str, Scene] = {}
        for key, scene in scenes.items():
            scene.set_manager(self)
            self.scenes[key] = scene
        # select the first scene by insertion order
        self._scene = next(iter(scenes))

    def switch_to(self, scene: str) -> None:
        """Switch to a scene by name.

        Raises:
            ValueError: if scene name is unknown.
        """
        if scene not in self.scenes:
            raise ValueError("Scene does not exist")
        self._scene = scene

    def get_current_scene(self) -> Scene:
        return self.scenes[self._scene]
