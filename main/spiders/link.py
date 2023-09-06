import scrapy
from main.items import MainItem

class LinkSpider(scrapy.Spider):
    name = "link"
    subgroup_link_no = 0
    start_url = 'https://www.catcar.info/jaguar'
    base_payload = "=&i=36fa3ecc0b2d2bfe0bec0f2b369f24db&q=HF%1B%05%1B%1C%07%1F%00%01V%19P%02%11%00%1BB%0C%06%11%19Y7%5E%0C%1B%0D%05%0D%40Z1CVJ%14DBI%3E%05%0B%0C%18%01%0B_%03F%3C5L%5EUYGXH_%024WSY%3B%0C%06AB%5DIsS%40Q%11ZQARDH%3BA%06%1E%04%3E%09%07%23%1E%02%5DHwCAVG_SMEFP1y%22%3F-L%5E%26MEF%14%13Z%13WSY%2B%00%0B%1C%19Q_%03F1%09%1B%03%08%0DRD%3EK%00%40%5CQG%5CKXRDH)P%10%13%13%00IW.BEOT%02%40&b=45641106"
    headers = {
            "authority": "www.catcar.info",
            "accept": "text/javascript, text/html, application/xml, text/xml, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "_ym_uid=1690186051751525270; _ym_d=1690186051; _ym_isad=2; __gads=ID=1006d74feef29199-224615b0e4e20041:T=1690186052:RT=1692207113:S=ALNI_MZUFDsrRNcCTV6kHyHjER54P7Zsmw; __gpi=UID=00000d0f3ec2117e:T=1690186052:RT=1692207113:S=ALNI_MbBX4a4T-MHTktk0Ghf-mWW4H92cg; PHPSESSID=1216289d4b14ae274e912c9a58d33721; __utma=221044234.106513709.1690827390.1692207094.1692272440.17; __utmc=221044234; __utmz=221044234.1692272440.17.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ym_visorc=w; __utmb=221044234.2.10.1692272440",
            "origin": "https://www.catcar.info",
            "referer": "https://www.catcar.info/jaguar/?lang=en",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
    def start_requests(self):
        url_with_params = f"{self.start_url}?fromchanged=true&lang=en" 
        yield scrapy.Request(
            url=url_with_params,
            method='POST',
            headers=self.headers,
            body=self.base_payload,
            callback=self.parse
        )

    def parse(self, response):
        cars = response.xpath('//li')
        for car in cars:
            title = car.xpath('.//div[@align="center" and @name="title"]/text()').get()
            link = car.xpath('.//div[contains(@style, "padding:4px;")]/@onclick').re_first(r"HM\.set\(\'(.*?)\'\)")
            image_url = car.xpath('.//img/@src').get()

            model_title = title
            model_link = self.start_url + '/?lang=en#' + link
            model_image = image_url

            url = f"https://www.catcar.info/jaguar/?fromchanged=true&lang=en&l={link}"
            yield scrapy.Request(
            url=url,
            method='POST',
            headers=self.headers,
            body=self.base_payload,
            callback=self.body,
            cb_kwargs={'model_title':model_title,'model_link':model_link,'model_image':model_image}
        )



    def body(self,response,model_title,model_link,model_image):
        tr_tags = response.xpath('//tr[contains(@class, "over")]')
        for tr in tr_tags:
            title = tr.xpath('./td/text()').get()
            onclick_value = tr.xpath('./@onclick').re_first(r"HM\.set\(\'(.*?)\'\)")
            parameter_title = title.strip() if title else None
            parameter_link = self.start_url + '/?lang=en#' + onclick_value
            url = f"https://www.catcar.info/jaguar/?fromchanged=true&lang=en&l={onclick_value}"
            yield scrapy.Request(
                url=url,
                method='POST',
                headers=self.headers,
                body=self.base_payload,
                callback=self.maingroup_page,
                cb_kwargs={'model_title':model_title,'model_link':model_link,'model_image':model_image,'parameter_title':parameter_title,'parameter_link':parameter_link}
                )

    def maingroup_page(self, response,model_title,model_link,model_image,parameter_title,parameter_link):
        tr_tags = response.xpath('//tr[@class="over oddeng"]')
        for tr in tr_tags:
            title = tr.xpath('./td/text()').get()
            onclick_value = tr.xpath('./@onclick').re_first(r"HM\.set\(\'(.*?)\'\)")
            group_title = title.strip() if title else None
            group_link = self.start_url + '/?lang=en#' + onclick_value
            url = f"https://www.catcar.info/jaguar/?fromchanged=true&lang=en&l={onclick_value}"
            yield scrapy.Request(
                url=url,
                method='POST',
                headers=self.headers,
                body=self.base_payload,
                callback=self.subgroup_page,
                cb_kwargs={'model_title':model_title,'model_link':model_link,'model_image':model_image,'parameter_title':parameter_title,'parameter_link':parameter_link,
                'group_title':group_title,'group_link':group_link         
                })

    def subgroup_page(self , response,model_title,model_link,model_image,parameter_title,parameter_link,group_title,group_link):
        tr_tags = response.xpath('//tr[contains(@class, "over")]')
        for tr in tr_tags:
            title = tr.xpath('./td/text()').get()
            onclick_value = tr.xpath('./@onclick').re_first(r"HM\.set\(\'(.*?)\'\)")
            subgroup_title = title.strip() if title else None
            subgroup_link = self.start_url + '/?lang=en#' + onclick_value


            self.subgroup_link_no+=1
            item = MainItem()
            item['model_title'] = model_title
            item['model_link'] = model_link
            item['model_image'] = model_image
            item['parameter_title'] = parameter_title
            item['parameter_link'] = parameter_link
            item['group_title']= group_title
            item['group_link']= group_link
            item['subgroup_title']=subgroup_title 
            item['link_no']=self.subgroup_link_no
            item['subgroup_link']=subgroup_link


            yield item
        