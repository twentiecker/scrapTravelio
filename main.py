from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as Soup
import os
import scrolling
import scraping
import writing
import reading

file_name_writeRegion = "travelio_region"

scroll = scrolling.Scrolling()
scrap = scraping.Scraping()
write = writing.Writing()
read = reading.Reading()

# Define region that need to be scraped
if os.path.isfile(f"./{file_name_writeRegion}.csv"):  # Check file_name_writeRegion
    read.read_region(file_name_writeRegion)
else:
    regions = ["D.I. Yogyakarta,543e2bd9969324a955000025", "Banten,543e2a81969324a95500001a",
               "Jawa Tengah,543e2acf969324a955000020", "DKI Jakarta,543e2aab969324a95500001d",
               "Jawa Barat,543e2ac5969324a95500001f", "Jawa Timur,543e2ad8969324a955000021"]

    write.write_region(file_name_writeRegion, regions)
    read.read_region(file_name_writeRegion)

# Scrap every region that has been listed/writed before
list_region = tuple(read.list_region)
for y in list_region:
    z = y.split(",")
    file_name_write = f"travelio_{z[0]}"
    file_name_writeUrl = f"travelio_url_{z[0]}"
    file_name_writeDetail = f"travelio_detail_{z[0]}"
    file_name_remainder = f"travelio_url_remainder_{z[0]}"

    if os.path.isfile(f"./{file_name_remainder}.csv"):  # Check file_name_remainder
        # Read url in file_name_remainder
        print("===== START READING REMAINDER =====")
        read.read(file_name_remainder)
        print("===== FINISH READING REMAINDER =====")

        list_url = tuple(read.list_url)
        # Parsing html page
        for url in list_url:
            try:
                uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                page_html = urlopen(uClient).read()
                page_soup = Soup(page_html, "html.parser")

                # Scraping detail page
                print("===== START SCRAPING DETAIL =====")
                scrap.scrap_detail(page_soup)
                print("===== FINISH SCRAPING DETAIL =====")

                # Write the scraping result (detail page)
                print("===== START WRITING DETAIL =====")
                write.write_detail(file_name_writeDetail, scrap.m_title, scrap.m_address, scrap.m_furnish,
                                   scrap.m_facilities, scrap.m_type, scrap.m_bfacilities, scrap.m_nearby)
                print("===== FINISH WRITING DETAIL =====")

                # Remove url that has been scraped from the list_remainder
                for x in list_url:
                    if url == x:
                        read.list_url.remove(url)
                        break

                # Write remaining url that need to be scraped
                print("===== START WRITING REMAINDER =====")
                write.write_url(file_name_remainder, read.list_url)  # Remainder url
                print("===== FINISH WRITING REMAINDER =====")
            except HTTPError as err:
                if err.code == 404:
                    print("Page not found, Continue to the next link !!")

                    # Remove url that has been scraped from the list_remainder
                    for x in list_url:
                        if url == x:
                            read.list_url.remove(url)
                            break

                    # Write remaining url that need to be scraped
                    print("===== START WRITING REMAINDER =====")
                    write.write_url(file_name_remainder, read.list_url)  # Remainder url
                    print("===== FINISH WRITING REMAINDER =====")

                    continue
                else:
                    raise
    else:
        if not os.path.isfile(f"./{file_name_writeUrl}.csv"):
            # Url base bulanan
            url = f"https://www.travelio.com/en/search?searchType=monthly&destinationCategory=Region&" \
                  f"destinationUrlName=&destinationPlaceId=&destinationCountryId=ID&destinationId={z[1]}&nights=31&" \
                  f"flexible=1&destination={z[0]}&checkIn=02-03-2022&checkOut=02-04-2022&months=1&cbFlexible=on&" \
                  f"unitType=3%2C2%2C1%2Cstudio&propTypeId=room%2Cvilla%2Chouse%2Capartment&" \
                  f"sellType=Unfurnished%2CFull%2BFurnished"

            # # Url base harian
            # url = f"https://www.travelio.com/search?searchType=daily&destinationCategory=Region&destinationUrlName=&" \
            #       f"tempUiAutoComplete=&destinationId={z[1]}&destinationPlaceId=&destinationCountryId=ID&flexible=1&" \
            #       f"destination={z[0]}&checkIn=07-02-2022&checkOut=08-02-2022&nights=1&sellType=Full+Furnished&" \
            #       f"cbFlexible=on&unitType=3%2C2%2C1%2Cstudio&propTypeId=room%2Cvilla%2Chouse%2Capartment"

            # Scrolling until end of page
            print("===== START SCROLLING =====")
            scroll.scroll(url)
            print("===== FINISH SCROLLING =====")

            # Scrap the contents after finished scrolling until end of page
            print("===== START SCRAPING =====")
            scrap.scrap(scroll.page_soup)
            print("===== FINISH SCRAPING =====")

            # Write two file, append/crate file_name_write and create file_name_writeUrl
            print("===== START WRITING =====")
            write.write(file_name_write, scrap.list_property_name, scrap.list_property_location,
                        scrap.list_property_price,
                        scrap.list_property_url)
            write.write_url(file_name_writeUrl, scrap.list_property_url)
            print("===== FINISH WRITING =====")

        # Read url in file_name_writeUrl
        print("===== START READING =====")
        read.read(file_name_writeUrl)
        print("===== FINISH READING =====")

        if read.list_url:
            list_url = tuple(read.list_url)
            # Parsing html page
            for url in list_url:
                try:
                    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    page_html = urlopen(uClient).read()
                    page_soup = Soup(page_html, "html.parser")

                    # Scraping detail page
                    print("===== START SCRAPING DETAIL =====")
                    scrap.scrap_detail(page_soup)
                    print("===== FINISH SCRAPING DETAIL =====")

                    # Write the scraping result (detail page)
                    print("===== START WRITING DETAIL =====")
                    write.write_detail(file_name_writeDetail, scrap.m_title, scrap.m_address, scrap.m_furnish,
                                       scrap.m_facilities, scrap.m_type, scrap.m_bfacilities, scrap.m_nearby)
                    print("===== FINISH WRITING DETAIL =====")

                    # Remove url that has been scraped from the list_remainder
                    for x in list_url:
                        if url == x:
                            read.list_url.remove(url)
                            break

                    # Write remaining url that need to be scraped
                    print("===== START WRITING REMAINDER =====")
                    write.write_url(file_name_remainder, read.list_url)  # Remainder url
                    print("===== FINISH WRITING REMAINDER =====")
                except HTTPError as err:
                    if err.code == 404:
                        print("Ora ono halamane COOKKKK!!")

                        # Remove url that has been scraped from the list_remainder
                        for x in list_url:
                            if url == x:
                                read.list_url.remove(url)
                                break

                        # Write remaining url that need to be scraped
                        print("===== START WRITING REMAINDER =====")
                        write.write_url(file_name_remainder, read.list_url)  # Remainder url
                        print("===== FINISH WRITING REMAINDER =====")

                        continue
                    else:
                        raise

    # Check whether file_name_remainder still usefull or not
    print("===== START CHECKING FILE REMAINDER =====")
    if os.path.isfile(f"./{file_name_remainder}.csv"):
        read.read(file_name_remainder)
        if not read.list_url:
            os.remove(f"{file_name_remainder}.csv")
            os.remove(f"{file_name_writeUrl}.csv")
            print("===== ALL REMAINDER URL HAS BEEN SCRAPED =====")
            print("===== FINISH CHECKING FILE REMAINDER =====")
    else:
        os.remove(f"{file_name_writeUrl}.csv")
        print("===== ALL REMAINDER URL HAS BEEN SCRAPED =====")
        print("===== FINISH CHECKING FILE REMAINDER =====")

    # Remove region that has been scraped from the list_region
    for x in list_region:
        if y == x:
            read.list_region.remove(y)
            break

    # Write remaining region that need to be scraped
    print("===== START WRITING REGION REMAINDER =====")
    write.write_region(file_name_writeRegion, read.list_region)  # Remainder url
    print("===== FINISH WRITING REGION REMAINDER =====")

# Check whether file_name_writeRegion still usefull or not
print("===== START CHECKING FILE REGION REMAINDER =====")
read.read_region(file_name_writeRegion)
if not read.list_region:
    os.remove(f"{file_name_writeRegion}.csv")
    print("===== ALL REMAINDER REGION HAS BEEN SCRAPED =====")
    print("===== FINISH CHECKING FILE REGION REMAINDER =====")
