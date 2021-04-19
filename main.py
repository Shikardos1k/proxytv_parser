from datetime import datetime
from ftplib import FTP
from re import findall, MULTILINE
from shutil import get_terminal_size
from time import sleep
from os import system, name as osName

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


__banner__ = """
╔═╗┬─┐┌─┐─┐ ┬┬ ┬╔╦╗╦  ╦╔═╗┌─┐┬─┐┌─┐┌─┐┬─┐
╠═╝├┬┘│ │┌┴┬┘└┬┘ ║ ╚╗╔╝╠═╝├─┤├┬┘└─┐├┤ ├┬┘
╩  ┴└─└─┘┴ └─ ┴  ╩  ╚╝ ╩  ┴ ┴┴└─└─┘└─┘┴└─
"""
__author__ = "Author: shikardosik"


while True:
    system("cls" if osName == "nt" else "clear")
    print(__banner__)
    print(__author__.center(get_terminal_size()[0] // 2, " "))
    
    browser = webdriver.Chrome()
    try:
        browser.get('https://proxytv.ru/')
        browser.find_element_by_css_selector("#formsearch > div > input[type=search]:nth-child(1)")\
            .send_keys(f"plist{Keys.RETURN}{Keys.BACKSPACE * 5}")
        
        html = browser.page_source
        while "https://proxytv.ru/iptv/img/flags/" not in html:
            html = browser.page_source
        
        channels = "#EXTM3U list-autor=\"shikardosik\"\n\n"
        for i in findall(r"плейлист \"(.*)\"", html):
            Q = "pl:" + i
            browser.find_element_by_css_selector("#formsearch > div > input[type=search]:nth-child(1)")\
                .send_keys(f"{Q}{Keys.RETURN}{Keys.BACKSPACE * len(Q)}")
            html = browser.page_source
            while "#EXTM3U" not in html and "Источники отсутствуют или ошибка подключения к БД!" not in html:
                html = browser.page_source
            channels += "\n\n".join(findall(r"(#EXTINF:.*:\d\d\d\d)", html, flags=MULTILINE)) + "\n\n"
    except WebDriverException:
        continue
    except KeyboardInterrupt:
        browser.quit()
        break
    browser.quit()
    channels = channels[:-2].replace("<br>", "\n").replace("<b>", "").replace("</b>", "")
    
    fn = "all.m3u8"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(channels)
    
    ftp = FTP("5.252.116.9")
    ftp.login("tv", "H3i4H1n5")
    
    with open(fn, "rb") as f:
        ftp.storbinary("STOR " + fn, f, 512)
    
    print(datetime.today(), "Updated")
    sleep(60*5)
