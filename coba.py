from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as Soup
import scraping
import writing

scrap = scraping.Scraping()
write = writing.Writing()
# url = "https://www.travelio.com/property/salatiga/unihouse-non-ac-room-for-one-person/?searchType=monthly&checkIn=11-02-2022&checkOut=11-03-2022&guest=1&nights=28&handpicked=&roomName=UNIHOUSE%20NON%20AC%20ROOM%20FOR%20ONE%20PERSON&roomBreakfast=0"
# url = "https://www.travelio.com/property/semarang/3br-homey-ceria/?searchType=monthly&checkIn=11-02-2022&checkOut=11-03-2022&guest=1&nights=28&handpicked=&roomName=3%20Bedrooms%20Homey%20Ceria&roomBreakfast=0"
# url = "https://www.travelio.com/en/property/jakarta/studio-bellmont-residence-near-puri-by-travelio/?searchType=daily&checkIn=07-02-2022&checkOut=08-02-2022&guest=1&nights=1&handpicked=&roomName=Studio%20Room%20&roomBreakfast=0"
# url = "https://www.travelio.com/property/semarang/3br-/?searchType=monthly&checkIn=23-02-2022&checkOut=11-03-2022&guest=1&nights=28&handpicked=&roomName=3%20Bedrooms%20Homey%20Ceria&roomBreakfast=0"
url = "https://www.travelio.com/en/property/yogyakarta-jogja/2-bedrooms-omah-yoja-1/?searchType=monthly&checkIn=09-03-2022&checkOut=02-04-2022&guest=1&nights=24&handpicked="

uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    page_html = urlopen(uClient).read()
    page_soup = Soup(page_html, "html.parser")

    scrap.scrap_detail(page_soup)
    print("===== START WRITING DETAIL =====")
    write.write_detail("coba", scrap.m_title, scrap.m_address, scrap.m_furnish,
                       scrap.m_facilities, scrap.m_type, scrap.m_bfacilities, scrap.m_nearby)
    print("===== FINISH WRITING DETAIL =====")
except HTTPError as err:
    if err.code == 404:
        print("ora ono")
    else:
        print("raise")
