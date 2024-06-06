from ._module_unit import *

##### 已組合元件 #####

class BaseElement(IBaseElement, Tag):
    """
    IBaseElement抽象類別的實作類別。

    繼承自'IBaseElement'、'Tag'。

    -------------------------------

    IBaseElement ---> 規範網頁元素的基本建構行為。

    Tag ---> 使該類別具有'tag'可以使用。
    """
    def __init__(self, indent_tab: int = 0, has_attrs: bool = True) -> None:
        """
        實作繼承的類別的初始化方法。
        """
        Tag.__init__(self, has_attrs)
        self.indent_tab = indent_tab
    def _generate_attr_string(self):
        """
        由於此類別並未繼承'HtmlGlobalAttr'或'IndividualAttr'類別，故該方法僅設置'all_attr_string'為空字串。
        """
        self.all_attr_string = ""
    def _generate_pattern(self):
        """
        由於此類別並未繼承'HtmlGlobalAttr'或'IndividualAttr'類別，故該方法僅設置'element_pattern'為最簡單的格式。

        若輸出為字串的話，應該如下：

        <tag></tag>
        """
        self.element_pattern = [
            "\t"*self.indent_tab,
            self._start_tag,
            self._end_tag
        ]
    def build(self) -> str:
        """
        該方法為產生完整的網頁元素。
        """
        if hasattr(self, "all_attr_string") == False:
            self._generate_attr_string()
        if hasattr(self, "element_pattern") == False:
            self._generate_pattern()
        return "".join(self.element_pattern)
    
    @property
    def all_attr_string(self) -> str:
        return self.__all_attr_string
    @all_attr_string.setter
    def all_attr_string(self, new_val: str):
        if isinstance(new_val, str):
            self.__all_attr_string = new_val
        else:
            raise TypeError

    @property
    def element_pattern(self) -> list[str]:
        return self.__element_pattern
    @element_pattern.setter
    def element_pattern(self, new_val: list[str]):
        if isinstance(new_val, list):
            self.__element_pattern = new_val
        else:
            raise TypeError

    @property
    def indent_tab(self) -> int:
        return self.__indent_tab
    @indent_tab.setter
    def indent_tab(self, new_val: int):
        if isinstance(new_val, int):
            self.__indent_tab = new_val
        else:
            raise TypeError


class NormalElement(BaseElement, HtmlGlobalAttr, IndividualAttr, HtmlText):
    """
    BaseElement類別子類，大部分的網頁元素可以繼承此類。

    繼承自'BaseElement'、'HtmlGlobalAttr'、'IndividualAttr'、'HtmlText'。

    -------------------------------

    BaseElement ---> 已實作網頁元素的基本建構行為。

    HtmlGlobalAttr ---> 使該類別具有網頁元素'全域'屬性可以設置。

    IndividualAttr ---> 使該類別具有網頁元素'獨特'屬性可以設置。

    HtmlText ---> 使該類別具有'文字內容'可以設置且該文字內容可以被'TextModifier'修飾。
    """
    def __init__(self, id_attr: str, text: str = "", indent_tab: int = 0, has_attrs: bool = True) -> None:
        HtmlGlobalAttr.__init__(self, id_attr)
        BaseElement.__init__(self, indent_tab, has_attrs)
        HtmlText.__init__(self, text)
    def _generate_attr_string(self):
        """
        該方法會將對應之'全域'、'獨特'屬性轉化成字串並存於'self.__all_attr_string'。
        """
        global_attr_string = self.generate_global_attr_string()
        individual_attr_string = self.generate_individual_attr_string()
        if individual_attr_string == "":
            self.all_attr_string = global_attr_string
        else:
            self.all_attr_string = individual_attr_string + " " + global_attr_string
    def _generate_pattern(self):
        """
        該方法設置'element_pattern'為大部分網頁元素適用的格式。

        若輸出為字串的話，應該如下：

        <tag attr1=val1 attr2=val2 ...>self.text</tag>
        """
        self.element_pattern = [
            "\t"*self.indent_tab,
            self._start_tag.replace("#AttrContent#", self.all_attr_string),
            self.text,
            self._end_tag
        ]


