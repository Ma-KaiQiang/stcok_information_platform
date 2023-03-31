'''
Author : MaKaiQiang
dateTime: 2021-11-11
FileName:page_object.py
'''
import warnings
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from stock_app.business.news.base.exceptions import PageSelectException
from stock_app.business.news.base.exceptions import FindElementTypesError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('django')

LOCATOR_LIST = {
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME
}


class Browser:
    driver = None


class PageObject(object):
    """
    Page Object pattern.
    """

    def __init__(self, driver, url=None):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
        """
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        self.driver.implicitly_wait(5)

    def run_script(self, js=None, *args):
        """
        run JavaScript script
        """
        if js is None:
            raise ValueError("Please input js script")
        else:
            self.driver.execute_script(js, *args)


class PageSelect(object):
    """
    下拉框操作
    """
    warnings.warn("use NewPageElement instead", DeprecationWarning, stacklevel=2)

    def __init__(self, select_elem, value=None, text=None, index=None):
        if value is not None:
            Select(select_elem).select_by_value(value)
        elif text is not None:
            Select(select_elem).select_by_visible_text(text)
        elif index is not None:
            Select(select_elem).select_by_index(index)
        else:
            raise PageSelectException('"value" or "text" or "index" options can not be all empty.')


class PageWait(object):
    warnings.warn("use NewPageElement instead", DeprecationWarning, stacklevel=2)

    def __init__(self, elm, timeout=3):
        """
        元素等待
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        for i in range(timeout_int):
            if elm is not None:
                if elm.is_displayed() is True:
                    break
                else:
                    sleep(1)
            else:
                sleep(1)
        else:
            raise TimeoutError("Timeout, element invisible")


