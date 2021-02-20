import requests
from bs4 import BeautifulSoup


def search_grape():
    want_to_search = input("Hi, would you like to find out about wine? (Enter Yes/No): ")
    while want_to_search.lower() == "yes":
        grape_query = input("What grape would you like to find?  ")

        URL = 'https://winefolly.com/grapes/' + grape_query.lower() + '/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        grape = soup.find('div', class_='col-12')
        grape_name = grape.find('h1', class_='px-5')

        flavors = soup.find(id='flavours')
        flavor_elems = flavors.find_all('ul', class_='flavours')
        

        taste_profile = soup.find(id='tasting-profile')
        taste_profile_elems = taste_profile.find_all('div')


        food_pairing = soup.find(id='food-pairing')
        food_pairing_elems = food_pairing.find_all('p')

        print("----------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------")
        print("   Grape: ", grape_name.text)
        print("----------------------------------------------------------------------------------------")
        for taste_profile_elem in taste_profile_elems:
            taste_sweetness = taste_profile_elem.find(class_='label sweetness')
            taste_body = taste_profile_elem.find(class_='label body')
            taste_tannins = taste_profile_elem.find(class_='label tannins')
            taste_acidity = taste_profile_elem.find(class_='label acidity')
            taste_alcohol = taste_profile_elem.find(class_='label alcohol')
            if None in (taste_sweetness, taste_body, taste_tannins, taste_acidity, taste_alcohol):
                continue
            print("Sweetness: ", taste_sweetness.text.strip())
            print("Body: ", taste_body.text.strip())
            print("Tannins: ", taste_tannins.text.strip())
            print("Acidity: ", taste_acidity.text.strip())
            print("Alcohol: ", taste_alcohol.text.strip())

        print("----------------------------------------------------------------------------------------")
        print("   Flavours:")
        print("----------------------------------------------------------------------------------------")

        for flavor_elem in flavor_elems:
            item_elems = flavor_elem.find_all('li')
            if None in flavor_elems:
                continue
            for item_elem in item_elems:
                name_elem = item_elem.find('span')
                print(name_elem.text)

        print("----------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------")
        print("   Food Pairing:")
        print("----------------------------------------------------------------------------------------")

        for food_pairing_elem in food_pairing_elems:
            #I need to add a cleaner to this so that it only displays food items
            print(food_pairing_elem.text)
            print("---------------   ---------   ----------   -----------    -----------   ---------------")

        print("----------------------------------------------------------------------------------------")
        
        search_again = input(" Would you like to make another search? (Enter Yes/No): ")
        if search_again.lower() == "no":
            print("----------------------------------------------------------------------------------------")
            print(" That's okay, see you around!")
            print("----------------------------------------------------------------------------------------")
            break

    else:
        print("----------------------------------------------------------------------------------------")
        print(" That's okay, see you around!")
        print("----------------------------------------------------------------------------------------")

if __name__ == '__main__':
    search_grape()
