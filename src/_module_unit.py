from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


##### 基本元件 #####

class HtmlGlobalAttr:
    """
    包含Html所擁有的全域屬性及其設置的條件。
    
    大部分的Html元素都該繼承此類別。
    """
    _global_attrs = (
        "accesskey", "class_attr", "contenteditable", "data", "dir_attr",
        "draggable", "enterkeyhint", "hidden", "id_attr", "inert",
        "inputmode", "lang", "popover", "spellcheck", "style",
        "tabindex", "title"
    )
    class Dir(Enum):
        """
        Html的'Dir'屬性。決定元素所包含的文字顯示方向。
        
        可以使用的值為：LTR, RTL, AUTO
        """
        LTR = "ltr"
        RTL = "rtl"
        AUTO = "auto"
    class Draggable(Enum):
        """
        Html的'Draggable'屬性。決定元素是否可以被拖曳。
        
        可以使用的值為：TRUE, FALSE, AUTO
        """
        TRUE = "true"
        FALSE = "false"
        AUTO = "auto"
    class Enterkeyhint(Enum):
        """
        Html的'Enterkeyhint'屬性。設置'Enter'鍵的效果。
        
        可以使用的值為：DONE, ENTER, GO, NEXT, PREVIOUS, SEARCH, SEND
        """
        DONE = "done"
        ENTER = "enter"
        GO = "go"
        NEXT = "next"
        PREVIOUS = "previous"
        SEARCH = "search"
        SEND = "send"
    class Inputmode(Enum):
        """
        Html的'Inputmode'屬性。提供使用者在編輯該元素或其內容時，對該元素的輸入資料的資料類型的提示。
        
        可以使用的值為：DECIMAL, EMAIL, NONE, NUMERIC, SEARCH, TEL, TEXT, URL
        """
        DECIMAL = "decimal"
        EMAIL = "email"
        NONE = "none"
        NUMERIC = "numeric"
        SEARCH = "search"
        TEL = "tel"
        TEXT = "text"
        URL = "url"
    class Lang(Enum):
        """
        Html的'Inputmode'屬性。該元素應顯示為何種語言。
        """
        EN = "en"
        ZH = "zh"
    def __init__(self, id_attr: str):
        """
        HtmlGlobalAttr的初始化方法，為區分繼承該類別的每個元素，故必須設置其'id'屬性。

        補充：

        因為'id'屬性是不可以'重複'的。
        """
        self.id_attr = id_attr
    def set_global_attr(self, attr_dict: dict[str, Any] = dict()):
        """
        該方法提供使用者設定元素的全域屬性，應該都從這裡進行設定。

        該方法會回傳已經設定好的屬性的物件。

        可設定之屬性：

        'accesskey', 'class_attr', 'contenteditable', 'data', 'dir_attr',
        
        'draggable', 'enterkeyhint', 'hidden', 'id_attr', 'inert',
        
        'inputmode', 'lang', 'popover', 'spellcheck', 'style',
        
        'tabindex', 'title'
        """
        error_messenge = f"您提供的屬性名稱#AttributeName#並不在屬性列表裡。請確認符合其中的名稱：\n{self._global_attrs}"
        for html_attr, new_val in attr_dict.items():
            if html_attr not in self._global_attrs:
                raise AttributeError(error_messenge.replace("#AttributeName#", html_attr))
            setattr(self, html_attr, new_val)
        return self
    def generate_global_attr_string(self) -> str:
        """
        該方法會將已設置好的'全域'屬性轉化為一串彼此以空格相連的字串形式。

        每種'全域'屬性都是透過'getter'來獲得對應的屬性字串格式。

        回傳字串格式:

        attr1=value attr2=value ...
        """
        exist_attr_list = list()
        for attr_name in self._global_attrs:
            val = getattr(self, attr_name, None)
            if val != None:
                exist_attr_list.append(val)
        return " ".join(exist_attr_list)

    @property
    def accesskey(self):
        return f'accesskey="{self.__accesskey}"'
    @accesskey.setter
    def accesskey(self, new_val: str):
        if isinstance(new_val, str):
            if len(new_val) == 1:
                self.__accesskey = new_val
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def class_attr(self):
        return f'class="{self.__class_attr}"'
    @class_attr.setter
    def class_attr(self, new_val: str):
        if isinstance(new_val, str):
            self.__class_attr = new_val
        else:
            raise TypeError
        
    @property
    def contenteditable(self):
        return f'contenteditable="{str(self.__contenteditable).lower()}"'
    @contenteditable.setter
    def contenteditable(self, new_val: bool):
        if isinstance(new_val, bool):
            self.__contenteditable = new_val
        else:
            raise TypeError
        
    @property
    def data(self):
        return f'data-{self.__data[0]}="{self.__data[1]}"'
    @data.setter
    def data(self, new_val: tuple[str, str]):
        if (isinstance(new_val[0], str) and
            isinstance(new_val[1], str)):
            self.__data = new_val
        else:
            raise TypeError
        
    @property
    def dir_attr(self):
        return f'dir="{self.__dir_attr}"'
    @dir_attr.setter
    def dir_attr(self, new_val: Dir):
        self.__dir_attr = new_val.value
            
    @property
    def draggable(self):
        return f'draggable="{self.__draggable}"'
    @draggable.setter
    def draggable(self, new_val: Draggable):
        self.__draggable = new_val.value

    @property
    def enterkeyhint(self):
        return f'enterkeyhint="{self.__enterkeyhint}"'
    @enterkeyhint.setter
    def enterkeyhint(self, new_val: Enterkeyhint):
        self.__enterkeyhint = new_val.value
    
    @property
    def hidden(self):
        return self.__hidden
    @hidden.setter
    def hidden(self, new_val: bool):
        if isinstance(new_val, bool):
            if new_val == True:
                self.__hidden = "hidden"
            else:
                self.__hidden = None
        else:
            raise TypeError
    
    @property
    def id_attr(self):
        return f'id="{self.__id}"'
    @id_attr.setter
    def id_attr(self, new_val: str):
        if isinstance(new_val, str):
            self.__id = new_val
        else:
            raise TypeError

    @property
    def inert(self):
        return self.__inert
    @inert.setter
    def inert(self, new_val: bool):
        if isinstance(new_val, bool):
            if new_val == True:
                self.__inert = "inert"
            else:
                self.__inert = None
        else:
            raise TypeError

    @property
    def inputmode(self):
        return f'inputmode="{self.__inputmode}"'
    @inputmode.setter
    def inputmode(self, new_val: Inputmode):
        self.__inputmode = new_val.value
    
    @property
    def lang(self):
        return f'lang="{self.__lang}"'
    @lang.setter
    def lang(self, new_val: Lang):
        self.__lang = new_val.value

    @property
    def popover(self):
        return self.__popover
    @popover.setter
    def popover(self, new_val: bool):
        if isinstance(new_val, bool):
            if new_val == True:
                self.__popover = "popover"
            else:
                self.__popover = None
        else:
            raise TypeError

    @property
    def spellcheck(self):
        return f'spellcheck="{str(self.__spellcheck).lower()}"'
    @spellcheck.setter
    def spellcheck(self, new_val: bool):
        if isinstance(new_val, bool):
            self.__spellcheck = new_val
        else:
            raise TypeError

    @property
    def style(self):
        return f'style="{self.__style}"'
    @style.setter
    def style(self, new_val: str):
        if isinstance(new_val, str):
            self.__style = new_val
        else:
            raise TypeError

    @property
    def tabindex(self):
        return f'tabindex="{str(self.__tabindex)}"'
    @tabindex.setter
    def tabindex(self, new_val: int):
        if isinstance(new_val, int):
            self.__tabindex = new_val
        else:
            raise TypeError

    @property
    def title(self):
        return f'title="{self.__title}"'
    @title.setter
    def title(self, new_val: str):
        if isinstance(new_val, str):
            self.__title = new_val
        else:
            TypeError


