from __future__ import annotations
from enum import Enum
from typing import Any
import os
from .base import *

##### 檔案輸出 #####

class HtmlDocument(SectionElement):
    _tag_symbol = "html"
    def __init__(self, indent_tab: int = 0) -> None:
        SectionElement.__init__(self, indent_tab, None)
        self._element_list: list[SectionElement] = list()
    def _generate_pattern(self):
        self.element_pattern = [
            "<!DOCTYPE html>",
            self._start_tag,
            self.container_content,
            self._end_tag
        ]
    def attach(self, element: SectionElement):
        """
        會將接受到的元素儲存於'_element_list'列表裡。
        """
        if isinstance(element, SectionElement):
            self._element_list.append(element)
        else:
            raise TypeError
    def build(self, output_directory: str, html_name: str = "default.html") -> str:
        # 檢查資料夾是否存在
        if os.path.isdir(output_directory) == False:
            raise NotADirectoryError
        full_file_path = os.path.join(output_directory, html_name)
        # 建立文本
        self._generate_pattern()
        with open(full_file_path, "w") as output_file:
            html_string = "\n".join(self.element_pattern)
            output_file.write(html_string)


##### 網頁元素 #####

class HtmlBody(SectionElement):
    _tag_symbol = "body"
    def __init__(
            self, indent_tab: int = 0, parent_container: Container | None = None) -> None:
        """
        Html的'body'元素。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。

        parent_container: 指定上級的容器元素實例，若不指定的話，則視自己為最上層容器。
        """
        SectionElement.__init__(self, indent_tab, parent_container)


class HtmlHead(SectionElement):
    _tag_symbol = "head"
    def __init__(
            self, indent_tab: int = 0, parent_container: Container | None = None) -> None:
        """
        Html的'head'元素。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。

        parent_container: 指定上級的容器元素實例，若不指定的話，則視自己為最上層容器。
        """
        SectionElement.__init__(self, indent_tab, parent_container)


class HtmlDivision(ContainerElement):
    _tag_symbol = "div"
    def __init__(
            self, id_attr: str, indent_tab: int = 0,
            parent_container: Container | None = None) -> None:
        """
        Html的'div'元素。

        id_attr: 該元素的'id'。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。

        parent_container: 指定上級的容器元素實例，若不指定的話，則視自己為最上層容器。
        """
        ContainerElement.__init__(self, id_attr, indent_tab, parent_container)


class HtmlHeading(NormalElement):
    _tag_symbol = "h"
    def __init__(self, id_attr: str, text: str = "", style_number: int = 1, indent_tab: int = 0) -> None:
        """
        Html的'h1~h6'元素。

        id_attr: 該元素的'id'。

        text: 該元素的文字內容，可以為空字串。

        style_number: 可以接受整數1~6，表示該'heading'的風格。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。
        """
        NormalElement.__init__(self, id_attr, text, indent_tab)
        self.style_number = style_number
        self._start_tag = f"<{self._tag_symbol}{str(self.style_number)} #AttrContent#>"
        self._end_tag = f"</{self._tag_symbol}{str(self.style_number)}>"

    @property
    def style_number(self):
        return self._style_number
    @style_number.setter
    def style_number(self, new_val: int):
        if isinstance(new_val, int):
            if 0 <= new_val <= 6:
                self._style_number = new_val
            else:
                raise ValueError
        else:
            TypeError


class HtmlParagraph(ContainerTextElement):
    _tag_symbol = "p"
    def __init__(
            self, id_attr: str, text: str = "",
            indent_tab: int = 0, parent_container: Container | None = None) -> None:
        """
        Html的'p'元素。

        id_attr: 該元素的'id'。

        text: 該元素的文字內容，可以為空字串。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。

        parent_container: 指定上級的容器元素實例，若不指定的話，則視自己為最上層容器。
        """
        ContainerTextElement.__init__(
            self, id_attr, text, indent_tab, parent_container)


class HtmlSpan(ModifyElement):
    _tag_symbol = "span"
    def __init__(self, id_attr: str, indent_tab: int = 0) -> None:
        """
        Html的'span'元素。

        id_attr: 該元素的'id'。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。
        """
        ModifyElement.__init__(self, id_attr, indent_tab)


class HtmlForm(ContainerElement):
    _tag_symbol = "form"
    _individual_attrs = ("action", "method")

    class Method(Enum):
        GET = "get"
        POST = "post"

    def __init__(
            self, id_attr: str, action: str = "",
            method: Method = Method.GET, indent_tab: int = 0, parent_container: Container | None = None) -> None:
        """
        Html的'form'元素。

        id_attr: 該元素的'id'。

        action: 表示該表單的資料要傳去哪裡，應給予一串網址。

        method: 表示資料的傳遞方式。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。

        parent_container: 指定上級的容器元素實例，若不指定的話，則視自己為最上層容器。

        備註：

        具有自身'獨特'的屬性。
        """
        ContainerElement.__init__(self, id_attr, indent_tab, parent_container)
        self.action = action
        self.method = method
    def set_individual_attr(self, attr_dict: dict[str, Any] = ...):
        """
        該方法提供使用者設定元素的獨特屬性，應該都從這裡進行設定。

        該方法會回傳已經設定好的屬性的物件。

        可設定之屬性：

        'action', 'method'
        """
        return ContainerElement.set_individual_attr(self, attr_dict)

    
    @property
    def action(self):
        return f'action="{self._action}"'
    @action.setter
    def action(self, new_val: str):
        if isinstance(new_val, str):
            self._action = new_val
        else:
            raise TypeError

    @property
    def method(self):
        return f'method="{self._method}"'
    @method.setter
    def method(self, new_val: Method):
        self._method = new_val.value


class HtmlInput(VoidElement):
    _tag_symbol = "input"
    _individual_attrs = ("input_type", "value")

    class InputType(Enum):
        BUTTON = "button"
        CHECKBOX = "checkbox"
        COLOR = "color"
        DATE = "date"
        DATETIME_LOCAL = "datetime-local"
        EMAIL = "email"
        FILE = "file"
        HIDDEN = "hidden"
        IMAGE = "image"
        MONTH = "month"
        NUMBER = "number"
        PASSWORD = "password"
        RADIO = "radio"
        RANGE = "range"
        RESET = "reset"
        SEARCH = "search"
        SUBMIT = "submit"
        TEL = "tel"
        TEXT = "text"
        TIME = "time"
        URL = "url"
        WEEK = "week"

    def __init__(self, id_attr: str, input_type: InputType = InputType.TEXT, indent_tab: int = 0) -> None:
        """
        Html的'input'元素。

        id_attr: 該元素的'id'。

        input_type: 指定要渲染的元素的類型。

        indent_tab: 該元素在轉換成字串時，需要縮排'多少'個tab。
        """
        VoidElement.__init__(self, id_attr, indent_tab)
        self.input_type = input_type
    def set_individual_attr(self, attr_dict: dict[str, Any] = ...):
        """
        該方法提供使用者設定元素的獨特屬性，應該都從這裡進行設定。

        該方法會回傳已經設定好的屬性的物件。

        可設定之屬性：

        'input_type', 'value'
        """
        return VoidElement.set_individual_attr(self, attr_dict)

    @property
    def input_type(self):
        return f'type="{self._input_type}"'
    @input_type.setter
    def input_type(self, new_val: InputType):
        self._input_type = new_val.value
    
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, new_val: str):
        if isinstance(new_val, str):
            self.__value = new_val
        else:
            raise TypeError