class ModifyElement(BaseElement, HtmlGlobalAttr, IndividualAttr, TextModifier):
    """
    BaseElement類別子類，大部分的網頁元素可以繼承此類。

    繼承自'BaseElement'、'HtmlGlobalAttr'、'IndividualAttr'、'TextModifier'。

    -------------------------------

    BaseElement ---> 已實作網頁元素的基本建構行為。

    HtmlGlobalAttr ---> 使該類別具有網頁元素'全域'屬性可以設置。

    IndividualAttr ---> 使該類別具有網頁元素'獨特'屬性可以設置。

    TextModifier ---> 使該類別具有'文字內容'可以設置且該文字內容可以被'TextModifier'修飾。

    備註：

    雖然部分網頁標籤(span ...)也可以具有文字內容，但是其本質是修飾文字內容，故僅將其當做'修飾用'網頁元素。

    雖然無法設置其文字內容，但取而代之的是可以對繼承'HtmlText'類別的網頁元素類別的文字內容作修飾。
    """
    def __init__(self, id_attr: str, indent_tab: int = 0) -> None:
        HtmlGlobalAttr.__init__(self, id_attr)
        BaseElement.__init__(self, indent_tab, True)
    def _generate_attr_string(self):
        """
        該方法會將對應之'全域'、'獨特'屬性轉化成字串並存於'self.__all_attr_string'。
        """
        global_attr_string = self.generate_global_attr_string()
        individual_attr_string = self.generate_individual_attr_string()
        if individual_attr_string == "":
            self.all_attr_string = global_attr_string
        else:
            self.all_attr_string = individual_attr_string + " " + global_attr_string
    def _generate_pattern(self):
        """
        該方法設置'element_pattern'為少部分網頁元素適用的格式。

        若輸出為字串的話，應該如下：

        <tag attr1=val1 attr2=val2 ...></tag>
        """
        self.element_pattern = [
            "\t"*self.indent_tab,
            self._start_tag.replace("#AttrContent#", self.all_attr_string),
            self._end_tag
        ]
    def generate_modify_string(self, text: str) -> str:
        self._generate_attr_string()
        modify_pattern = [
            self._start_tag.replace("#AttrContent#", self.all_attr_string),
            text,
            self._end_tag
        ]
        return "".join(modify_pattern)


class VoidElement(BaseElement, HtmlGlobalAttr, IndividualAttr):
    """
    BaseElement類別子類，該類別的特點為不具備結束標籤，也因為其不具備結束標籤，故不會有文字內容。

    繼承自'BaseElement'、'HtmlGlobalAttr'、'IndividualAttr'。

    -------------------------------

    BaseElement ---> 已實作網頁元素的基本建構行為。

    HtmlGlobalAttr ---> 使該類別具有網頁元素'全域'屬性可以設置。

    IndividualAttr ---> 使該類別具有網頁元素'獨特'屬性可以設置。
    """
    def __init__(self, id_attr: str, indent_tab: int = 0, has_attrs: bool = True) -> None:
        HtmlGlobalAttr.__init__(self, id_attr)
        BaseElement.__init__(self, indent_tab, has_attrs)
    def _generate_attr_string(self):
        """
        該方法會將對應之'全域'、'獨特'屬性轉化成字串並存於'self.__all_attr_string'。
        """
        global_attr_string = self.generate_global_attr_string()
        individual_attr_string = self.generate_individual_attr_string()
        if individual_attr_string == "":
            self.all_attr_string = global_attr_string
        else:
            self.all_attr_string = individual_attr_string + " " + global_attr_string
    def _generate_pattern(self):
        """
        該方法設置'element_pattern'為少部分網頁元素適用的格式。

        若輸出為字串的話，應該如下：

        <tag attr1=val1 attr2=val2 ...>
        """
        self.element_pattern = [
            "\t"*self.indent_tab,
            self._start_tag.replace("#AttrContent#", self.all_attr_string)
        ]


class SectionElement(BaseElement, Container):
    """
    BaseElement類別子類，該類別僅適用於'html'、'head'、'body'。

    繼承自'BaseElement'、'Container'。

    -------------------------------

    BaseElement ---> 已實作網頁元素的基本建構行為。

    Container ---> 使該類別可以包含其他類別。
    """
    def __init__(
            self, indent_tab: int = 0, 
            parent_container: Container | None = None) -> None:
        BaseElement.__init__(self, indent_tab, False)
        Container.__init__(self, parent_container)
    def _generate_pattern(self):
        """
        該方法設置'element_pattern'為'head'、'body'網頁元素適用的格式。

        若輸出為字串的話，應該如下：

        <tag></tag>

        or

        <tag>
        
            content
        
        </tag>
        """
        if self.container_content == "":
            self.element_pattern = [
                "\t"*self.indent_tab + self._start_tag + self._end_tag
            ]
        else:
            self.element_pattern = [
                "\t"*self.indent_tab + self._start_tag,
                self.container_content,
                "\t"*self.indent_tab + self._end_tag
            ]
    def build(self) -> str:
        self._generate_pattern()
        return "\n".join(self.element_pattern)