class IndividualAttr:
    """
    部分的Html元素會具備自己獨有的屬性。
    
    如果繼承該類別，則需要注意將'特有屬性'設置於'_individual_attrs'數組裡並設置對應的'@property'。

    該類別不與'HtmlGlobalAttr'類別衝突。

    備註：

    設置於'_individual_attrs'裡的字串必須符合變數的命名方式。(如不能有空白鍵、不能以數字做為開頭...)，
    """
    _individual_attrs: tuple[str] = ()
    def set_individual_attr(self, attr_dict: dict[str, Any] = dict()):
        """
        該方法提供使用者設定元素的獨特屬性，應該都從這裡進行設定。

        該方法會回傳已經設定好的屬性的物件。

        可設定之屬性：

        未定義
        """
        error_messenge = f"您提供的屬性名稱#AttributeName#並不在屬性列表裡。請確認符合其中的名稱：\n{self._individual_attrs}"
        for html_attr, new_val in attr_dict.items():
            if html_attr not in self._individual_attrs:
                raise AttributeError(error_messenge.replace("#AttributeName#", html_attr))
            setattr(self, html_attr, new_val)
        return self
    def generate_individual_attr_string(self):
        """
        該方法會將已設置好的'獨特'屬性'轉化為一串彼此以空格相連的字串形式。

        每種'獨特'屬性都是透過'getter'來獲得對應的屬性字串格式。

        回傳字串格式:

        attr1=value attr2=value ...
        """
        exist_attr_list = list()
        for attr_name in self._individual_attrs:
            val = getattr(self, attr_name, None)
            if val != None:
                exist_attr_list.append(val)
        return " ".join(exist_attr_list)


