#!/usr/bin/env python
# gesture_extensions/action_helpers.py

from typing import TYPE_CHECKING, List, Optional, Tuple, cast

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.pointer_input import PointerInput
from typing_extensions import Self

from appium.webdriver.webelement import WebElement

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver

class ActionHelpers:
    def scroll(self, origin_el: WebElement, destination_el: WebElement, duration: Optional[int] = None) -> Self:
        if duration is None:
            duration = 600

        touch_input = PointerInput(interaction.POINTER_TOUCH, 'touch')

        actions = ActionChains(cast('WebDriver', self))
        actions.w3c_actions = ActionBuilder(self, mouse=touch_input)

        actions.w3c_actions.pointer_action.move_to(origin_el)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions = ActionBuilder(self, mouse=touch_input, duration=duration)
        actions.w3c_actions.pointer_action.move_to(destination_el)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        return self

    def drag_and_drop(self, origin_el: WebElement, destination_el: WebElement, pause: Optional[float] = None) -> Self:
        actions = ActionChains(cast('WebDriver', self))
        actions.w3c_actions.pointer_action.click_and_hold(origin_el)
        if pause is not None and pause > 0:
            actions.w3c_actions.pointer_action.pause(pause)
        actions.w3c_actions.pointer_action.move_to(destination_el)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        return self

    def tap(self, positions: List[Tuple[int, int]], duration: Optional[int] = None) -> Self:
        if len(positions) == 1:
            actions = ActionChains(cast('WebDriver', self))
            actions.w3c_actions = ActionBuilder(self, mouse=PointerInput(interaction.POINTER_TOUCH, 'touch'))
            x = positions[0][0]
            y = positions[0][1]
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.pointer_down()
            if duration:
                actions.w3c_actions.pointer_action.pause(duration / 1000)
            else:
                actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
        else:
            finger = 0
            actions = ActionChains(cast('WebDriver', self))
            actions.w3c_actions.devices = []
            for position in positions:
                finger += 1
                x = position[0]
                y = position[1]
                new_input = actions.w3c_actions.add_pointer_input('touch', f'finger{finger}')
                new_input.create_pointer_move(x=x, y=y)
                new_input.create_pointer_down(button=MouseButton.LEFT)
                if duration:
                    new_input.create_pause(duration / 1000)
                else:
                    new_input.create_pause(0.1)
                new_input.create_pointer_up(MouseButton.LEFT)
            actions.perform()
        return self

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 0) -> Self:
        touch_input = PointerInput(interaction.POINTER_TOUCH, 'touch')

        actions = ActionChains(cast('WebDriver', self))
        actions.w3c_actions = ActionBuilder(self, mouse=touch_input)
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        if duration > 0:
            actions.w3c_actions = ActionBuilder(self, mouse=touch_input, duration=duration)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        return self

    def flick(self, start_x: int, start_y: int, end_x: int, end_y: int) -> Self:
        actions = ActionChains(cast('WebDriver', self))
        actions.w3c_actions = ActionBuilder(self, mouse=PointerInput(interaction.POINTER_TOUCH, 'touch'))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        return self