class ContainerElement(BaseElement, Container, HtmlGlobalAttr, IndividualAttr):
    """
    BaseElement類別子類，容器類型的網頁元素(div...)可以繼承此類。

    繼承自'BaseElement'、'Container'、'HtmlGlobalAttr'、'IndividualAttr'。

    -------------------------------

    BaseElement ---> 已實作網頁元素的基本建構行為。

    Container ---> 使該類別可以包含其他類別。

    HtmlGlobalAttr ---> 使該類別具有網頁元素'全域'屬性可以設置。

    IndividualAttr ---> 使該類別具有網頁元素'獨特'屬性可以設置。
    """
    def __init__(
            self, id_attr: str, indent_tab: int = 0, 
            parent_container: Container | None = None) -> None:
        BaseElement.__init__(self, indent_tab, True)
        Container.__init__(self, parent_container)
        HtmlGlobalAttr.__init__(self, id_attr)
        # 以下的陳述式是微調縮排：
        self._adjust_tab += self.indent_tab
    def _generate_attr_string(self):
        """
        該方法會將對應之'全域'、'獨特'屬性轉化成字串並存於'self.__all_attr_string'。
        """
        global_attr_string = self.generate_global_attr_string()
        individual_attr_string = self.generate_individual_attr_string()
        if individual_attr_string == "":
            self.all_attr_string = global_attr_string
        else:
            self.all_attr_string = individual_attr_string + " " + global_attr_string
    def _generate_pattern(self):
        """
        該方法設置'element_pattern'為容器類型的網頁元素適用的格式。

        若輸出為字串的話，應該如下：

        <tag attr1=val1 attr2=val2 ...>
        
            content
        
        </tag>
        """
        self.element_pattern = [
            "\t"*self.indent_tab + self._start_tag.replace("#AttrContent#", self.all_attr_string),
            self.container_content,
            "\t"*self.indent_tab + self._end_tag
        ]
    def build(self) -> str:
        self._generate_attr_string()
        self._generate_pattern()
        return "\n".join(self.element_pattern)


class ContainerTextElement(BaseElement, Container, HtmlGlobalAttr, IndividualAttr, HtmlText):
    """
    BaseElement類別子類，目前專為'paragraph'開設的類別，未來可能會做調整。

    繼承自'BaseElement'、'Container'、'HtmlGlobalAttr'、'IndividualAttr'、'HtmlText'。

    -------------------------------

    BaseElement ---> 已實作網頁元素的基本建構行為。

    Container ---> 使該類別可以包含其他類別。

    HtmlGlobalAttr ---> 使該類別具有網頁元素'全域'屬性可以設置。

    IndividualAttr ---> 使該類別具有網頁元素'獨特'屬性可以設置。

    HtmlText ---> 使該類別具有'文字內容'可以設置且該文字內容可以被'TextModifier'修飾。
    """
    def __init__(
            self, id_attr: str, text: str = "",
            indent_tab: int = 0, parent_container: Container | None = None) -> None:
        HtmlGlobalAttr.__init__(self, id_attr)
        BaseElement.__init__(self, indent_tab, True)
        Container.__init__(self, parent_container)
        HtmlText.__init__(self, text)
        # 以下的陳述式是微調縮排：
        self._adjust_tab += self.indent_tab
    def _generate_attr_string(self):
        """
        該方法會將對應之'全域'、'獨特'屬性轉化成字串並存於'self.__all_attr_string'。
        """
        global_attr_string = self.generate_global_attr_string()
        individual_attr_string = self.generate_individual_attr_string()
        if individual_attr_string == "":
            self.all_attr_string = global_attr_string
        else:
            self.all_attr_string = individual_attr_string + " " + global_attr_string
    def _generate_pattern(self):
        """
        該方法設置'element_pattern'為容器類型的網頁元素適用的格式。

        若輸出為字串的話，應該如下：

        <tag attr1=val1 attr2=val2 ...>
        
            content
        
        </tag>
        """
        if hasattr(self, "container_content") == False:
            self.element_pattern = [
                "\t"*self.indent_tab + self._start_tag.replace("#AttrContent#", self.all_attr_string),
                self.text,
                self._end_tag
            ]
        else:
            self.element_pattern = [
                "\t"*self.indent_tab + self._start_tag.replace("#AttrContent#", self.all_attr_string),
                self.container_content,
                "\t"*self.indent_tab + self._end_tag
            ]
    def build(self) -> str:
        self._generate_attr_string()
        self._generate_pattern()
        if hasattr(self, "container_content") == False:
            return "".join(self.element_pattern)
        else:
            return "\n".join(self.element_pattern)