class IBaseElement(ABC):
    """
    該模組最底層的抽象類別，所有的網頁元素類別都該繼承此抽象類別或此抽象類別的子類。

    需要額外實作'all_attr_string'、'element_pattern'、'indent_tab'屬性。
    """
    @abstractmethod
    def __init__(self, indent_tab: int = 0) -> None:
        """
        未實作。'indent_tab'規定網頁元素在縮排時，需要多少的'tab'。
        """
        raise NotImplementedError
    @abstractmethod
    def _generate_attr_string(self):
        """
        未實作。該方法只能用於產生網頁元素所需要的屬性字串，而該字串需要儲存在'self.__all_attr_string'，由'self.all_attr_string'呼叫。
        """
        raise NotImplementedError
    @abstractmethod
    def _generate_pattern(self):
        """
        未實作。該方法規範網頁元素要如何排版，而排版的格式需要儲存在'self.__element_pattern'，由'self.element_pattern'呼叫。
        """
        raise NotImplementedError
    @abstractmethod
    def build(self):
        """
        未實作。該方法規範如何產生完整的網頁元素字串。
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def all_attr_string(self) -> str: ...
    @all_attr_string.setter
    @abstractmethod
    def all_attr_string(self, new_val: str): ...

    @property
    @abstractmethod
    def element_pattern(self) -> list[str]: ...
    @element_pattern.setter
    @abstractmethod
    def element_pattern(self, new_val: list[str]): ...

    @property
    @abstractmethod
    def indent_tab(self) -> int: ...
    @indent_tab.setter
    @abstractmethod
    def indent_tab(self, new_val: int): ...


class Tag:
    """
    建立元素所對應之標籤。
    
    欲設定標籤之文字，請變更'_tag_symbol'的值。
    """
    _tag_symbol = ""
    def __init__(self, has_attrs: bool = True) -> None:
        """
        可以透過參數'has_attrs'來產生是否具有可以填入屬性的標籤。

        例如'body'元素不具有任何屬性
        """
        if has_attrs == True:
            self._start_tag = f"<{self._tag_symbol} #AttrContent#>"
            self._end_tag = f"</{self._tag_symbol}>"
        else:
            self._start_tag = f"<{self._tag_symbol}>"
            self._end_tag = f"</{self._tag_symbol}>"


class Container:
    """
    該類別用於可以接收其他元素的元素，例如'Form'、'div'...。

    該類別也新增對於其他繼承該類別的上下級設定。

    實例化該類別的方式必須使用'with class as varible: ...'
    """
    def __init__(self, parent_container: Container | None) -> None:
        """
        在建構此類別的實例時，需確認其是否具有上級'Container'。

        如果有其上級的話，需給予參數'parent_container'所需的'Container'實例。

        example:

        這裡以'class HtmlDivision(Container)'為例

        最上級 ---> with HtmlDivision() as div1:

                        code ...
        
        第一級 --->     with HtmlDivision(parent_container=div1) as div2:
            
                            code ...
        """
        self._element_list: list[IBaseElement] = list()
        self._parent_container = parent_container
        # '_adjust_tab'用於調整當其他元素儲存於該'Container'時，應該縮排多少個'tab'。
        self._adjust_tab: int = 1
        self.container_content: str
    def attach(self, element: IBaseElement):
        """會將接受到的元素儲存於'_element_list'列表裡。"""
        if isinstance(element, IBaseElement):
            self._element_list.append(element)
        else:
            raise TypeError
    def _encapsulate(self):
        """
        將所儲存的'所有'元素轉換成字串並串聯在一起的方法。
        
        主要透過'IBaseElement.build()'達成每個元素的字串轉換。

        該方法應只能在退出'with class as varible: ...'時使用。
        """
        container_content_list = list()
        for element in self._element_list:
            element.indent_tab += self._adjust_tab
            container_content_list.append(element.build())
        self.container_content = "\n".join(container_content_list)
    def __enter__(self):
        """用於該語法'with class as varible: ...'並建立'Container'的上下級關係"""
        if self._parent_container != None:
            if isinstance(self._parent_container, Container):
                self._parent_container._element_list.append(self)
                self._adjust_tab = self._adjust_tab + self._parent_container._adjust_tab
                return self
            else:
                raise TypeError
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._encapsulate()


class TextModifier:
    """
    和'HtmlText'類別相對應的類別，用於區分可修飾的對象。
    """
    def generate_modify_string(self, text: str) -> str:
        """
        該方法將'HtmlText'實例中的'text'修飾成符合預期的字串。
        """
        raise NotImplementedError


class HtmlText:
    """
    和'TextModifier'類別相對應的類別，當網頁元素可以具有文字內容(夾在'tag'之間的那段字串)時，需要繼承此類別。
    """
    def __init__(self, text: str = "") -> None:
        """
        建立一個名為'self.text'的變數。
        """
        self.text: str = text
    def text_modify(self, *modifiers: TextModifier):
        """
        該方法透過'TextModifier'的實例來修飾文字內容。
        """
        for modifier in modifiers:
            self.text = modifier.generate_modify_string(self.text)
        return self