class NewPageElement(object):

    def __init__(self, timeout=5, describe="undefined", index=0, **kwargs):
        self.timeout = timeout
        self.index = index
        self.desc = describe
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST.keys():
            raise FindElementTypesError("Element positioning of type '{}' is not supported.".format(self.k))

    def __get__(self, instance, owner):
        if instance is None:
            return None

        Browser.driver = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)
        self.send_keys(value)

    def __find_element(self, elem):
        """
        Find if the element exists.
        """

        for i in range(self.timeout):
            elems = Browser.driver.find_elements(by=elem[0], value=elem[1])
            if len(elems) == 1:
                logger.warning("Find {n} elements through：{by}={value}".format(n=len(elems), by=elem[0], value=elem[1]))
                # return elems
                return True
            elif len(elems) > 1:
                logger.warning("Find {n} elements through：{by}={value}".format(n=len(elems), by=elem[0], value=elem[1]))
                return True
                # return elems
            else:
                sleep(1)
        else:
            logger.warning("Find 0 elements through：{by}={value}".format(by=elem[0], value=elem[1]))
            return False
            # return None

    def __get_element(self, by, value):
        """
        Judge element positioning way, and returns the element.
        """
        # selenium
        if by == "id_":
            try:
                elem = WebDriverWait(Browser.driver, timeout=10).until(
                    ec.visibility_of_element_located((By.ID, value)),
                    message='元素不可见')
            except Exception as e:
                logger.warning(e)
                return False
        elif by == "name":
            self.__find_element((By.NAME, value))
            elem = Browser.driver.find_elements_by_name(value)[self.index]
        elif by == "class_name":
            self.__find_element((By.CLASS_NAME, value))
            elem = Browser.driver.find_elements_by_class_name(value)[self.index]
        elif by == "tag":
            self.__find_element((By.TAG_NAME, value))
            elem = Browser.driver.find_elements_by_tag_name(value)[self.index]
        elif by == "link_text":
            self.__find_element((By.LINK_TEXT, value))
            elem = Browser.driver.find_elements_by_link_text(value)[self.index]
        elif by == "partial_link_text":
            self.__find_element((By.PARTIAL_LINK_TEXT, value))
            elem = Browser.driver.find_elements_by_partial_link_text(value)[self.index]
        elif by == "xpath":
            # self.__find_element((By.XPATH, value))
            try:
                if self.index == 'n':
                    elem = WebDriverWait(Browser.driver, timeout=self.timeout).until(
                        ec.visibility_of_all_elements_located((By.XPATH, value)),
                        message='元素不可见')
                else:
                    elem = WebDriverWait(Browser.driver, timeout=self.timeout).until(
                        ec.visibility_of_element_located((By.XPATH, value)),
                        message='元素不可见')

            except Exception as e:
                logger.warning(e)
                return False
            # elem = Browser.driver.find_elements(By.XPATH,value)[self.index]
        elif by == "css":
            self.__find_element((By.CSS_SELECTOR, value))
            elem = Browser.driver.find_elements_by_css_selector(value)[self.index]
        else:
            raise FindElementTypesError(
                "Please enter the correct targeting elements")

        if by in ["id_", "css", "name", "link_text", "partial_link_text", "tag", "class_name"]:
            style_red = 'arguments[0].style.border="2px solid red"'
            Browser.driver.execute_script(style_red, elem)

        return elem

    def elements(self):
        elems = self.__get_element(self.k,self.v)
        return elems

    def clear(self):
        """Clears the text if it's a text entry element."""
        elem = self.__get_element(self.k, self.v)
        logger.info("clear element: {}".format(self.desc))
        elem.clear()

    def send_keys(self, value):
        """
        Simulates typing into the element.
        """

        elem = self.__get_element(self.k, self.v)
        logger.info("send_keys element: {}".format(self.desc))
        elem.send_keys(value)

    def click(self):
        """Clicks the element."""
        try:
            elem = self.__get_element(self.k, self.v)
            logger.info("click element: {}".format(self.desc))
            elem.click()
        except Exception as e:
            raise e

    def submit(self):
        """Submits a form."""
        elem = self.__get_element(self.k, self.v)
        elem.submit()

    @property
    def tag_name(self):
        """This element's ``tagName`` property."""
        elem = self.__get_element(self.k, self.v)
        return elem.tag_name

    @property
    def text(self):
        """Clears the text if it's a text entry element."""
        elem = self.__get_element(self.k, self.v)
        if elem:
            return elem.text
        else:
            return False

    @property
    def size(self):
        """The size of the element."""
        elem = self.__get_element(self.k, self.v)
        return elem.size

    def get_property(self, name):
        """
        Gets the given property of the element.
        """
        elem = self.__get_element(self.k, self.v)
        return elem.get_property(name)

    def get_attribute(self, name):
        """Gets the given attribute or property of the element."""
        elem = self.__get_element(self.k, self.v)
        return elem.get_attribute(name)

    def is_displayed(self):
        """Whether the element is visible to a user."""
        elem = self.__get_element(self.k, self.v)
        return elem.is_displayed()

    def is_selected(self):
        """Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        elem = self.__get_element(self.k, self.v)
        return elem.is_selected()

    def is_enabled(self):
        """Returns whether the element is enabled."""
        elem = self.__get_element(self.k, self.v)
        return elem.is_selected()

    def switch_to_frame(self):
        """
        selenium API
        Switches focus to the specified frame
        """
        elem = self.__get_element(self.k, self.v)
        Browser.driver.switch_to.frame(elem)

    def move_to_element(self):
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).move_to_element(elem).perform()

    def click_and_hold(self):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).click_and_hold(elem).perform()

    def context_click(self):
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, x, y):
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def move_to_element_with_offset(self, x, y):
        ele = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).move_to_element_with_offset(to_element=ele, xoffset=x, yoffset=y).perform()

    def release(self):
        ele = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).release(on_element=ele).perform()

    def refresh_element(self, timeout=10):
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        elem = self.__get_element(self.k, self.v)
        for i in range(timeout_int):
            if elem is not None:
                try:
                    elem
                except StaleElementReferenceException:
                    Browser.driver.refresh()
                else:
                    break
            else:
                sleep(1)
        else:
            raise TimeoutError("stale element reference: element is not attached to the page document.")

    def select_by_value(self, value):
        """
        selenium API
        Select all options that have a value matching the argument. That is, when given "foo" this
           would select an option like:

           <option value="foo">Bar</option>

           :Args:
            - value - The value to match against

           throws NoSuchElementException If there is no option with specisied value in SELECT
        """
        select_elem = self.__get_element(self.k, self.v)
        Select(select_elem).select_by_value(value)

    def select_by_index(self, text):
        """
        selenium API
        Select the option at the given index. This is done by examing the "index" attribute of an
           element, and not merely by counting.

           :Args:
            - index - The option at this index will be selected

           throws NoSuchElementException If there is no option with specisied index in SELECT
        """
        select_elem = self.__get_element(self.k, self.v)
        Select(select_elem).select_by_index(text)

    def select_by_visible_text(self, text):
        """
        selenium API
        Select all options that display text matching the argument. That is, when given "Bar" this
           would select an option like:

            <option value="foo">Bar</option>

           :Args:
            - text - The visible text to match against

            throws NoSuchElementException If there is no option with specisied text in SELECT
        """
        select_elem = self.__get_element(self.k, self.v)
        Select(select_elem).select_by_visible_text(text)
