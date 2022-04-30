from urllib.parse import urljoin


class Scraping:
    def __init__(self):
        self.list_property_url = []
        self.list_property_name = []
        self.list_property_location = []
        self.list_property_price = []
        self.m_title = ""
        self.m_address = ""
        self.m_furnish = ""
        self.m_facilities = ""
        self.m_type = ""
        self.m_bfacilities = ""
        self.m_nearby = ""

    def scrap(self, page_soup):
        # Set empty array
        self.list_property_url = []
        self.list_property_name = []
        self.list_property_location = []
        self.list_property_price = []

        # Get all property content tag
        property_soup = page_soup.find_all("div", class_="property-box")

        # Scrap property url
        for x in property_soup:
            y = x.find("a")
            z = y["href"]  # Get href inside tag a
            url = urljoin("https:", z)
            self.list_property_url.append(url)

        # Scrap property name
        for x in property_soup:
            property_name = x.find("div", class_="property-detail-name")
            if property_name:
                self.list_property_name.append(property_name.text.strip())
            else:
                property_name = x.find("div", class_="property-name smoothening")
                self.list_property_name.append(property_name.text.strip())

        # Scrap property location
        for x in property_soup:
            property_location = x.find("div", class_="property-detail-desc")
            if property_location:
                self.list_property_location.append(property_location.text.strip())
            else:
                property_location = x.find("div", class_="property-info smoothening")
                y = property_location.text
                z = y.replace("• Full Furnished", "").strip()
                self.list_property_location.append(z)

        # Scrap property price
        for x in property_soup:
            property_price = x.find("div", class_="price")
            y = property_price.text
            z = y.replace("IDR", "").replace(",", "").replace("/ malam", "").replace("/ night", ""). \
                replace("/ bulan", "").replace("/ month", "").replace("/ tahun", "").replace("/ year", "").strip()
            self.list_property_price.append(z)

    def scrap_detail(self, url):
        # Property name
        title = url.find("h2")
        print(title.text.strip())
        self.m_title = title.text.strip()

        # Property address
        address = url.find("div", {"id": "hotel-address"})
        print(address.text.strip())
        self.m_address = address.text.strip()

        # Property furnish
        furnish = url.find("div", {"id": "hotel-property"})
        print(furnish.text.strip())
        self.m_furnish = furnish.text.strip()

        # Property facility
        temp = ""
        facilities = url.findAll("div", {"class": "hotel-info-facility-name"})
        for x in facilities:
            facility = x.text.strip()
            temp = f"{temp}{facility}, "
        print(temp.strip().strip(","))
        self.m_facilities = temp.strip().strip(",")

        # Property type
        x = url.find("div", {"class": "col-xs-12 hotel-left-item-info"})
        y = x.find("div", {"class": "hotel-left-item-info-detail capitalize"})
        print(y.text.strip())
        self.m_type = y.text.strip()

        # Property of building facility
        temp = ""

        daily_facility = url.find("div", {"class": "col-xs-4 hotel-facility-item daily-only"})
        if daily_facility:
            temp = f"{temp}{daily_facility.text.strip()}, "

        bfacility = url.find_all("div", {"class": "col-xs-4 hotel-facility-item"})
        if bfacility:
            for x in bfacility:
                temp = f"{temp}{x.text.strip()}, "
            print(temp.strip().strip(","))
            self.m_bfacilities = temp.strip().strip(",")
        else:
            print("Tidak tersedia Fasilitas Gedung")
            self.m_bfacilities = "Tidak tersedia Fasilitas Gedung"

        # Landmark Nearby
        temp = ""
        nearby = url.find("div", {"class": "nearby-landmark-wrapper"})
        if nearby:
            x = nearby.find_all("div", {"class": "col-xs-8"})
            for y in x:
                temp = f"{temp}{y.text.strip()}, "
            print(temp.strip().strip(","))
            self.m_nearby = temp.strip().strip(",")
        else:
            print("Tidak ada Objek Wisata Sekitar")
            self.m_nearby = "Tidak ada Objek Wisata Sekitar."
