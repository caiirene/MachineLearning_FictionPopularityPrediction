from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

fieldnames = ['book_id', 'book_name', 'latest_update_time', 'latest_chapter', 'word_count', 'total_recommend', 'weekly_recommend', 'book_intro_detail', 'book_intro', 'status', 'contract_vip', 'remaining_attributes', 'author_level', 'total_works', 'total_creation_words', 'creation_days']

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=service, options=options)

def get_one_book(url):
    book_data = {}
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        error_element = driver.find_elements(By.CSS_SELECTOR, "div.error-wrap-new")
        if error_element:
            return None

        # 获取书名
        book_name_tag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1#bookName")))
        book_data['book_name'] = book_name_tag.text.strip()

        # 获取最后更新时间
        latest_update_time_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.update-time")))
        book_data['latest_update_time'] = latest_update_time_span.text[5:15]

        # 获取最新章节
        latest_chapter_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.book-latest-chapter")))
        book_data['latest_chapter'] = latest_chapter_link.text

        # 获取字数
        word_count_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.count > em:nth-child(1)")))
        word_count_str = str(word_count_em.text)
        if word_count_str[-1] == "万":
            word_count_str = word_count_str[:-1]
            word_count = float(word_count_str) * 10000
        else:
            word_count = float(word_count_str)
        book_data['word_count'] = int(word_count)

        # 获取总推荐数
        total_recommend_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.count > em:nth-child(3)")))
        total_recommend_str = total_recommend_em.text.strip()
        if total_recommend_str[-1] == "万":
            total_recommend_str = total_recommend_str[:-1]
            total_recommend = float(total_recommend_str) * 10000
        else:
            total_recommend = float(total_recommend_str)
        book_data['total_recommend'] = int(total_recommend)

        # 获取周推荐数
        weekly_recommend_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.count > em:nth-child(5)")))
        weekly_recommend_str = weekly_recommend_em.text.strip()
        if weekly_recommend_str[-1] == "万":
            weekly_recommend_str = weekly_recommend_str[:-1]
            weekly_recommend = float(weekly_recommend_str) * 10000
        else:
            weekly_recommend = float(weekly_recommend_str)
        book_data['weekly_recommend'] = int(weekly_recommend)

        # 获取长简介
        book_intro_detail_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p#book-intro-detail")))
        book_data['book_intro_detail'] = book_intro_detail_em.text.strip()

        # 获取短简介
        book_intro_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.intro")))
        book_data['book_intro'] = book_intro_em.text.strip()

        # 获取book-attribute
        book_attribute_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.book-attribute")))
        book_attribute_spans = book_attribute_em.find_elements(By.TAG_NAME, "span")
        book_attribute_as = book_attribute_em.find_elements(By.TAG_NAME, "a")

        # 规则1：判断连载还是完本
        status = 0 if book_attribute_spans[0].text == "连载" else 1
        book_data['status'] = status

        # 规则2：判断免费还是签约+VIP
        if "免费" in [span.text for span in book_attribute_spans]:
            contract_vip = 0
        elif "签约" in [span.text for span in book_attribute_spans] and "VIP" in [span.text for span in book_attribute_spans]:
            contract_vip = 1
        else:
            contract_vip = -1  # 无法识别的情况
        book_data['contract_vip'] = contract_vip

        # 规则3：记录剩下的a标签的文本
        remaining_attributes = [a.text for a in book_attribute_as]
        book_data['remaining_attributes'] = remaining_attributes

        # 获取作者等级
        author_level_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.level-platina, p.level-lv, p.level-author, p.level-god")))
        author_level = -1  # 默认值
        for elem in author_level_elements:
            span_text = elem.find_element(By.TAG_NAME, "span").text.strip()
            if "level-platina" in elem.get_attribute("class"):
                author_level = 7
            elif "level-lv" in elem.get_attribute("class"):
                author_level = int(span_text.split('.')[1])  # "Lv.x" 中的 x
            elif "level-author" in elem.get_attribute("class"):
                author_level = 0
            elif "level-god" in elem.get_attribute("class"):
                author_level = 6
            if author_level != -1:
                break  # 找到等级后退出循环
        book_data['author_level'] = author_level

        # 获取作品总数
        total_works_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.work-number > em.color-font-card")))
        book_data['total_works'] = int(total_works_em.text.strip())

        # 获取总创作字数
        total_words_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.write > em.color-font-card")))
        total_words_str = total_words_em.text.strip()
        if total_words_str[-1] == "万":
            total_words = int(float(total_words_str[:-1]) * 10000)
        else:
            total_words = int(total_words_str)
        book_data['total_creation_words'] = total_words

        # 获取创作天数
        creation_days_em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.days > em.color-font-card")))
        book_data['creation_days'] = int(creation_days_em.text.strip())

        return book_data

    except Exception as e:
        print(f"Error while processing URL {url}: {e}")
        return None

with open('QidianBooks.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:  # 如果文件为空，则写入表头
        writer.writeheader()

    for book_id in range(1038307040, 1038307060 + 1):
        url = f"https://www.qidian.com/book/{book_id}/"
        book_data = get_one_book(url)
        if book_data:
            book_data['book_id'] = book_id
            print(book_id)
            writer.writerow(book_data)
