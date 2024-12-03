from __future__ import annotations
from typing import Optional, List, Dict, Any
from copy import deepcopy
from flet import Page, View


class Renderer:
    def __init__(self: Renderer):
        self._routes: List[str] = []
        self._master_pages: List[Optional[View]] = []
        self._flet_pages: List[Page] = []

    def find_element(self: Renderer, element: Any, key: str) -> Any:
        if "key" in dir(element) and element.key == key:
            return element
        for child in element._get_children():
            returned_element = self.find_element(child, key)
            if returned_element is not None:
                return returned_element
        return None

    def update_attributes(
        self: Renderer,
        route: str,
        key: str,
        attributes: Dict[str, Any],
    ) -> None:
        if route not in self._routes:
            return
        for flet_page in self._flet_pages:
            element = self.find_element(flet_page, key)
            if element is None:
                break
            print(f"Found element to update: {element}.")
            for attr_name, value in attributes.items():
                setattr(element, attr_name, value)
            element.update()

    def update(self: Renderer) -> None:
        for flet_page in self._flet_pages:
            flet_page.update()

    def show(self: Renderer, page: View) -> None:
        if page.route in self._routes and page.route != self._routes[-1]:
            index = self._routes.index(page.route)
            # Move route
            route = self._routes.pop(index)
            self._routes.append(route)
            # Move root page
            _master_page = self._master_pages.pop(index)
            self._master_pages.append(_master_page)
            # Move shown pages
            for flet_page in self._flet_pages:
                _ = flet_page.views.pop(index)
                _page = deepcopy(_master_page)
                flet_page.views.append(_page)
        elif page.route not in self._routes:
            self._routes.append(page.route)
            self._master_pages.append(page)
            for flet_page in self._flet_pages:
                _page = deepcopy(page)
                flet_page.views.append(_page)
                print(f"View {id(_page)} added.")
            print(f"Page added to renderer: {page.route}.")
        else:
            print(f"Page already exists: {page.route}.")
            pass
        self.update()

    def close(self: Renderer) -> None:
        del self._routes[-1]
        del self._master_pages[-1]
        for flet_page in self._flet_pages:
            del flet_page.views[-1]
        print(f"Removed last page from renderer.")
        self.update()

    def go_to(self: Renderer, route: str) -> None:
        if route not in self._routes:
            return
        index = self._routes.index(route)
        # Move route
        route = self._routes.pop(index)
        self._routes.append(route)
        # Move root page
        _master_page = self._master_pages.pop(index)
        self._master_pages.append(_master_page)
        # Move shown pages
        for flet_page in self._flet_pages:
            _ = flet_page.views.pop(index)
            _page = deepcopy(_master_page)
            flet_page.views.append(_page)
        print(f"Routed to page: {route}.")
        self.update()

    def go_back(self: Renderer, level: int = -1) -> None:
        # Move route
        route = self._routes.pop(level - 1)
        self._routes.append(route)
        # Move root page
        _master_page = self._master_pages.pop(level - 1)
        self._master_pages.append(_master_page)
        # Move shown pages
        for flet_page in self._flet_pages:
            _ = flet_page.views.pop(level - 1)
            _page = deepcopy(_master_page)
            flet_page.views.append(_page)
        print(f"Routed back to page: {route}.")
        self.update()

    def register(self: Renderer, flet_page: Page) -> None:
        root_page = flet_page.views[0]
        if root_page.route not in self._routes:
            self._routes.append(root_page.route)
            self._master_pages.append(None)
        for master_page in self._master_pages:
            if master_page is None:
                continue
            _page = deepcopy(master_page)
            flet_page.views.append(_page)
            print(f"View {id(_page)} added.")
        self._flet_pages.append(flet_page)
        print(f"Number of flet pages in registry: {len(self._flet_pages)}")
        flet_page.update()

    def deregister(self: Renderer, flet_page: Page) -> None:
        if flet_page in self._flet_pages:
            self._flet_pages.remove(flet_page)
        print(f"Number of flet pages in registry: {len(self._flet_pages)}")


global_renderer: Renderer = Renderer()
