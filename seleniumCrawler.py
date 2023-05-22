from time import sleep, time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import csv

class hotplaceCrawler:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def setup(self):
        chrome_service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=chrome_service)
        self.driver.maximize_window()

    def visit_page(self, url):
        self.driver.get(url)

    """
    把数据信息写入csv文件
    """

    def save_to_csv(self, data,place):
        with open('tour_info_'+place+'.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['名称', '价格', '出发地', '已售', '评分'])
            for row in data:
                writer.writerow(row)

    """
    获取首页跟团信息/首页和其他页信息不同
    """
    def get_tour_info_first(self,driver):
        tour_info = []
        # 获取所有的跟团信息
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='search-list']"))
        )
        # 获取单个的跟团信息
        rows = WebDriverWait(table, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='sight_item']"))
        )
        for row in rows:
            # 获取名称信息
            try:
                name = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//a[@class='name']"))
                ).text
            except:
                name = "暂无名称"

            # 获取价格信息
            try:
                price = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='sight_item_price']/em"))
                ).text
            except:
                price = "暂无价格"

            # 获取出发地信息
            try:
                departure = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='area']"))
                ).text
            except:
                departure = "暂无出发地"

            # 获取已售信息
            try:
                sold = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='relation_cap']"))
                ).text
            except:
                sold = "暂无已售"

            # 获取评分信息
            try:
                rating = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='relation_count']"))
                ).text
            except:
                rating = "暂无评分"
            print(name, price, departure, sold, rating)
            # 将跟团信息添加到列表中
            tour_info.append((name, price, departure, sold, rating))
        return tour_info

    """
    获取其他页跟团信息/首页和其他页信息不同
    """
    def get_tour_info_others(self,driver):
        tour_info = []
        # 获取单个的跟团信息
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='sight_item sight_itempos']"))
        )
        for row in rows:
            # 获取名称信息
            try:
                name = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//a[@class='name']"))
                ).text
            except:
                name = "暂无名称"

            # 获取价格信息
            try:
                price = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='sight_item_price']/em"))
                ).text
            except:
                price = "暂无价格"

            # 获取出发地信息
            try:
                departure = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='area']"))
                ).text
            except:
                departure = "暂无出发地"

            # 获取已售信息
            try:
                sold = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='relation_cap']"))
                ).text
            except:
                sold = "暂无已售"

            # 获取评分信息
            try:
                rating = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[@class='relation_count']"))
                ).text
            except:
                rating = "暂无评分"
            print(name, price, departure, sold, rating)
            # 将跟团信息添加到列表中
            tour_info.append((name, price, departure, sold, rating))
        return tour_info

    def get_page(self, place):
        try:
            self.visit_page("https://piao.qunar.com/")
        except:
            print("Error: 无法访问网页")
            return None
        print("正确访问网页")

        # 找到品质一日游
        a_subnav63 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='subnav63']")))
        a_subnav63.click()

        # 找到文本框进行输入
        input_search = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='searchValue']")))
        input_search.send_keys(place)

        # 找到搜索按钮并点击
        btn_search = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='searchBtn']")))
        btn_search.click()

        tour_info = []
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='search-list']"))
        )
        # 获取跟团信息
        page_tour_info = self.get_tour_info_first(table)
        tour_info.extend(page_tour_info)
        while True:
            # 查找下一页按钮
            try:
                next_page_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='next']")))
                # 点击下一页按钮
                next_page_link.click()
                sleep(5)
                # 重新定位table元素
                table = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='search-list']"))
                )
                # 获取跟团信息
                page_tour_info = self.get_tour_info_others(table)
                tour_info.extend(page_tour_info)
            except:
                print("信息爬取完毕...")
                break

        # 将跟团信息写入CSV文件
        self.save_to_csv(tour_info,place)

        # 返回结果
        return tour_info

    # 在完成所有操作后关闭浏览器：
    def teardown(self):
        self.driver.quit()

# 使用类的方法
crawler = hotplaceCrawler('chromedriver.exe')
crawler.setup()
crawler.get_page("北京")
# 在完成所有操作后关闭浏览器
crawler.teardown()
